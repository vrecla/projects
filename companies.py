#This project aims to scrape all companies and its other details in a conference website using Selenium.

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
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://virtex.canadianminingexpo.com/exhibitor/list/page/16")


# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)  # Adjust the wait time as needed
    
# Function to close the signup page if it appears
def close_signup_page():
    try:
        close_button_xpath = '//*[@id="signup-div-inner-content-temp"]/div/div/div[2]/button'
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, close_button_xpath)))
        close_button.click()    
        print("Signup page closed")
    except Exception as e:
        print("No signup page to close or an error occurred: ", e)

# Initially wait and close the signup page if it appears
time.sleep(20)
close_signup_page()

article_list = []

# Start timer
start_time = time.time()
page_count = 0
article_count = 0


while True:

   # Wait for signup page to appear
    time.sleep(20)

    # Close the signup page if it appears
    close_signup_page()

    # Scroll to the bottom of the page
    scroll_to_bottom()
    
    # Find all articles
    articles = driver.find_elements(By.CLASS_NAME, 'procurement__item')
    article_count = len(articles)
    page_count += 1
    print(f"Page {page_count}: Current number of articles found: {len(articles)}")
    print(f"Current number of articles found: {len(articles)}")

    # Scrape the article names and tags
    for article in articles:
        try:
            info_container = article.find_element(By.CLASS_NAME, 'procurement__item-txt')
            link = info_container.find_element(By.TAG_NAME, 'a').get_attribute('href')
            company = info_container.find_element(By.TAG_NAME, 'a').text

            article_item = {
                'company': company,
                'link': link,
            }
                
            article_list.append(article_item)

        except Exception as e:
            print(f"An error occurred while processing an article: {e}")
    
    #click the next button at the bottom of the page to scrape articles in the next page
    try:
        next_button_container = driver.find_element(By.CLASS_NAME, 'card-footer.clearfix')
        ul_container= next_button_container.find_element(By.CLASS_NAME, 'pagination.pagination-sm.m-0.float-right')
        next_button = ul_container.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/main/div[4]/div[21]/ul/li[9]/a')
        close_signup_page()
        next_button.click()

    except Exception as e:
        print(f"No next button found or an error occurred: {e}")
        break

# End timer
end_time = time.time()
duration = end_time - start_time
print(f"Total time for loading all articles: {duration} seconds")

# Save the scraped data to a CSV file
csv_file = 'Exhibitor List.csv'
csv_columns = ['company', 'link']

try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        for article in article_list:
            writer.writerow(article)
except IOError:
    print("I/O error")


driver.quit()

#Last Run: Next button function do not work for other pages
