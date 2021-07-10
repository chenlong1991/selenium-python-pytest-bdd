from pytest_bdd import scenarios, when, then, parsers
from pages.home import HomePage as page
from sttable import parse_str_table
from pages.base import BasePage

scenarios('../features/home_page.feature')

@when(parsers.parse('I click on the "{page_name}" link'))
def click_page_link(browser, page_name):
    page(browser).click_page_link(page_name)

@then(parsers.parse('the page title is "{title}"'))
def verify_page_title(browser, title):
    assert title == page(browser).get_page_title_text()


@then(parsers.parse('the sub-header text is "{text}"'))
def verify_subheader_text(browser, text):
    assert text == page(browser).get_subheader_text()


@then(parsers.parse('a list of the following sub-pages is displayed\n{subpages}'))
def verify_subpage_list(browser, datatable, subpages):
    expected = parse_str_table(subpages)
    for field in expected.fields:
        assert expected.columns[field] == page(browser).get_subpage_list()

@then(parsers.parse('the "{page_name}" page opens'))
def verify_page_opens(browser, page_name, navigate_to):
    assert navigate_to == page(browser).get_current_url()
