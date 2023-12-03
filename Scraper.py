from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import math
import re

#-----------------------------------
#       CUSTOMIZATION

#   provide url to SECOND PAGE (with no filters)
url = 'https://www.pracuj.pl/praca/sprzedawca;kw?pn=2'

#   select pages (e.g. 1, 1)
first_page = 1
last_page = 0

#   choose whether you want to save scrapped data
save_to_file = False
file_path = 'scrapped data/sprzedawca.csv'

#   Show avg. salary density
show_plot = True

#-----------------------------------
#   Compare salaries from files

compare = True
sal_file1 = 'scrapped data/sprzedawca.csv'
sal_file2 = 'scrapped data/spawacz.csv'
sal_file3 = 'scrapped data/'
sal_file4 = 'scrapped data/specjalista ai.csv'

#-----------------------------------

pages_list = [i for i in range(first_page, last_page + 1)]
#   Striping last character - page number
base_url = url[:-1]

#   Create empty lists to fill in
links_array = []
titles_array = []
additional_info0_array = []
additional_info1_array = []
additional_info2_array = []
additional_info3_array = []
offer_salary_array = []
salary_from_array = []
salary_to_array = []
plus_VAT_array = []
technologies_list_array = []
is_super_array = []
date_array = []
company_name_array = []
localization_array = []

#   Looping through pages
for current_page in pages_list:
    try:
        print('Trying to connect...')
        #   Setting correct page-url address
        page_url = base_url + str(current_page)
        html_text = requests.get(page_url).text
    except:
        print('Failed to connect.')
        continue

    print(f'Scraping page no. {current_page}...')

    #   Save page content
    soup = BeautifulSoup(html_text, 'lxml')

    #   Create list of offers (select only default offers, recommended and sugested excluded)
    offers = soup.find_all('div', attrs = {'data-test' : 'default-offer'})

    #   Loop through offers -------------------------------------------
    for offer in offers:
        #   search for additional info
        try:
            additional_info0_array.append(offer.find('li', attrs = {'data-test' : 'offer-additional-info-0'}).text)
        except:
            additional_info0_array.append(None)
        try:
            additional_info1_array.append(offer.find('li', attrs = {'data-test' : 'offer-additional-info-1'}).text)
        except:
            additional_info1_array.append(None)
        try:
            additional_info2_array.append(offer.find('li', attrs = {'data-test' : 'offer-additional-info-2'}).text)
        except:
            additional_info2_array.append(None)
        try:
            additional_info3_array.append(offer.find('li', attrs = {'data-test' : 'offer-additional-info-3'}).text)
        except:
            additional_info3_array.append(None)

        #   Type correction / getting text when attribute is provided ( <>...<> ==> .. )
        offer_salary = offer.find('span', attrs = {'data-test' : 'offer-salary'}).text if offer.find('span', attrs = {'data-test' : 'offer-salary'}) else None
        offer_salary_array.append(offer_salary)

        #   Split salary in two - from ... to ...
        if offer_salary:
            offer_salary = str(offer_salary)
            salary_from = re.search('[0-9]+[\s]?[0-9]+', offer_salary).group()
            
            #   Filter data with regex
            if re.search('[–]', offer_salary):
                salary_to = re.search('–[0-9]+[\s]?[0-9]+', offer_salary).group()[1:]
            else:
                salary_to = None

            #   Check wether VAT is included
            if re.search('VAT', offer_salary):
                plus_VAT = True
            else:
                plus_VAT = False
        else:
            salary_from = None
            salary_to = None
            plus_VAT = None
        
        #   Move data to list
        salary_from_array.append(salary_from)
        salary_to_array.append(salary_to)
        plus_VAT_array.append(plus_VAT)

        #   Get offer title
        titles_array.append(offer.find('h2', attrs = {'data-test' : 'offer-title'}).text)
        
        #   List of technologies
        technologies_list_array.append((offer.find('div', attrs = {'data-test' : 'technologies-list'}).text if offer.find('div', attrs = {'data-test' : 'technologies-list'}) else None))

        #   When was added
        date_array.append(offer.find('p', attrs = {'data-test' : 'text-added'}).text)

        #   Check if is super offer
        if offer.find('span', attrs = {'data-test' : 'text-super-offer'}):
            is_super = True
        else:
            is_super = False
        is_super_array.append(is_super)

        #   Find company name
        company_name_array.append(offer.find('h4', attrs = {'data-test' : 'text-company-name'}).text)

        #   Company and work localization
        localization_array.append(offer.find('h5', attrs = {'data-test' : 'text-region'}).text)

        #   Get offer link
        try:
            #   Get the href=...
            link = offer.find('a', attrs = {'data-test' : 'link-offer'})['href']
        except:
            link = None
        links_array.append(link)
        #--------------------------------------

    #------------------------------------------

#   Update the dictionary
dict_data = {'link' : links_array, 
             'title' : titles_array,
             'company' : company_name_array,
             'salary' : offer_salary_array,
             'salary from' : salary_from_array,
             'salary to' : salary_to_array,
             'plus VAT' : plus_VAT_array,
             'is super' : is_super_array,
             'technologies' : technologies_list_array,
             'date' : date_array,
             'localization' : localization_array,
             'add. info0' : additional_info0_array,
             'add. info1' : additional_info1_array,
             'add. info2' : additional_info2_array,
             'add. info3' : additional_info3_array,
             }

#   convert dictionary to pandas DataFrame
bricks = pd.DataFrame(dict_data)

#   Display DataFrame without 'link' column
#print(bricks.drop('link', axis=1))
#print(bricks[['technologies']])

def plot_histogram(x):
    #   Draw a histogram
    plt.hist(sorted(x), density=True, facecolor='g', alpha = 0.5)  # density=False would make counts
    plt.ylabel('Density')
    plt.xlabel('Salary')
    plt.grid(True)
    plt.yticks([])
    plt.xticks(rotation = 45)
    #plt.yticks([0, 25, 50, 100])
    plt.show()

def normalize_salary(salary_from_array, salary_to_array):
    #   Convert $/hour to $/month (x168)
    for a, b, i in zip(salary_from_array, salary_to_array, range(len(salary_from_array))):
    #   Since salary_from_array and salary_to_array have same lenght we can change both at once
        s_from = int(str(a).replace(u'\xa0', u'') if a != None else 0)
        s_to = int(str(b).replace(u'\xa0', u'') if b != None else 0)

        if s_from < 1000:
            salary_from_array[i] = s_from * 168
        else:
            salary_from_array[i] = s_from
        if s_to > 1000:
            salary_to_array[i] = s_to
        else:
            salary_to_array[i] = s_to * 168
    #   mean/average
    avg_salary_array = []
    for a, b in zip(salary_from_array, salary_to_array):
        avg_salary_array.append( (a+b) / 2)
    return avg_salary_array

def comparision_histogram(file1 = '', file2 = '', file3 = '', file4 = ''):
    #   convert file to array
    def avg_salary_list_from_file(file_path = ''):
        if file_path != '':
            #   Try opening a file
            try:
                df = pd.read_csv(file_path)
            except:
                print('file:', file_path, 'not found.')
                return []

            #   Filter nan's
            list_from = []
            for a in df['salary from']:
                if str(a) != 'nan':
                    list_from.append(a)
                else:
                    list_from.append(None)
            
            #   Filter nan's
            list_to = []
            for a in df['salary to']:
                if str(a) != 'nan':
                    list_to.append(a)
                else:
                    list_to.append(None)
            #   return normalized ('/x0' -> '')and sorted
            return sorted(normalize_salary(list_from, list_to))
        else:
            return []
        
    #   Generate multiplot
    plt.hist(avg_salary_list_from_file(file1), density=True, facecolor='green', alpha = 0.5, label = file1)
    plt.hist(avg_salary_list_from_file(file2), density=True, facecolor='blue', alpha = 0.5, label = file2)
    plt.hist(avg_salary_list_from_file(file3), density=True, facecolor='magenta', alpha = 0.5, label = file3)
    plt.hist(avg_salary_list_from_file(file4), density=True, facecolor='yellow', alpha = 0.5, label = file4)
    plt.yticks([])
    plt.xlabel('Salary')
    plt.ylabel('Density')
    plt.legend(loc = 'upper right')
    plt.show()

if compare:
    comparision_histogram(sal_file1, sal_file2, sal_file3, sal_file4)

if show_plot:
    if dict_data != {}:
        avg_salary_array = normalize_salary(salary_from_array = salary_from_array, salary_to_array = salary_to_array)
        plot_histogram([x for x in avg_salary_array if x != 0])

if save_to_file:
    bricks.to_csv(file_path)