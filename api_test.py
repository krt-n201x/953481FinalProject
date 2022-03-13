import time
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Edge



class ApiTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')

    def tearDown(self):
        self.driver.quit()

    def test_login(self):

        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/login")

        # Retrieve input elements
        email_input = self.driver.find_element(by=By.NAME, value='email')
        password_input = self.driver.find_element(by=By.NAME, value='password')

        # Populate inputs with dummy text
        email_input.send_keys('test@gmail.com')
        password_input.send_keys('test')
        time.sleep(3)

        # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='login-button')
        submit_button.click()
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/profile')

    def test_logout(self):

        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/login")

        # Retrieve input elements
        email_input = self.driver.find_element(by=By.NAME, value='email')
        password_input = self.driver.find_element(by=By.NAME, value='password')

        # Populate inputs with dummy text
        email_input.send_keys('test2@gmail.com')
        password_input.send_keys('test2')
        time.sleep(3)

        # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='login-button')
        submit_button.click()
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/profile')

        logout_button = self.driver.find_element(by=By.NAME, value='logout-button')
        logout_button.click()
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/')

    def test_register(self):

        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/signup")

        # Retrieve input elements
        email_input = self.driver.find_element(by=By.NAME, value='email')
        name_input = self.driver.find_element(by=By.NAME, value='name')
        password_input = self.driver.find_element(by=By.NAME, value='password')
        re_password_input = self.driver.find_element(by=By.NAME, value='re-password')

        # Populate inputs with dummy text
        email_input.send_keys('test2@gmail.com')
        name_input.send_keys('test2 test2')
        password_input.send_keys('test2')
        re_password_input.send_keys('test2')
        time.sleep(3)

        # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='signup-button')
        submit_button.click()
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/login')

    def test_search_food(self):
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/login")
        time.sleep(3)

        # Retrieve input elements
        email_input = self.driver.find_element(by=By.NAME, value='email')
        password_input = self.driver.find_element(by=By.NAME, value='password')

        # Populate inputs with dummy text
        email_input.send_keys('test2@gmail.com')
        password_input.send_keys('test2')
        time.sleep(3)

        # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='login-button')
        submit_button.click()

        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/profile')

        self.driver.get("http://127.0.0.1:5000/home")
        search_food_button = self.driver.find_element(by=By.NAME, value='search-food-name')
        search_food_button.click()
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/searcall')

        time.sleep(3)
        # Retrieve input elements
        food_name_input = self.driver.find_element(by=By.NAME, value='inputword')
        #
        # Populate inputs with dummy text
        food_name_input.send_keys('misobutter roast chicken with acorn squash panzanella')
        time.sleep(3)

        # # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='search-button')
        submit_button.click()
        time.sleep(3)

    def test_search_ingredients(self):
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/login")
        time.sleep(3)

        # Retrieve input elements
        email_input = self.driver.find_element(by=By.NAME, value='email')
        password_input = self.driver.find_element(by=By.NAME, value='password')

        # Populate inputs with dummy text
        email_input.send_keys('test2@gmail.com')
        password_input.send_keys('test2')
        time.sleep(3)

        # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='login-button')
        submit_button.click()

        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/profile')

        self.driver.get("http://127.0.0.1:5000/home")
        search_food_button = self.driver.find_element(by=By.NAME, value='search-food-ingredients')
        search_food_button.click()
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/searcall')

        time.sleep(3)
        # Retrieve input elements
        food_name_input = self.driver.find_element(by=By.NAME, value='inputword')
        #
        # Populate inputs with dummy text
        food_name_input.send_keys('chicken milk')
        time.sleep(3)

        # # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='search-button')
        submit_button.click()
        time.sleep(3)

    def test_favorite(self):
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/login")
        time.sleep(3)

        # Retrieve input elements
        email_input = self.driver.find_element(by=By.NAME, value='email')
        password_input = self.driver.find_element(by=By.NAME, value='password')

        # Populate inputs with dummy text
        email_input.send_keys('test2@gmail.com')
        password_input.send_keys('test2')
        time.sleep(3)

        # Find submit button and submit form by sending an "Enter" keypress
        submit_button = self.driver.find_element(by=By.NAME, value='login-button')
        submit_button.click()

        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/profile')

        self.driver.get("http://127.0.0.1:5000/home")
        time.sleep(3)

        search_food_button = self.driver.find_element(by=By.NAME, value='add-favorite-button')
        search_food_button.click()
        time.sleep(3)

        self.driver.get("http://127.0.0.1:5000/favorite")
        time.sleep(3)

        redirect_url = self.driver.current_url
        self.assertEqual(redirect_url, 'http://127.0.0.1:5000/favorite')

if __name__ == '__main__':
    unittest.main()