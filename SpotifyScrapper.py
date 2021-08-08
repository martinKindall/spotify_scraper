from typing import Iterator

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dataTypes.Song import Song

baseURL = 'https://spotifycharts.com/regional/'


class SpotifyScrapper:

    def requestAndObtainTopSongs(self) -> Iterator[Song]:
        driver = webdriver.Chrome(
            executable_path=r'C:\\webdrivers\\chromedriver.exe'
        )
        country = 'co'
        date = '2021-08-04'
        driver.get(baseURL + '{}/daily/{}'.format(country, date))
        delay = 20
        try:
            flyTabs = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'chart-table')))
            generalDetails: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
            songsList = generalDetails.find('table', {'class': 'chart-table'}) \
                            .find_all('tr')[1:]
            return map(
                lambda songRaw: self.parseSong(songRaw, country, date),
                songsList
            )

        except TimeoutException:
            print("Loading took too much time!")
            exit()

    def parseSong(self, songRaw: BeautifulSoup, country: str, date: str) -> Song:
        nameAndArtist = songRaw.find('td', {'class': 'chart-table-track'})
        name = nameAndArtist.find('strong').getText()
        artist = nameAndArtist.find('span').getText()
        position = songRaw.find('td', {'class': 'chart-table-position'}).getText()
        return Song(int(position), name, artist, date, country)


if __name__ == '__main__':
    songs = list(SpotifyScrapper().requestAndObtainTopSongs())
    import pdb; pdb.set_trace()
    print("hi")
