# import required libraies 
from selenium import webdriver
import time
import pandas as pd
import os
links = []


# distance and zipcode manual input from terminal
distance = input('Distance: ') or '50'
zipCode = input('Zipcode: ') or ''
# loding google drivers
script_dir = os.path.dirname(__file__)
rel_path = "driver\chromedriver.exe"
abs_file_path = os.path.join(script_dir, rel_path)
driver = webdriver.Chrome(abs_file_path)

driver.get(f'https://www.tred.com/buy?body_style=&distance={distance}&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip={zipCode}')
time.sleep(2)
# loading all js files links from website
previous_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    link_elements = driver.find_elements_by_css_selector('.grid-box-container a')

    for link_el in link_elements:
        
        href = link_el.get_attribute('href')

        links.append(href)
    if  previous_height== new_height:
        break
    
    previous_height = new_height

# scrabing data from individual links
name = []
price = []
vehicle_summary = []
vehicle_option = []
for j in links:
    driver.get(j)
    time.sleep(2)
    try:
        v_name = driver.find_element_by_css_selector('.lede-left h2')
        v_price = driver.find_element_by_css_selector('.no-arrow h2')
        v_details = driver.find_elements_by_css_selector('.col-md-7 td')
        v_option = driver.find_elements_by_css_selector('#options-table tr:nth-child(10) td')
        if (v_name and v_price and v_details and v_option) is not None:
            name.append(v_name.text)
            price.append(v_price.text)
            ls = []
            for d in v_details:
                ls.append(d.text)
            vehicle_summary.append(ls)
            ls = []
            for d in v_option:
                ls.append(d.text)
            vehicle_option.append(ls)
    except:
        pass

    
driver.quit()   

product_list = {
    'name':name,
    'price':price,
    'veihcle_Summary':vehicle_summary,
    'veichle_option':vehicle_option


}


#making data frame and csv file
df = pd.DataFrame(product_list)
df.to_csv('data.csv', sep=',', encoding='utf-8')
    