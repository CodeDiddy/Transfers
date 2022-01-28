from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup
import csv
import os
# import lxml


os.environ['WDM_LOG_LEVEL'] = '0'
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

def haal_transfers(jaar):
   try:
      driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
      # driver = webdriver.Firefox()

      # Ga naar webpagina
      driver.get(f"https://www.transfermarkt.nl/eredivisie/transfers/wettbewerb/NL1/plus/?saison_id={jaar}&s_w=&leihe=0&intern=0&intern=1")

      # Switch naar Iframe met privacy-voorwaarden, accept en terug naar main content
      driver.implicitly_wait(20)
      driver.switch_to.frame(driver.find_element(By.ID, 'sp_message_iframe_575848'))
      driver.implicitly_wait(20)
      driver.find_element(By.CSS_SELECTOR, '.sp_choice_type_11').click()
      time.sleep(3)
      driver.switch_to.default_content()
      time.sleep(3)

      player_list = []
      soup = BeautifulSoup(driver.page_source, 'lxml')
      overzicht = soup.find_all('div', class_='box')
      for club in overzicht:
         try:
            club_name = club.div.h2.a.string
            df = pd.read_html(club.prettify())
            for frame in df:               
               for index, rows in frame.iterrows():
                  temp_list = [jaar, club_name]
                  if rows['Aanwinst']:
                     temp_list.append(rows['Aanwinst'])
                     temp_list.append(rows['Vorige club.1'])
                  else:
                     continue
                  
                  temp_list.append(rows['Leeftijd'])
                  temp_list.append(rows['Pos'])
                  temp_list.append(rows['Afkoopsom'])

                  player_list.append(temp_list)
                  temp_list = []           
         except:
            continue
                      
      driver.close()
      with open('gegevens.csv', 'a') as f:
         writer = csv.writer(f)
         for player in player_list:
            writer.writerow(player)
   except:
      print("er is iets mis gegaan")
      driver.close()
      haal_transfers(jaar)


for jaar in range(2000, 2021):
   haal_transfers(jaar)
   print(f"Transfers toegevoegd voor seizoen {jaar}/{jaar + 1}") 
  