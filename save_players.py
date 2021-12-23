from selenium import webdriver
import time
import DbWorkerSaveResults as dbWorker
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.livesport.com/ru/tennis/rankings/wta/")
time.sleep(10)
player_href_boxes = driver.find_elements(by=By.XPATH,
                                    value="//a[contains(concat(' ', normalize-space(@class), ' '), ' rankingTable__href ')]")
links = [elem.get_attribute('href') for elem in player_href_boxes]

for link in links:
    href_params = link.split("/")
    player_name = href_params[-2]
    player_site_id = href_params[-1]
    dbWorker.save_player(player_name, player_site_id)