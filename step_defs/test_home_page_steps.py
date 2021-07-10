from pytest_bdd import scenarios, given, when, then, parsers
from pages.home import HomePage as page
from sttable import parse_str_table

scenarios('../features/home_page.feature')


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
