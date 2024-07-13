#This project aims to scrape all articles in a news website using Selenium.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import time

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver with the configured options
# Change state in the link to: southamerica/, centralamericacaribbean/
# Change keyword to: geothermal, ground+source+heat+pump, geothermal+heating+and+cooling
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.thinkgeoenergy.com/category/byregion/northamerica/?s=geothermal+heating+and+cooling")

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # Adjust the wait time as needed

article_list = []

# Start timer
start_time = time.time()

# Scroll to load more articles until no more new articles are loaded
prev_article_count = 0

while True:
    # Scroll to the bottom of the page
    scroll_to_bottom()
    
    # Wait for new articles to load
    time.sleep(10)
    
    # Find all articles
    articles = driver.find_elements(By.CLASS_NAME, 'content-post-items.col-sm-6.col-md-4.col-lg-4')
    
    prev_article_count = len(articles)
    print(f"Current number of articles found: {len(articles)}")

    for article in articles:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'thumbnail')
            title = title_element.find_element(By.CLASS_NAME, 'caption').text
            link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            date = title_element.find_element(By.CLASS_NAME, 'article-meta').text

            article_item = {
                'title': title,
                'link': link,
                'date': date,
            }
                
            article_list.append(article_item)

        except Exception as e:
            print(f"An error occurred while processing an article: {e}")

    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.next.page-numbers'))
        )
    
        # Scroll the next button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        
        # Click the next button
        next_button.send_keys('\n')

        time.sleep(5)

    except Exception as e:
        print(f"No next button found or an error occurred: {e}")
        break

# End timer
end_time = time.time()
duration = end_time - start_time
print(f"Total time for loading all articles: {duration} seconds")

# Save the scraped data to a CSV file
csv_file = 'ThinkGeoEnergy_Articles_NorthAmerica_GeothermalDrilling.csv'
# csv_file = 'ThinkGeoEnergy_Articles_SouthAmerica.csv'
# csv_file = 'ThinkGeoEnergy_Articles_CentralAmerica.csv'
csv_columns = ['date', 'title', 'link']

try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        for article in article_list:
            writer.writerow(article)
except IOError:
    print("I/O error")


driver.quit()

#Last Run: 45mins for 43 pages 


