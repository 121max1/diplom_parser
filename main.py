from selenium import webdriver
import time
import DbWorkerSaveResults as dbWorker
from selenium.webdriver.common.by import By

from Entities import Match, Set

driver = webdriver.Chrome()

driver.get("https://www.livesport.com/ru/tennis/rankings/wta/")
player_href_boxes = driver.find_elements(by=By.XPATH,
                                    value="//a[contains(concat(' ', normalize-space(@class), ' '), ' rankingTable__href ')]")
links = [elem.get_attribute('href') for elem in player_href_boxes]
for link in links:
    driver.get(link+"/results/")
    previous_amount = 0
    current_amount = len(driver.find_elements(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' event__match--twoLine ')]"))
    while current_amount != previous_amount:
        driver.find_element(by=By.XPATH, value="//a[contains(concat(' ', normalize-space(@class), ' '), ' event__more')]").click()
        time.sleep(1)
        previous_amount = current_amount
        current_amount = len(driver.find_elements(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' event__match--twoLine ')]"))
    matches_id_list = [elem.get_attribute('id').split("_")[-1] for elem in driver.find_elements(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' event__match--twoLine ')]")]
    for match_id in matches_id_list:
        if dbWorker.is_match_exists(match_id):
            continue
        match_to_save = None
        sets_to_save = []
        games_to_save = None
        game_units_to_save = None
        # Get scores of sets
        driver.get(f"https://www.livesport.com/ru/match/{match_id}/#match-summary/match-summary")
        first_player_match_result = int(driver.find_element(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' detailScore__wrapper')]/span[1]").text)
        second_player_match_result = int(driver.find_element(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' detailScore__wrapper')]/span[3]").text)
        number_of_sets = first_player_match_result + second_player_match_result
        first_player_match_result_by_set_dict = {}
        second_player_match_result_by_set_dict = {}
        for set_number in range(number_of_sets):
            set_fp_result = int(driver.find_element(by=By.XPATH, value=r'//div[@class="smh__part  smh__home smh__part--{set_number}"]'.format(set_number=set_number+1)).text[0])
            first_player_match_result_by_set_dict[set_number] = set_fp_result
        for set_number in range(number_of_sets):
            set_sp_result = int(driver.find_element(by=By.XPATH, value=r'//div[@class="smh__part  smh__away smh__part--{set_number}"]'.format(set_number=set_number+1)).text[0])
            second_player_match_result_by_set_dict[set_number] = set_sp_result

        # Get players id's for match table
        first_player_site_id_element = driver.find_element(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' duelParticipant__home')]/div[4]/div[2]/a")
        first_player_site_id = first_player_site_id_element.get_attribute('href').split("/")[-1]
        second_player_site_id_element = driver.find_element(by=By.XPATH, value="//div[contains(concat(' ', normalize-space(@class), ' '), ' duelParticipant__away')]/div[4]/div[1]/a")
        second_player_site_id = second_player_site_id_element.get_attribute('href').split("/")[-1]

        # Save match to db
        match_to_save = Match(first_player_site_id, second_player_site_id, match_id)
        for set_number in range(number_of_sets):
            won_player_id = None
            won_score_set = None
            lose_score_set = None
            if first_player_match_result_by_set_dict[set_number] > second_player_match_result_by_set_dict[set_number]:
                won_player_id = first_player_site_id
                won_score_set = first_player_match_result_by_set_dict[set_number]
                lose_score_set = second_player_match_result_by_set_dict[set_number]
            else:
                won_player_id = second_player_site_id
                won_score_set = second_player_match_result_by_set_dict[set_number]
                lose_score_set = first_player_match_result_by_set_dict[set_number]
            # Save set to db
            match_to_save.sets.append(Set(set_number))
            # sets_to_save.append.save_set(set_number + 1, match_db_id, won_player_id, won_score_set, lose_score_set)
            driver.get(f"https://www.livesport.com/ru/match/{match_id}/#match-summary/point-by-point/{set_number}")
            result_game_row_elements = driver.find_elements(by=By.XPATH, value="//div[@class='matchHistoryRow']")
            game_process_row_element = driver.find_elements(by=By.XPATH, value="//div[@class='matchHistoryRow__fifteens']")
            on_serve_player_id = None
            try:
                driver.find_element(by=By.XPATH,value="//*[@id='detail']/div[8]/div[2]/div[2]/div")
                on_serve_player_id = first_player_site_id
            except:
                on_serve_player_id = second_player_site_id
            for i in range(len(game_process_row_element)):
                current_game_process_row_element = game_process_row_element[i]
                current_result_string = ""
                for element in current_game_process_row_element.find_element(by=By.CLASS_NAME, value="matchHistoryRow__fifteen"):
                    current_result_string += element.text












