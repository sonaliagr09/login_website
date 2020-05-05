from bs4 import BeautifulSoup as soup
import requests
import urllib.request
import pytesseract as tess
from PIL import Image
import time
import json

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#dummy_function_get_captcha()
def get_captcha():

    tess.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    im = Image.open('text1.png')
    captcha_text = tess.image_to_string(Image.open('text1.png'))
    return captcha_text


def login_to_website():
    url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    license_no = driver.find_element_by_xpath('//*[@id="form_rcdl:tf_dlNO"]')
    license_no.clear()
    license_no.send_keys('DL-0420110149646')
    dob = driver.find_element_by_xpath('//*[@id="form_rcdl:tf_dob_input"]')
    dob.clear()
    dob.send_keys('09-02-1976')
    captcha = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt34:CaptchaID"]')
    captcha.clear()
    a=input("enter captcha-")
    captcha.send_keys(a)
    driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt46"]/span').click()
    time.sleep(10)

    file= list()

    html = driver.execute_script("return document.documentElement.outerHTML")

    sel_soup = soup(html,'html.parser')

    table= sel_soup.find('table')
    table_rows= table.findAll('tr')
    for tr in table_rows:
        td = tr.findAll('td')
        temp= list()
        for i in td:
            temp.append(i.text)

        file.append(temp)
    final= dict()
    for j in file:
        final[j[0]] = j[1]

    json_object = json.dumps(final, indent = 5)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
login_to_website()
