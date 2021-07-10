import pytest
import selenium.webdriver
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pytest_bdd import given, then, parsers
from pages.base import BasePage


@pytest.fixture
def config(scope='session'):

    BROWSERS = ['Chrome', 'Firefox']

    # Read config file
    with open('config.json') as config_file:
        config = json.load(config_file)

    # Assert values are acceptable
    assert config['browser'] in BROWSERS
    assert isinstance(config['headless'], bool)
    assert isinstance(config['implicit_wait'], int)
    assert config['implicit_wait'] > 0

    # Return config so it can be used
    return config


@pytest.fixture
def browser(config):

    # Initialize the WebDriver instance
    if config['browser'] == 'Chrome':
        opts = webdriver.ChromeOptions()
        if config['headless']:
            opts.add_argument('headless')
        b = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    elif config['browser'] == 'Firefox':
        opts = webdriver.FirefoxOptions()
        if config['headless']:
            opts.headless = True
        b = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(), options=opts)
    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    # Make call wait up to 10 seconds for elements to appear
    b.implicitly_wait(config['implicit_wait'])

    # Return the WebDriver instance for the setup
    yield b

    # Quit the WebDriver instance for the teardown
    b.quit()


@pytest.fixture
def datatable():
    return DataTable()


class DataTable(object):

    def __init__(self):
        pass

    def __str__(self):
        dt_str = ''
        for field, value in self.__dict__.items():
            dt_str = f'{dt_str}\n{field} = {value}'
        return dt_str

    def __repr__(self) -> str:
        return self.__str__()


@given(parsers.parse('I have navigated to the \'the-internet\' "{page_name}" page'), target_fixture='navigate_to')
def navigate_to(browser, page_name):
    BASE_URL = "https://the-internet.herokuapp.com"

    PAGE_URLS = {
        "home": BASE_URL + "/",
        "checkboxes": BASE_URL + "/checkboxes",
        "dropdown": BASE_URL + "/dropdown",
        "dynamic controls": BASE_URL + "/dynamic_controls",
        "form authentication": BASE_URL + "/login",
        "inputs": BASE_URL + "/inputs",
        "secure area": BASE_URL + "/secure"
    }
    url = PAGE_URLS.get(page_name.lower())
    browser.get(url)
    return url


@then(parsers.parse('a "{text}" banner is displayed in the top-right corner of the page'))
def verify_banner_text(browser, text):
    url = 'https://github.com/tourdedave/the-internet'
    assert text == BasePage(browser).get_github_fork_banner_text()
    assert url == BasePage(browser).get_github_fork_banner_link()
    styleAttrs = BasePage(browser).get_github_fork_banner_position().split(";")
    for attr in styleAttrs:
        if attr.startswith("position"):
            assert "absolute" == attr.split(": ")[1]
        if attr.startswith("top"):
            assert "0px" == attr.split(": ")[1]
        if attr.startswith("right"):
            assert "0px" == attr.split(": ")[1]
        if attr.startswith("border"):
            assert "0px" == attr.split(": ")[1]


@then(parsers.parse('the page has a footer containing "{text}"'))
def verify_footer_text(browser, text):
    assert text == BasePage(browser).get_page_footer_text()


@then(parsers.parse('the link in the page footer goes to "{url}"'))
def verify_footer_link_url(browser, url):
    assert url == BasePage(browser).get_page_footer_link_url()
