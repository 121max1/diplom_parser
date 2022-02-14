from selenium import webdriver
import time
import DbWorkerSaveResults as dbWorker
from selenium.webdriver.common.by import By

from Entities import Match, Set, GameUnit, Game, Stat

driver = webdriver.Chrome()

driver.get("https://www.livesport.com/ru/tennis/rankings/wta/")
time.sleep(2)
#player_href_boxes = driver.find_elements(by=By.XPATH,
#                                    value="//a[contains(concat(' ', normalize-space(@class), ' '), ' rankingTable__href ')]")
#links = [elem.get_attribute('href') for elem in player_href_boxes]
links = [f"https://www.livesport.com/ru/player/{player.name}/{player.site_id}" for player in dbWorker.get_players_name_and_ids()]
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
        try:
            if dbWorker.is_match_exists(match_id) or dbWorker.is_match_exists_in_bad_matches(match_id):
                continue
            match_to_save = None
            # Get scores of sets
            driver.get(f"https://www.livesport.com/ru/match/{match_id}/#match-summary/match-summary")
            if driver.find_elements(by=By.XPATH, value="//span[contains(concat(' ', normalize-space(@class), ' '), 'fixedHeaderDuel__detailStatus ')]")[0].text.__contains__("отказ"):
                continue
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

            stats = []
            for i in range(number_of_sets+1):
                driver.get(f"https://www.livesport.com/ru/match/{match_id}/#match-summary/match-statistics/{i}")
                time.sleep(0.5)
                first_serve_percentage_first_player = driver.find_element(by=By.XPATH, value="//div[contains(text(), '% первой подачи')]/../div[1]").text.replace("%","")
                first_serve_percentage_second_player = driver.find_element(by=By.XPATH, value="//div[contains(text(), '% первой подачи')]/../div[3]").text.replace("%","")
                percentage_points_won_on_serve_first_player = driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Выиграно на подаче')]/../div[1]").text.split(" ")[0].replace("%","")
                percentage_points_won_on_serve_second_player = driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Выиграно на подаче')]/../div[3]").text.split(" ")[0].replace("%","")
                percentage_points_won_on_receive_first_player = driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Выиграно на приеме')]/../div[1]").text.split(" ")[0].replace("%","")
                percentage_points_won_on_receive_second_player = driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Выиграно на приеме')]/../div[3]").text.split(" ")[0].replace("%","")
                stats.append(Stat(int(first_serve_percentage_first_player),
                                  int(first_serve_percentage_second_player),
                                  int(percentage_points_won_on_serve_first_player),
                                  int(percentage_points_won_on_serve_second_player),
                                  int(percentage_points_won_on_receive_first_player),
                                  int(percentage_points_won_on_receive_second_player)))
            # Save match
            match_to_save = Match(first_player_site_id, second_player_site_id, match_id)
            match_to_save.first_serve_percentage_first_player = stats[0].first_serve_percentage_first_player
            match_to_save.first_serve_percentage_second_player = stats[0].first_serve_percentage_second_player
            match_to_save.percentage_points_won_on_serve_first_player = stats[0].percentage_points_won_on_serve_first_player
            match_to_save.percentage_points_won_on_serve_second_player = stats[0].percentage_points_won_on_serve_second_player
            match_to_save.percentage_points_won_on_receive_first_player = stats[0].percentage_points_won_on_receive_first_player
            match_to_save.percentage_points_won_on_receive_second_player = stats[0].percentage_points_won_on_receive_second_player
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
                # Save set
                set_to_add = Set(set_number, won_player_id, won_score_set, lose_score_set)
                set_to_add.first_serve_percentage_first_player = stats[set_number+1].first_serve_percentage_first_player
                set_to_add.first_serve_percentage_second_player = stats[set_number+1].first_serve_percentage_second_player
                set_to_add.percentage_points_won_on_serve_first_player = stats[set_number+1].percentage_points_won_on_serve_first_player
                set_to_add.percentage_points_won_on_serve_second_player = stats[set_number+1].percentage_points_won_on_serve_second_player
                set_to_add.percentage_points_won_on_receive_first_player = stats[set_number+1].percentage_points_won_on_receive_first_player
                set_to_add.percentage_points_won_on_receive_second_player = stats[set_number+1].percentage_points_won_on_receive_second_player
                match_to_save.sets.append(set_to_add)
                driver.get(f"https://www.livesport.com/ru/match/{match_id}/#match-summary/point-by-point/{set_number}")
                time.sleep(0.5)
                result_game_row_elements = driver.find_elements(by=By.XPATH, value="//div[@class='matchHistoryRow']")
                game_process_row_element = driver.find_elements(by=By.XPATH, value="//div[@class='matchHistoryRow__fifteens']")
                on_serve_player_id = None
                player_on_serve_number = -1
                try:
                    driver.find_element(by=By.XPATH, value="//*[@id='detail']/div[8]/div[2]/div[2]/div")
                    on_serve_player_id = first_player_site_id
                    player_on_serve_number = 1
                except:
                    on_serve_player_id = second_player_site_id
                    player_on_serve_number = 2
                current_game_number = 1
                first_player_current_game_score = 0
                second_player_current_game_score = 0
                for i in range(len(game_process_row_element)):
                    current_game_process_row_element = game_process_row_element[i]
                    current_result_string = ""
                    for element in current_game_process_row_element.find_elements(by=By.CLASS_NAME, value="matchHistoryRow__fifteen"):
                        current_result_string += element.text
                    game_units_text = current_result_string.split(",")
                    game_units = []
                    for text_game_result in game_units_text:
                        game_result_text_array = text_game_result.replace(" ", "").split(":")
                        if game_result_text_array[0] == "A":
                            game_result_text_array[0] = "41"
                        if game_result_text_array[1] == "A":
                            game_result_text_array[1] = "41"
                        game_units.append(GameUnit(int(game_result_text_array[0]),int(game_result_text_array[1])))
                    player_game_won = 0
                    game_won_player_id = None
                    if game_units[-1].player1_score > game_units[-1].player2_score:
                        game_won_player_id = first_player_site_id
                        first_player_current_game_score += 1
                    else:
                        game_won_player_id = second_player_site_id
                        second_player_current_game_score += 1
                    match_to_save.sets[-1].games.append(Game(current_game_number,
                                                             game_won_player_id,
                                                             first_player_current_game_score,
                                                             second_player_current_game_score,
                                                             on_serve_player_id,
                                                             game_unit_list=game_units))
                    current_game_number += 1
                    if player_on_serve_number == 1:
                        on_serve_player_id = second_player_site_id
                        player_on_serve_number = 2
                    elif player_on_serve_number == 2:
                        on_serve_player_id = first_player_site_id
                        player_on_serve_number = 1

            dbWorker.save_match_entity(match_to_save)
        except Exception as e:
            try:
                dbWorker.add_to_bad_matches(match_id)
            except Exception as e:
                print(e)