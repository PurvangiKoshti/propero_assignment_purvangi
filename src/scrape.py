import time
import os
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScrapeBase:
    """
    A class for basic web scraping functionalities.
    """

    def __init__(self):
        """
        Initializes the ScrapeBase class.
        """
        self.driver = webdriver.Chrome()

    def logger(self, *args):
        """
        Logs messages along with the current time.

        Args:
            *args: Variable length argument list.
        """
        current_time = dt.datetime.now()
        readable_format = current_time.strftime("%Y-%m-%dT%H:%M:%S")
        print("[" + readable_format + "]", *args)

    def calculate_date_range(self, months_back):
        """
        Calculates the start and end date based on the specified number of months back.

        Args:
            months_back (int): Number of months back.

        Returns:
            tuple: A tuple containing start and end dates.
        """
        today = dt.date.today()
        start_date = today - dt.timedelta(days=30 * int(months_back))
        return start_date, today

    def request_to_url(self, url):
        """
        Requests the given URL.

        Args:
            url (str): The URL to request.
        """
        self.driver.get(url)
        self.logger("## Requested URL")

    def find_search_field(self):
        """
        Finds and clicks on the search button.
        """
        self.logger("## Clicking on search button")
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-button']"))
        ).click()
        self.logger("## Clicked on search Button")

    def input_search_field(self):
        """
        Inputs search query into the search field.
        """
        self.logger("## Searching input")
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='search-input']"))
        )
        search_input.send_keys(os.environ["SEARCH_INPUT"])

        go_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-submit']"))
        )
        go_button.click()

        self.logger("## Completed Searching")

    def input_date_range(self):
        """
        Inputs the date range for the search.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-date-dropdown-a']"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Specific Dates']"))
        ).click()

        start_date, end_date = self.calculate_date_range(os.environ["NUMBER_OF_MONTH"])

        start_date_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='DateRange-startDate']"))
        )
        end_date_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='DateRange-endDate']"))
        )

        self.logger("## Entering date")
        start_date_input.clear()
        start_date_input.send_keys(start_date.strftime("%m/%d/%Y"))

        end_date_input.clear()
        end_date_input.send_keys(end_date.strftime("%m/%d/%Y"))
        end_date_input.send_keys(Keys.ENTER)

    def load_full_content(self):
        """
        Loads the full content of the page by repeatedly clicking on the 'Show More' button.
        
        Returns:
            list: A list of items with full content loaded.
        """
        self.logger("## Loading a data by clicking on show more")
        while True:
            try:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-show-more-button']"))
                )
                show_more_button.click()
                time.sleep(1)
            except Exception as e:
                print("No more 'Show More' button to click or an error occurred:", e)
                break

        results_list = self.driver.find_element(By.CSS_SELECTOR, "ol[data-testid='search-results']")
        items = results_list.find_elements(By.TAG_NAME, "li")

        return items

    def extract_data(self, items):
        """
        Extracts relevant data from the items.

        Args:
            items (list): List of items to extract data from.

        Returns:
            list: A list of dictionaries containing extracted data.
        """
        data = []
        for item in items:
            try:
                title = item.find_element(By.CLASS_NAME, "css-2fgx4k").text
                date = item.find_element(By.CSS_SELECTOR, "[data-testid='todays-date']").get_attribute('aria-label')
                description = item.find_element(By.CLASS_NAME, "css-16nhkrn").text
                img_link = item.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
                anchor_link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                data.append({"title": title, "date": date, "description": description, "image_link": img_link,
                             "anchor_link": anchor_link})
            except Exception as e:
                continue

        self.driver.quit()

        return data
