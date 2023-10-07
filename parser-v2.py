#!/usr/bin/env python
# coding: utf-8

# In[5]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm

# Задание параметров
list_params = ["2020",98]

browser = webdriver.Chrome()
list_links = []
values = list_params
for i in range(1, values[1] + 1):
    link = (f"https://auto.ru/sankt-peterburg/cars/vendor-foreign/all/?year_from={values[0]}"
            f"&page={i}")
    browser.get(link)
    links = browser.find_elements(By.CLASS_NAME, "ListingItemTitle__link")
    # Сохраняем ссылки в список    
    for link in links:
        list_links.append(link.get_attribute("href"))

test_links = list_links[:2]

# Проходим по каждой странице
list_result = []
for file_link, i in zip(list_links, tqdm(list_links)):
    browser.get(file_link)
    try:
        list_1 = browser.find_element(By.CLASS_NAME, "CardHead__title").text.split(",")
        probeg = browser.find_element(By.CLASS_NAME, 'CardInfoRow_kmAge').text.split("\n")[1]
        list_2 = browser.find_element(By.CLASS_NAME, 'CardInfoRow_engine').text.split('\n')[1].split('/')
        car = {   
            'car': list_1[0],
            'year': list_1[1],
            'mosh':list_2[0],
            'obyem':list_2[1],
            'type_dvig':list_2[2],
            'km': probeg
        }
        list_result.append(car)
    except:
        pass

df = pd.DataFrame(list_result)

# Разделим на бензин и электро
df_b = df.query("type_dvig != ' Электро'")
df_e = df.query("type_dvig == ' Электро'")

# Правим датасет
df_b['mosh'] = df_b['mosh'].apply(lambda x : str(x)[:-2]).apply(lambda x : float(x))
df_b['obyem'] = df_b['obyem'].apply(lambda x : str(x)[:-5]).apply(lambda x : int(x))
df_b['year'] = df_b['year'].apply(lambda x : int(x))
df_b['km'] = df_b['km'].apply(lambda x : str(x)[:-3]).str.replace(" ", "").apply(lambda x : int(x)/1000)

# Правим датасет
obyem = df_e.mosh
mosh = df_e.obyem
df_e['mosh'] = mosh 
df_e['obyem'] = obyem
df_e['mosh'] = df_e['mosh'].apply(lambda x : str(x)[:-4]).apply(lambda x : float(x))
df_e['obyem'] = df_e['obyem'].apply(lambda x : str(x)[:-5]).apply(lambda x : int(x))
df_e['year'] = df_e['year'].apply(lambda x : int(x))
df_e['km'] = df_e['km'].apply(lambda x : str(x)[:-3]).str.replace(" ", "").apply(lambda x : int(x)/1000)
df_e

# Сохраняем результаты
df.to_excel(r'dataset.xlsx', index=False)

