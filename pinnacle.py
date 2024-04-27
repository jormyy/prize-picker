import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Clear the terminal screen
print("\n" * 50)

# Configure ChromeDriver path and options
chrome_driver_path = "/Users/matthew/Documents/SeleniumDrivers/chromedriver_mac_arm64"
os.environ['PATH'] += os.pathsep + chrome_driver_path
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode
chrome_options.add_argument(f"exec-path={chrome_driver_path}")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.pinnacle.com/en/basketball/matchups/")
wait = WebDriverWait(driver, 10)

desired_team = "Denver Nuggets"
player_name = "Aaron Gordon"
player_prop = "Assists"
total_player_prop = player_name + " (" + player_prop + ")"
found_team = False
i = 1

while True and found_team is False:
    try:
        # Navigate back to main page for each iteration to refresh state
        driver.get("https://www.pinnacle.com/en/basketball/matchups/")
        
        # Check and click on the match
        parent_div_xpath = f'(//div[contains(@class, "style_row__yBzX8") and contains(@class, "style_row__12oAB")])[{i}]'
        parent_div = wait.until(EC.element_to_be_clickable((By.XPATH, parent_div_xpath)))
        teams = parent_div.find_elements(By.CLASS_NAME, "ellipsis.event-row-participant.style_participant__2BBhy")
        
        if any(desired_team in team.text for team in teams):
            # Find the link (a tag) and use its href to navigate
            link = parent_div.find_element(By.TAG_NAME, 'a')
            driver.get(link.get_attribute('href'))
            print(f"Navigated to {desired_team}'s match at index {i}")
            found_team = True
            
            # Click player props tab
            wait.until(EC.visibility_of_element_located((By.ID, "player-props")))
            player_props_button = driver.find_element(By.ID, "player-props")
            player_props_button.click()
            
            # Search for player prop
            try:
                props = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'style_marketGroups___6K0n matchup-market-groups')]")))
                for prop in props:
                    if total_player_prop in prop.text:
                        price = prop.find_element(By.CLASS_NAME, 'style_price__3Haa9').text
                        print(f"{total_player_prop}: {price}")

            except Exception as e:
                print(f"{player_name} {player_prop} props not found:", e)
        else:
            print(f"{desired_team} not playing in match {i}.")
        
        i += 1  # Increment to go to the next match
    except Exception as e:
        print(f"Error encountered: {e}")
        break

input("Press Enter to close the browser...")
driver.quit()
