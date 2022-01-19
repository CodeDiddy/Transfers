from cgitb import text
import imp
from tokenize import Name
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get("https://www.transfermarkt.nl")

driver.implicitly_wait(10)

# cookies = driver.get_cookies()
# print(len(cookies))
# print(cookies)

# driver.switch_to.active_element
# buttons = driver.find_elements(By.TAG_NAME, 'button')
# for button in buttons:
#     print(button)


# Omdat de privacy-voorwaarden in een Iframe worden weergegeven, lukte het mij niet om de 'accepteer-button' te vinden. Daarom middels het injecteren van javascript verwijder ik het hele Ifram
driver.execute_script("""
   var l = document.getElementById("sp_message_iframe_575848");
   l.parentNode.removeChild(l);
""")
