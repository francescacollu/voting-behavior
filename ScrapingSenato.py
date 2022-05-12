from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

senators_list = open('Senators_list.txt', 'r').read()
senators_list = senators_list.split('\n')
legislature='18'
folder = 'Senato_'+legislature
dirname = os.path.dirname(__file__)
path=os.path.join(dirname, folder)
if not os.path.exists(path):
    os.mkdir(folder)

for senator_name in senators_list:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://dati.senato.it/sito/votazioni?testo_generico=13&legislatura=18")
    driver.implicitly_wait(20)
    elem = driver.find_element_by_name("senatore")
    elem.clear()
    elem.send_keys(senator_name)
    listElements = driver.find_elements(By.XPATH, "//li[@class='ui-menu-item']//a")
    print("Total suggestions are: ", len(listElements))

    for ele in listElements:
        if ele.text == senator_name:
            print("Record found")
            ele.click()
            break

    button = driver.find_element(By.XPATH, "//input[@class='submit'][@name='commit'][@value='Cerca']")
    button.click()

    format_data = driver.find_element(By.XPATH, "//option[@value='csv']")
    format_data.click()

    download_button = driver.find_element(By.XPATH, "//input[@class='submit_search_btn'][@id='submit_search_btn_11']")
    download_button.click()
    print('Downloading '+ senator_name +"'s votes")
    time.sleep(10)
    while not os.path.isfile('/Users/francescacollu/Downloads/votazioni_senatore.csv'):
        time.sleep(10)
    os.rename('/Users/francescacollu/Downloads/votazioni_senatore.csv',path+'/votazioni_senatore_'+senator_name.strip(' ')+'.csv')
    driver.quit()
