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
driver.get("https://map.juniormininghub.com/news")

# Click the filter button for time
filter_time_xpath = '//*[@id="date-filter-selector"]'
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, filter_time_xpath))).click()


# Click "this year" option
this_year_option_xpath = '//*[@id="date-range-option-this-year"]'
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, this_year_option_xpath))).click()

# Click the search button for time filter
search_button_time_xpath = '//*[@id="date-filter-selector"]/div[2]/div[3]/button'
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, search_button_time_xpath))).click()

# Click the search box
search_box_xpath = '//*[@id="article-search"]'
search_box = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, search_box_xpath)))
search_box.click()

# Type "flow-through shares" in the search box
search_box.send_keys("flow-through shares")

# Click the first result
result_xpath = '//*[@id="article-search-dropdown-content"]/div[1]'
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, result_xpath))).click()

# Click the filters button
filters_button_xpath = '//*[@id="news-search-wrapper"]/div[2]/div/div[1]'
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, filters_button_xpath))).click()

# Click the country filter
country_filter_xpath = '//*[@id="filter-country"]'
country_filter = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, country_filter_xpath)))
country_filter.click()

# Type "Canada" in the country filter
country_filter.send_keys("USA")
# country_filter.send_keys("Canada")

# Select the resulting word
country_result_xpath = '//*[@id="country-search-dropdown-content"]/div'
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, country_result_xpath))).click()

# Click the search button for filters
# search_button_filters_xpath = '//*[@id="accept-filters"]'
# WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, search_button_filters_xpath))).click()
search_button = driver.find_element(By.XPATH,'//*[@id="accept-filters"]')
driver.execute_script("arguments[0].click();", search_button)

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)  # Adjust the wait time as needed

article_list = []

# Start timer
start_time = time.time()

# Scroll to load more articles until no more new articles are loaded
prev_article_count = 0


while True:
    # Scroll to the bottom of the page
    scroll_to_bottom()
    
    # Wait for new articles to load
    time.sleep(20)
    
    # Find all articles
    articles = driver.find_elements(By.CLASS_NAME, 'news-item')
    
    # Check if new articles are loaded
    if len(articles) == prev_article_count:
        break  # No more new articles loaded
    
    prev_article_count = len(articles)
    print(f"Current number of articles found: {len(articles)}")

    # Scrape the article names and tags
    for article in articles:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'news-title')
            title = title_element.text

            link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')

            tags_element = article.find_element(By.CLASS_NAME, 'news-date-and-tags-wrapper')
            tags_element_item = tags_element.find_element(By.CLASS_NAME, 'news-tags-container')

            company_name_element = tags_element.find_element(By.CLASS_NAME, 'company-miniquote-container')
            company_name = company_name_element.find_element(By.CSS_SELECTOR, '.qmod-segment.qmod-longname').text

            all_tags = tags_element_item.text
            
            date = tags_element.find_element(By.CLASS_NAME, 'news-date').text

            # Initialize variables with default values
            country = state = ''
            areas = types = commodities = []

            # Use try-except blocks for each tag to handle missing elements
            try:
                country = tags_element_item.find_element(By.CSS_SELECTOR, '.news-tags-item.country').text
            except:
                pass

            try:
                state = tags_element_item.find_element(By.CSS_SELECTOR, '.news-tags-item.state').text
            except:
                pass

            try:
                areas = [element.text for element in tags_element_item.find_elements(By.CSS_SELECTOR, '.news-tags-item.area')]
            except:
                pass

            try:
                types = [element.text for element in tags_element_item.find_elements(By.CSS_SELECTOR, '.news-tags-item.type')]
            except:
                pass

            try:
                commodities = [element.text for element in tags_element_item.find_elements(By.CSS_SELECTOR, '.news-tags-item.commodity')]
            except:
                pass

            article_item = {
                'title': title,
                'date': date,
                'company name': company_name,
                # 'project_name': '',
                # 'project_area': '',
                'country': country,
                'state': state,
                'area': '\n'.join(areas),
                'type': '\n'.join(types),
                'commodity': '\n'.join(commodities),
                'all_tags': all_tags,
                'link': link,
                # 'body': ''

            }
                
            article_list.append(article_item)

        except Exception as e:
            print(f"An error occurred while processing an article: {e}")

# Open each URL and scrape project details
# for article in article_list:
#     try:
#         driver.get(article['link'])
#         time.sleep(20)  # wait for the page to load
        
#         project_container = driver.find_element(By.ID, 'current-project')
#         project_name = project_container.find_element(By.XPATH, '//*[@id="current-project"]/div/a').text
#         project_area_container = driver.find_element(By.XPATH, '//*[@id="current-project"]/div').text
#         project_area = project_area_container.replace(project_name,'')

#         article['project_name'] = project_name
#         article['project_area'] = project_area

#         # article_container = driver.find_element(By.CLASS_NAME, 'news-item')
#         # article_body = article_container.find_element(By.CLASS_NAME, 'article-excerpt').text
#         # article['body'] = article_body

#     except Exception as e:
#         print(f"An error occurred while scraping project details for {article['link']}: {e}")


# End timer
end_time = time.time()
duration = end_time - start_time
print(f"Total time for loading all articles: {duration} seconds")

# Save the scraped data to a CSV file
csv_file = 'JMH_Articles_USA.csv'
# csv_file = 'JMH_Articles_Canada.csv'
csv_columns = ['title', 'date', 'company name', 'country', 'state', 'area', 'type', 'commodity', 'all_tags', 'link']

try:
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        for article in article_list:
            writer.writerow(article)
except IOError:
    print("I/O error")


driver.quit()


#LAST RUN: 226 seconds or 4 minutes for 3 articles --> 'USA', 'flow-through shares' with project details
#Estimated run for Canada: 1.8 hours (almost 2 hours lol)
#TO FIX: scraping includes previously loaded articles



#----old
# options = Options()
# options.add_experimental_option("detach", True)
      
# cService = webdriver.ChromeService("/Users/vanessarecla/chromedriver")
# driver = webdriver.Chrome(service = cService, options= options)

# driver.get("https://map.juniormininghub.com/articles")