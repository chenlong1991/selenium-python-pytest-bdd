from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base import BasePage


class HomePage(BasePage):

    @property
    def PAGE_TITLE(self):
        return (By.TAG_NAME, 'h1')
    SUBHEADER = (By.TAG_NAME, 'h2')
    SUBPAGE_LINKS = (By.XPATH, '//*[@id="content"]/ul/li')

    def __init__(self, browser):
        self.browser = browser

    def get_page_title_text(self):
        return self.browser.find_element(*self.PAGE_TITLE).text

    def get_subheader_text(self):
        return self.browser.find_element(*self.SUBHEADER).text

    def get_subpage_list(self):
        links = self.browser.find_elements(*self.SUBPAGE_LINKS)
        titles = [link.text.split(" (")[0] for link in links]
        return titles