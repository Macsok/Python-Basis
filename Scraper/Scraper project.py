from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import requests
import tkinter

import re

#-----------------------------------
#       CUSTOMIZATION

#   provide url to SECOND PAGE (with no filters)
url = 'https://it.pracuj.pl/praca/front%20end%20developer;kw?pn=2'
scrap_from_online = True

#   select pages (e.g. 1, 1)
first_page = 1
last_page = 0

#   choose whether you want to save scrapped data
save_to_file = False
file_path = 'scrapped data/sap.csv'

#   Show avg. salary density
show_plot = 0

#-----------------------------------
#   Compare salaries from files

compare = False
sal_file1 = 'scrapped data/elektryk.csv'
sal_file2 = 'scrapped data/sap.csv'
sal_file3 = 'scrapped data/'
sal_file4 = 'scrapped data/'

#-----------------------------------

use_window = True

def input_window():

    def enter_data():
        #   Assign data
        global url
        global first_page
        global last_page
        global scrap_from_online
        global save_to_file
        global file_path
        global show_plot
        global compare
        global sal_file1
        global sal_file2
        global sal_file3
        global sal_file4
        url = url_entry.get()
        first_page = int(first_page_entry.get())
        last_page = int(last_page_entry.get())
        scrap_from_online = use_online_var.get()
        save_to_file = save_to_f_var.get()
        file_path = f_path_entry.get()
        show_plot = show_plot_var.get()
        compare = compare_var.get()
        sal_file1 = f_path_1_entry.get()
        sal_file2 = f_path_2_entry.get()
        sal_file3 = f_path_3_entry.get()
        sal_file4 = f_path_4_entry.get()
        #   Close window
        window.destroy()

    window = tkinter.Tk()
    window.title('DataScraper Entry Form')

    frame = tkinter.Frame(window)
    frame.pack()

    #   Online scraping URL getter and disabling
    get_url = tkinter.LabelFrame(frame, text = 'URL')
    get_url.grid(row= 0, column= 0, padx= 20, pady = 20)

    url_label = tkinter.Label(get_url, text = 'URL - link to 2nd page')
    url_label.grid(row = 0, column = 0)
    url_entry = tkinter.Entry(get_url)
    url_entry.grid(row = 1, column = 0)

    disable_checkbox_label = tkinter.Label(get_url, text = 'Scrap from online')
    disable_checkbox_label.grid(row = 0, column = 1)
    
    use_online_var = tkinter.BooleanVar()
    disable_checkbox = tkinter.Checkbutton(get_url, variable = use_online_var, onvalue = True, offvalue = False)
    disable_checkbox.grid(row = 1, column = 1)

    #   configure every element in specified grid
    for widget in get_url.winfo_children():
        widget.grid_configure(padx= 10, pady= 5)

    #   Online scraping customization
    online_custom_frame = tkinter.LabelFrame(frame, text = 'Online scraping configuration')
    online_custom_frame.grid(row = 1, column = 0, padx = 20, pady = 20)

    first_page_label = tkinter.Label(online_custom_frame, text = 'First page')
    first_page_label.grid(row = 0, column = 0)
    first_page_entry = tkinter.Spinbox(online_custom_frame, from_ = 1, to = 'infinity')
    first_page_entry.grid(row = 1, column = 0)

    last_page_label = tkinter.Label(online_custom_frame, text = 'Last page')
    last_page_label.grid(row = 0, column = 1)
    last_page_entry = tkinter.Spinbox(online_custom_frame, from_ = 1, to = 'infinity')
    last_page_entry.grid(row = 1, column = 1)

    save_to_f_var = tkinter.BooleanVar()
    save_to_file_checkbox = tkinter.Checkbutton(online_custom_frame, text = 'Save to file', variable = save_to_f_var, onvalue = True, offvalue=False)
    save_to_file_checkbox.grid(row = 3, column = 0)

    f_path_label = tkinter.Label(online_custom_frame, text = 'File path')
    f_path_label.grid(row = 2, column = 1)
    f_path_entry = tkinter.Entry(online_custom_frame)
    f_path_entry.insert(0, 'scrapped data/')
    f_path_entry.grid(row = 3, column = 1)

    show_plot_var = tkinter.BooleanVar()
    show_plot_checkbox = tkinter.Checkbutton(online_custom_frame, text = 'Show histogram', variable = show_plot_var, onvalue=True, offvalue=False)
    show_plot_checkbox.grid(row = 4, column = 0)

    #   configure every element in specified grid
    for widget in online_custom_frame.winfo_children():
        widget.grid_configure(padx= 10, pady= 5)

    #   Compare scrapped data
    from_files_frame = tkinter.LabelFrame(frame, text = 'Compare from csv files')
    from_files_frame.grid(row = 2, column = 0, padx = 20, pady = 20)

    compare_var = tkinter.BooleanVar()
    comp_from_files_checkbox = tkinter.Checkbutton(from_files_frame, text = 'Compare from files', variable=compare_var, onvalue=True, offvalue=False)
    comp_from_files_checkbox.grid(row = 0, column = 0)

    f_path_1_label = tkinter.Label(from_files_frame, text = '1. File path')
    f_path_1_label.grid(row = 1, column = 0)
    f_path_1_entry = tkinter.Entry(from_files_frame)
    f_path_1_entry.insert(0, 'scrapped data/')
    f_path_1_entry.grid(row = 2, column = 0)

    f_path_2_label = tkinter.Label(from_files_frame, text = '2. File path')
    f_path_2_label.grid(row = 1, column = 1)
    f_path_2_entry = tkinter.Entry(from_files_frame)
    f_path_2_entry.insert(0, 'scrapped data/')
    f_path_2_entry.grid(row = 2, column = 1)

    f_path_3_label = tkinter.Label(from_files_frame, text = '3. File path')
    f_path_3_label.grid(row = 3, column = 0)
    f_path_3_entry = tkinter.Entry(from_files_frame)
    f_path_3_entry.insert(0, 'scrapped data/')
    f_path_3_entry.grid(row = 4, column = 0)

    f_path_4_label = tkinter.Label(from_files_frame, text = '4. File path')
    f_path_4_label.grid(row = 3, column = 1)
    f_path_4_entry = tkinter.Entry(from_files_frame)
    f_path_4_entry.insert(0, 'scrapped data/')
    f_path_4_entry.grid(row = 4, column = 1)

    #   configure every element in specified grid
    for widget in from_files_frame.winfo_children():
        widget.grid_configure(padx= 10, pady= 5)

    #   Button
    button = tkinter.Button(frame, text = 'Enter data', command = enter_data)
    button.grid(row = 3, column = 0, sticky = 'news', padx = 20, pady = 10)

    window.mainloop()

if use_window: input_window()
#   Make an empty array of pages to go through
if scrap_from_online == False:
    first_page = 1
    last_page = 0

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
        #date_array.append(offer.find('p', attrs = {'data-test' : 'text-added'}).text)
        date_array.append(offer.find('p', attrs = {'data-test' : 'text-added'}))

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
    plt.ylabel('Distribution')
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
            return [a for a in sorted(normalize_salary(list_from, list_to)) if a != None and a != 0]
        else:
            return []
        
    #   Generate multiplot
    plt.hist(avg_salary_list_from_file(file1), density=True, facecolor='green', alpha = 0.5, label = file1.split('/')[-1].split('.')[0])
    plt.hist(avg_salary_list_from_file(file2), density=True, facecolor='blue', alpha = 0.5, label = file2.split('/')[-1].split('.')[0])
    plt.hist(avg_salary_list_from_file(file3), density=True, facecolor='magenta', alpha = 0.5, label = file3.split('/')[-1].split('.')[0])
    plt.hist(avg_salary_list_from_file(file4), density=True, facecolor='yellow', alpha = 0.5, label = file4.split('/')[-1].split('.')[0])
    plt.yticks([])
    plt.xlabel('Salary')
    plt.ylabel('Density')
    plt.legend(loc = 'upper right')
    plt.grid(True)
    plt.show()

if compare:
    comparision_histogram(sal_file1, sal_file2, sal_file3, sal_file4)

if show_plot:
    if dict_data != {}:
        avg_salary_array = normalize_salary(salary_from_array = salary_from_array, salary_to_array = salary_to_array)
        plot_histogram([x for x in avg_salary_array if x != 0])

if save_to_file:
    bricks.to_csv(file_path)