from cgitb import text
from email import header
import imp
from operator import index
from select import select
from tokenize import Name
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import time
import pandas as pd
# import lxml

# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

driver = webdriver.Firefox()
jaren = [2000]


def haal_transfers(jaar):
   try:
      # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
      driver = webdriver.Firefox()

      # Ga naar webpagina
      driver.get(f"https://www.transfermarkt.nl/eredivisie/transfers/wettbewerb/NL1/plus/?saison_id={jaar}&s_w=&leihe=0&intern=0&intern=1")

      # Switch naar Iframe met privicy-voorwaarden, accept en terug naar main content
      driver.implicitly_wait(20)
      driver.switch_to.frame(driver.find_element(By.ID, 'sp_message_iframe_575848'))
      driver.implicitly_wait(20)
      driver.find_element(By.CSS_SELECTOR, '.sp_choice_type_11').click()
      time.sleep(3)
      driver.switch_to.default_content()
      time.sleep(3)
      # html = driver.page_source
      html = pd.read_html(driver.page_source)
      print(html)
      
      with open('gegevens.txt', 'a') as f:
         for df in html:
            df.to_csv(f)
                
      driver.close()
      print("gelukt")
   except:
      print("er is iets mis gegaan")
      driver.close()
      haal_transfers(jaar)


for jaar in jaren:
   haal_transfers(jaar)
  