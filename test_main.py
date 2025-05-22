import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
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

    import time
    import pytest
    from selenium import webdriver
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

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








