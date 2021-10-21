from datetime import date
from typing import Iterator

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Utils
from dataTypes.Song import Song
from services.SongService import SongService

baseURL = 'https://spotifycharts.com/regional/'
#countryList = ['cl', 'co', 'ar', 'pe', 'pr', 'uy', 've', 'ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']
countryList = ['ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']


class SpotifyScrapper:

    def requestAndObtainTopSongs(self, country: str, date: str, driver) -> Iterator[Song]:
        driver.get(baseURL + '{}/daily/{}'.format(country, date))
        delay = 20
        try:
            WebDriverWait(driver, delay).until(
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
        name = nameAndArtist.find('strong').getText() \
            .replace("\"", "")\
            .strip()
        artist = nameAndArtist.find('span').getText()\
            .replace("by", "")\
            .replace("\"", "")\
            .strip()
        position = songRaw.find('td', {'class': 'chart-table-position'}).getText()
        return Song(int(position), name, artist, date, country)


if __name__ == '__main__':

    dateRange = Utils.generateMonthlyDateRange(date(2019, 1, 1), date(2021, 8, 1))
    driver = webdriver.Chrome(
        executable_path=r'C:\\webdrivers\\chromedriver.exe'
    )
    songService = SongService()
    for country in countryList:
        for dateObj in dateRange:
            songs = list(SpotifyScrapper().requestAndObtainTopSongs(
                country,
                dateObj.strftime("%Y-%m-%d"),
                driver
            ))
            for song in songs:
                songService.save(song)
