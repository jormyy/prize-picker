from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


URL = 'https://app.prizepicks.com/'

DRIVER = webdriver.Firefox()
DRIVER.get(URL)

PICKS = []


def setup():
    while True:
        try:
            close_btn = DRIVER.find_element(By.CLASS_NAME, 'close')
            time.sleep(1)
            close_btn.click()
            break
        except NoSuchElementException:
            continue


def look_at_sports():
    sports_div = DRIVER.find_element(By.ID, 'scrollable-area')
    all_sports = sports_div.find_elements(By.CLASS_NAME, 'league')
    
    for sport in all_sports:
        sport.click()
        
        time.sleep(1)
        
        sport_dict = {}
        sport_name = sport.find_element(By.CLASS_NAME, 'name').text
        sport_dict['sport'] = sport_name
        
        stats_div = DRIVER.find_element(By.CLASS_NAME, 'stat-container')
        all_stats = stats_div.find_elements(By.CLASS_NAME, 'stat')
        
        sport_dict['stats'] = {}
        
        stat_names = []
        
        for stat in all_stats:
            stat_names.append(stat.text)
        
        for i in range(len(all_stats)):
            stats_div = DRIVER.find_element(By.CLASS_NAME, 'stat-container')
            stats = stats_div.find_elements(By.CLASS_NAME, 'stat')
            
            stats[i].click()
            # time.sleep(1)
            stat_name = stat_names[i]
            print(stat_name)
            
            if stat_name == 'Popular 🔥':
                continue
            
            sport_dict['stats'][stat_name] = {}
            
            players_div = DRIVER.find_element(By.ID, 'projections')
            all_players = players_div.find_elements(By.TAG_NAME, 'li')
            
            for player in all_players:
                player_name = player.find_element(By.TAG_NAME, 'h3').text
                
                line = None
                
                try:
                    line = player.find_element(By.CLASS_NAME, 'text-atlien-100').text
                except NoSuchElementException:
                    line = player.find_element(By.CLASS_NAME, 'flex.flex-1.items-center.pr-2').text
                
                if player_name in sport_dict['stats'][stat_name]:
                    sport_dict['stats'][stat_name][player_name].append(line)
                else:
                    sport_dict['stats'][stat_name][player_name] = [line]
                    
        PICKS.append(sport_dict)
        break
            
        
        # for stat in all_stats:
        #     stat.click()
        #     stat_name = stat.text
        #     print(stat_name)
            
        #     if stat_name == 'Popular 🔥':
        #         continue
            
        #     # stat.click()
            
        #     sport_dict['stats'][stat_name] = {}
            
        #     players_div = DRIVER.find_element(By.ID, 'projections')
        #     all_players = players_div.find_elements(By.TAG_NAME, 'li')
            
        #     for player in all_players:
        #         player_name = player.find_element(By.TAG_NAME, 'h3').text
                
        #         line = None
                
        #         try:
        #             line = player.find_element(By.CLASS_NAME, 'text-atlien-100').text
        #         except NoSuchElementException:
        #             line = player.find_element(By.CLASS_NAME, 'flex.flex-1.items-center.pr-2').text
                
        #         if player_name in sport_dict['stats'][stat_name]:
        #             sport_dict['stats'][stat_name][player_name].append(line)
        #         else:
        #             sport_dict['stats'][stat_name][player_name] = [line]
        
        PICKS.append(sport_dict)
                    
                    
setup()
look_at_sports()
out_file = open("pick.json", "w") 
json.dump(PICKS, out_file, indent = 6) 
out_file.close()
DRIVER.quit()