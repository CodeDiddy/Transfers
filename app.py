from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup
# import lxml

# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# driver = webdriver.Firefox()
jaren = [2000]


# def haal_transfers(jaar):
#    try:
#       # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
#       driver = webdriver.Firefox()

#       # Ga naar webpagina
#       driver.get(f"https://www.transfermarkt.nl/eredivisie/transfers/wettbewerb/NL1/plus/?saison_id={jaar}&s_w=&leihe=0&intern=0&intern=1")

#       # Switch naar Iframe met privacy-voorwaarden, accept en terug naar main content
#       driver.implicitly_wait(20)
#       driver.switch_to.frame(driver.find_element(By.ID, 'sp_message_iframe_575848'))
#       driver.implicitly_wait(20)
#       driver.find_element(By.CSS_SELECTOR, '.sp_choice_type_11').click()
#       time.sleep(3)
#       driver.switch_to.default_content()
#       time.sleep(3)
#       # html = driver.page_source
#       html = pd.read_html(driver.page_source)
#       print(html)
      
#       with open('gegevens.txt', 'a') as f:
#          for df in html:
#             df.to_csv(f)
                
#       driver.close()
#       print("gelukt")
#    except:
#       print("er is iets mis gegaan")
#       driver.close()
#       haal_transfers(jaar)

def haal_transfers(jaar):
   try:
      # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
      driver = webdriver.Firefox()

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
      
      soup = BeautifulSoup(driver.page_source, 'lxml')
      overzicht = soup.find_all('div', class_='box')
      # print(overzicht)
      for club in overzicht[4:5]:
         try:
            club_name = club.div.h2.a.string
            df = pd.read_html(club.prettify())
            for frame in df:
               temp_list = [jaar, club_name]
               for index, rows in frame.iterrows():
                  if rows['Aanwinst']:
                     
                     temp_list.append('Inkomend')
                     temp_list.append(rows['Aanwinst'])
                     temp_list.append(club_name)
                     temp_list.append(rows['Vorige club.1'])
                  elif rows['Vertrokken speler']:
                     temp_list.append('Uitgaand')
                     temp_list.append(rows['Vertrokken speler'])
                     temp_list.append(rows['Nieuwe club.1'])
                     temp_list.append(club_name)
                  else:
                     temp_list.append(None)
                     temp_list.append(None)
                     temp_list.append(club_name)
                     temp_list.append(None)
                  
                  temp_list.append(rows['Leeftijd'])
                  temp_list.append(rows['Pos'])
                  temp_list.append(rows['Afkoopsom'])
               
               print(temp_list)
            
         except:
            print("DF niet kunnen printen")
            continue
     # df = pd.read_html(overzicht[0].prettify())
      # print(df)
                      
      driver.close()
      print("gelukt")
   except:
      print("er is iets mis gegaan")
      driver.close()
      haal_transfers(jaar)


for jaar in jaren:
   haal_transfers(jaar)
  