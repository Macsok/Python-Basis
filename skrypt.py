from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = 'https://www.google.com/search?q=olx&oq=olx&gs_lcrp=EgZjaHJvbWUqBwgAEAAYjwIyBwgAEAAYjwIyDQgBEC4YxwEY0QMYgAQyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyBwgGEAAYgAQyBggHEEUYPNIBCDIzNDVqMGo0qAIAsAIA&sourceid=chrome&ie=UTF-8'
#url = 'https://www.youtube.com/@Hallden_'
browser = webdriver.Chrome()
browser.get(url)
browser.find_element(By.XPATH, '//*[@id="W0wltc"]').click()
browser.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a')
#browser.find_element_by_xpath('//*[@id="thumbnail"]').click()