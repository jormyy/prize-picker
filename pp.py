from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import datetime


URL = 'https://app.prizepicks.com/'

DRIVER = webdriver.Firefox()
DRIVER.get(URL)

PICKS = []

TODAY = datetime.datetime.now()
DAY_OF_WEEK = TODAY.strftime("%A")

DAY_HASH = {
    'Sun': 'Sunday',
    'Mon': 'Monday',
    'Tue': 'Tuesday',
    'Wed': 'Wednesday',
    'Thu': 'Thursday',
    'Fri': 'Friday',
    'Sat': 'Saturday'
}


def setup():
    while True:
        try:
            close_btn = DRIVER.find_element(By.CLASS_NAME, 'close')
            time.sleep(1)
            close_btn.click()
            break
        except NoSuchElementException:
            continue


def look_at_leagues():
    leagues_div = DRIVER.find_element(By.ID, 'scrollable-area')
    all_leagues = leagues_div.find_elements(By.CLASS_NAME, 'league')
    for league in all_leagues:
        league.click()
        
        time.sleep(1)
        
        league_dict = {}
        league_name = league.find_element(By.CLASS_NAME, 'name').text
        league_dict['league'] = league_name
        
        stats_div = DRIVER.find_element(By.CLASS_NAME, 'stat-container')
        all_stats = stats_div.find_elements(By.CLASS_NAME, 'stat')
        
        league_dict['stats'] = {}
        
        stat_names = []
        
        for stat in all_stats:
            stat_names.append(stat.text)
        
        for i in range(len(all_stats)):
            stats_div = DRIVER.find_element(By.CLASS_NAME, 'stat-container')
            stats = stats_div.find_elements(By.CLASS_NAME, 'stat')
            
            stats[i].click()
            # time.sleep(1)
            stat_name = stat_names[i]
            
            if stat_name == 'Popular 🔥':
                continue
            
            league_dict['stats'][stat_name] = {}
            
            players_div = DRIVER.find_element(By.ID, 'projections')
            all_players = players_div.find_elements(By.TAG_NAME, 'li')
            
            for player in all_players:
                player_name = player.find_element(By.TAG_NAME, 'h3').text
                
                line = None
                
                try:
                    player.find_element(By.CLASS_NAME, 'text-atlien-100').text
                    continue
                except NoSuchElementException:
                    line = player.find_element(By.CLASS_NAME, 'flex.flex-1.items-center.pr-2').text
                
                try:
                    player.find_element(By.CLASS_NAME, 'h-9.w-9.rotate-12')
                    continue
                except NoSuchElementException:
                    line = player.find_element(By.CLASS_NAME, 'flex.flex-1.items-center.pr-2').text
                
                league_dict['stats'][stat_name][player_name] = [line]
                
                other = {}
                
                team = player.find_element(By.ID, 'test-team-position').text.split()[0]
                other['team'] = team
                
                try:
                    player.find_element(By.CLASS_NAME, 'text-spottieOttie')
                    other['day'] = DAY_OF_WEEK
                except NoSuchElementException:
                    day = player.find_element(By.TAG_NAME, 'time').text.split()[-2]
                    other['day'] = DAY_HASH[day]
                
                img_div = player.find_element(By.TAG_NAME, 'picture')
                img = img_div.find_element(By.TAG_NAME, 'img')
                img_src = img.get_attribute('src')
                
                other['img_src'] = img_src
                
                league_dict['stats'][stat_name][player_name].append(other)
                    
        PICKS.append(league_dict)


def format_stats():
    out_file = open("picks.json", "w") 
    json.dump(PICKS, out_file, indent = 4) 
    out_file.close()
    
                             
setup()
look_at_leagues()
format_stats()
DRIVER.quit()