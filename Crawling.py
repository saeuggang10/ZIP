import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc #한글지원
import platform
import seaborn as sns
import re

import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

file_path = './data/'


#----------------------------------------------------------------------------#
# df setting
col = ['date', 'state', 'num', 'tot'] # 'year', 'mon', 'day', 
df = pd.DataFrame([np.zeros(len(col))], columns=col)
num = 0

#----------------------------------------------------------------------------#
# Crawling
# - 2021.05.01~2024.05.31
lis1 = [str(ttemp) for ttemp in range(4,12)]
lis2 = [str(ttemp) for ttemp in range(12)]
lis3 = [str(ttemp) for ttemp in range(5)]

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# DeepL 웹사이트에 접속
deepl_url = 'https://stcis.go.kr/wps/dashBoard.do'

button_css = '//*[@id="container"]/form/fieldset/div/table/tbody/tr/td[1]/span/a'
back_xpath = '//*[@id="ui-datepicker-div"]/div/a[1]/span'

year_xpath = '//*[@id="ui-datepicker-div"]/div/div/select[1]'
mon_xpath = '//*[@id="ui-datepicker-div"]/div/div/select[2]'

cal_img_xpath = '//*[@id="container"]/div[1]/dl[1]/dt/h2/img'
cal_xpath = '//*[@id="ui-datepicker-div"]/table/tbody'
num_xpath = '//*[@id="container"]/div[3]/div[2]/div[1]/div'
num2_xpath = '//*[@id="container"]/div[3]/div[1]/div[1]/div'

driver.get(deepl_url)

# drop box _ value select
select_rtry = Select(driver.find_element(By.ID, "rtryCd"))
select_rtry.select_by_value("11")

time.sleep(1)

# 검색 버튼
button = driver.find_element(By.XPATH, button_css)
button.click()

# drop box _ value list
select_sgg = Select(driver.find_element(By.ID, "sggCd"))
all_options = select_sgg.options
all_options_value = [option.get_attribute('value') for option in all_options if option.get_attribute('value')]

for option in all_options_value[:10]:
    # 구 선택
    select_sgg = Select(driver.find_element(By.ID, "sggCd"))
    select_sgg.select_by_value(option)
    
    # 검색버튼 클릭
    button = driver.find_element(By.XPATH, button_css)
    button.click()
    
    img_btn = driver.find_element(By.XPATH, cal_img_xpath)
    driver.execute_script("arguments[0].click();", img_btn)
    
    for val, lis in zip(['2022','2023','2024'], [lis1, lis2, lis3]): #zip(년, 월)
        for val2 in lis:
            # 달력 클릭
            temp = Select(driver.find_element(By.XPATH, year_xpath))
            temp.select_by_value(val)

            temp2 = Select(driver.find_element(By.XPATH, mon_xpath))
            temp2.select_by_value(val2)
            
            a_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "ui-state-default") or contains(@class, "ui-state-active")]')

            time.sleep(2)
            
            for i in range(len(a_elements)):
                a_elements[i].click()
                
                # 장애인 이용수
                temp = driver.find_element(By.XPATH, num_xpath).text
                temp2 = driver.find_element(By.XPATH, num2_xpath).text
                df.loc[num] = [val+str(int(val2)+1).zfill(2)+str(i+1).zfill(2), option, temp, temp2]
                num += 1
                # print(temp)
                
                # 달력 클릭
                img_btn = driver.find_element(By.XPATH, cal_img_xpath)
                driver.execute_script("arguments[0].click();", img_btn)

                time.sleep(3)
                
                a_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "ui-state-default") or contains(@class, "ui-state-active")]')
    
        df.to_csv(file_path + 'data.csv', index=False)
    time.sleep(3)
df.to_csv(file_path + 'data.csv', index=False)