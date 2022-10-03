import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import listdir
from os.path import isfile, join
import re
from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path=r"E:\chromedriver\chromedriver.exe")
driver.get("http://192.168.0.12/front/central.php")

komp_lista_wydan = [f for f in listdir('E:\glpi_scrap\protokoly_wydania') if isfile(join('E:\glpi_scrap\protokoly_wydania', f))]
print(komp_lista_wydan)
def login():
    inputLogin = driver.find_element(By.ID, "login_name")
    inputLogin.send_keys('glpi')
    inputPassword = driver.find_element(By.ID, "login_password")
    inputPassword.send_keys('glpi')
    inputSubmit = driver.find_element(By.NAME, 'submit')
    inputSubmit.submit()

def searchUser():
    inputUserName = driver.find_element(By.NAME, 'globalsearch')
    user_name = komp_lista_wydan[0]
    extract_user_name = re.search('_(.*)_', user_name)
    #print(user_name.group(1))
    inputUserName.send_keys(extract_user_name.group(1)) #wpisanie nazwiska
    driver.find_element(By.NAME, 'globalsearchglass').click() #wyszukanie użytkownika

    if (user_name[-5] == 'K'):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        users = soup.find('h2', string='Użytkownicy')
        number_of_users = users.find_next('tbody')
        if (len(number_of_users) == 1):
            driver.find_element(By.XPATH, '//*[contains(@id, "User")]').click()
            driver.find_element(By.XPATH, '//*[@id="ui-id-11"]').click() #Dokumenty
        else:
            print('Znaleziono co najmniej 2 użytkowników. Zweryfikuj. ' + '(' + extract_user_name.group(1) + ')')
            exit()

        driver.find_element(By.XPATH, '//*[@id="ui-id-6"]').click()




def clickHeader():
    time.sleep(1)
    header = driver.find_element(By.XPATH, '//*[contains(@id, "documentitem_form")]/table/tbody/tr[2]/td[2]/span/span[1]')
    header.click()

    time.sleep(1)
    header1 = driver.find_element(By.XPATH, '//*[contains(@id, "select2-dropdown_documentcategories_id")]/li[2]')
    header1.click()
def addDocument():
    upload_file = driver.find_element(By.NAME, 'filename[]')
    #upload_file = driver.find_element(By.XPATH, '//*[contains(@id, "fileupload")]')
    #upload_file.click()
    upload_file.send_keys(os.getcwd()+f"/protokoly_wydania/{komp_lista_wydan[0]}")

    #add_file = driver.find_element(By.NAME, 'add')
    #add_file.click()
login()
searchUser()
#clickHeader()
#addDocument()

