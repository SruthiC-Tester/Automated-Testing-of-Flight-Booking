import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestExpedia:

    @pytest.fixture()
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.expedia.com/")
        self.driver.maximize_window()

        print("❗ Waiting 30 seconds for you to manually solve CAPTCHA if any...")
        time.sleep(30)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "header-logo"))
            )
        except Exception:
            print("⚠️ Warning: Page didn't load expected elements.")

        yield self.driver
        self.driver.quit()

    def test_Expedia_Travel_site_loaded(self, setup):
        assert "Expedia Travel: Vacation Homes, Hotels, Car Rentals, Flights & More" in self.driver.title
        time.sleep(5)  # Keep this if you need to observe the page

    def test_wrong_expedia_Travel_site_loaded(self, setup):
        assert "Expedia Travel: Vacation Homes, Hotels, Car Rentals, Flights & More 1234" in self.driver.title
        time.sleep(5)  # Keep this if you need to observe the page

    def test_flight_search_full(self, setup):
        driver = setup
        wait = WebDriverWait(driver, 20)
        actions = ActionChains(driver)

        # Click on "Flights"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Flights"]'))).click()

        # Open "Leaving from" input
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Leaving from"]'))).click()

        # Type into the input box
        leaving_input = wait.until(EC.visibility_of_element_located((By.ID, "origin_select")))
        leaving_input.clear()
        actions.send_keys("a").pause(5).send_keys("b").pause(5).send_keys("u").perform()

        # Wait for buttons to be present in DOM
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))

        # Loop through all buttons to find the one with exact aria-label
        found = False
        for btn in driver.find_elements(By.TAG_NAME, "button"):
            label = btn.get_attribute("aria-label")
            if label == "Abu Dhabi (AUH - Abu Dhabi Intl.) United Arab Emirates":
                wait.until(EC.element_to_be_clickable(btn)).click()
                found = True
                break

        assert found, "❌ Abu Dhabi option not found."

        # Click and fill the "Going to" field
        going_to_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Going to"]')))
        going_to_button.click()

        # Input destination
        going_input = wait.until(EC.visibility_of_element_located((By.ID, "destination_select")))
        going_input.clear()
        going_input.send_keys("Kozhikode")

        # Wait for results to load
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
        time.sleep(2)

        # Select Kozhikode from dropdown
        found = False
        for btn in driver.find_elements(By.TAG_NAME, "button"):
            label = btn.get_attribute("aria-label")
            if label and "Kozhikode (CCJ - Calicut Intl.) India" in label:
                wait.until(EC.element_to_be_clickable(btn)).click()
                found = True
                break

        assert found, "❌ Kozhikode option not found."

        # Step 4: Select Travel Dates (Jun 28 - Aug 21, 2025)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Dates")]'))).click()

        # Select departure date: June 28, 2025
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div.uitk-month-double-left tr:nth-of-type(4) > td:nth-of-type(7) > div"
        ))).click()
        time.sleep(1)

        # Next month for return date
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div.uitk-cal-controls-button-next > button"
        ))).click()
        time.sleep(2)

        # Select return date: August 21, 2025
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div.uitk-month-double-right tr:nth-of-type(4) > td:nth-of-type(5) div.uitk-date-number"
        ))).click()
        time.sleep(1)

        # Confirm dates
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "footer button"))).click()
        time.sleep(1)

        # Step 5: Set Travelers (1 adult + 1 child, age 5)
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div:nth-of-type(3) div.uitk-field > button"
        ))).click()
        time.sleep(1)

        # Increase child count
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "section > div:nth-of-type(2) button:nth-of-type(2) svg"
        ))).click()
        time.sleep(1)

        # Set child age to 5
        age_dropdown_element = wait.until(EC.element_to_be_clickable((
            By.ID,
            "age-traveler_selector_children_age_selector-0"
        )))
        Select(age_dropdown_element).select_by_visible_text("5")
        time.sleep(1)

        # Done with traveler selection
        wait.until(EC.element_to_be_clickable((By.ID, "travelers_selector_done_button"))).click()
        time.sleep(2)

        print("✅ Test case executed successfully.")
