from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

baseURL = 'https://spotifycharts.com/regional/'


class SpotifyScrapper:

    def requestAndObtainTopSongs(self):
        driver = webdriver.Chrome(
            executable_path=r'C:\\webdrivers\\chromedriver.exe'
        )
        driver.get(baseURL + 'co/daily/2021-08-04')
        delay = 20
        try:
            flyTabs = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'chart-table')))
            generalDetails: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
            songsList = generalDetails.find('table', {'class': 'chart-table'}) \
                            .find_all('tr')[1:]

        except TimeoutException:
            print("Loading took too much time!")
            exit()


if __name__ == '__main__':
    SpotifyScrapper().requestAndObtainTopSongs()
