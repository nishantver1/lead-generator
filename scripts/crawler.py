from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
import random
import re


class Crawler:

    def __init__(self, email : str, password : str) -> 'Crawler':
        self.options = Options()
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
        self.options.add_argument("--start-maximized")

        self.service = ChromeService(executable_path=ChromeDriverManager().install(), options=self.options)

        self.driver = webdriver.Chrome(service=self.service)

        self.email = email
        self.password = password

    def __username(self, profileLink : str) -> str:
        linkParts = re.split("[/?]", profileLink)

        found = False
        index = 0

        while not found:
            if linkParts[index] == 'in':
                index += 1
                found = True
                break
            index += 1

        return linkParts[index]



    def crawl(self, companyName : str, departmentName : str, pageNum : int = 1) -> list:

        page_url = f"https://www.linkedin.com/search/results/people/?keywords={companyName}%20{departmentName}&origin=SWITCH_SEARCH_VERTICAL&searchId=ebd1073f-9fca-4df7-806d-4f1b64f5761c&page={pageNum}&sid=C5C"

        self.driver.get(page_url)

        if(pageNum == 1):
            username = self.driver.find_element(By.ID,"username")
            username.send_keys(self.email)

            password = self.driver.find_element(By.ID,"password")
            password.send_keys(self.password)

            submit = self.driver.find_element(By.CSS_SELECTOR,".from__button--floating")
            submit.click()

        profiles = []
        try:
            profile_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href^='https://www.linkedin.com/in/']")

            # Extract and print the href attributes
            for link in profile_links:
                cleanLink = f"https://www.linkedin.com/in/{self.__username(link.get_attribute("href"))}/"
                if cleanLink not in profiles:
                    profiles.append(cleanLink)
        except Exception as e:
            print(f"Error occurred: {e}")

        time.sleep(random.randint(1,3))
        return profiles

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    crawler = Crawler("devverma269@gmail.com","!R0nald0!")
    print(crawler.crawl("google","hr"))