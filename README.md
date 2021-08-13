[![Continuous Integration Status](https://github.com/mathare/selenium-python-pytest-bdd/actions/workflows/ci.yml/badge.svg)]https://github.com/mathare/selenium-python-pytest-bdd/actions)

# UI Testing with Selenium Python & Pytest BDD - Page Object Model

## Overview
This project provides an example for testing a UI with Selenium WebDriver, written in Python, using the Page Object Model design pattern and driven via BDD feature files through Pytest BDD. It can be used to kickstart testing of other UIs with minimal changes to the project.

NB This is not a complete implementation of a Selenium test suite for the target UI. It is an example of how to structure a Selenium test suite in Python but only a subset of the possible tests have been added.

**Disclaimer**: This project is largely a Python port of the [equivalent Selenium Java project](https://github.com/mathare/selenium-java-junit4). However, my Python isn't as good as my Java so this project isn't perfect. I will be working on improving it over time as my Python gets better.

## Why Use Selenium?
Selenium is an open-source framework for testing web applications that is probably de facto the framework most people think of when it comes to UI testing. It supports a multitude of browsers (Chrome, Firefox, Safari, IE/Edge) as well as all major languages (there are bindings for Java, Python, JavaScript, C# and Ruby) making it suitable for almost any UI testing project. It is also highly portable so works across Windows, macOS and Linux/Unix and of course being open-source is freeware. There is an extensive and active Selenium community offering support for users and helping to extend and develop Selenium, which is always a bonus.

## Web Application Under Test
The website that is being tested by this framework is “[the-internet](http://the-internet.herokuapp.com/)”, a third-party application that contains a number of different pages, each showcasing a different aspect of UI testing, and the challenges one can face when implementing such testing. It is often flagged up as an excellent candidate website for practicing automated testing, which is why I have chosen to use it here. It is simple to understand and get started with while still offering a realistic challenge.

Only a subset of the available functionality has been tested, focusing on the following pages:
* [home/main](http://the-internet.herokuapp.com/) page
* [Checkboxes](http://the-internet.herokuapp.com/checkboxes)
* [Dropdown](http://the-internet.herokuapp.com/dropdown)
* [Dynamic Controls](http://the-internet.herokuapp.com/dynamic_controls)
* [Form Authentication](http://the-internet.herokuapp.com/login)
  That is sufficient to provide a demonstration of the main interaction and verification methods in Selenium while keeping the project size small enough to act as a template.

## Test Framework
As stated above, this project contains a Selenium Python test framework, implements the Page Object Model design pattern and utilises Pytest BDD. As such, it follows test automation best practices. The Page Object Model means that each individual webpage has its own class, each containing the methods specific to controls on that page. Thus, each page is independent and separate from the tests, meaning any changes to the page are isolated to only the corresponding page class. This makes for code that is cleaner, easier to read and maintain, and contains less duplication. The use of Gherkin-style BDD means the tests themselves are also clean and clear, written in plain English, so they can be understood by anyone working with the project, including non-technical roles. Although this project is just an example of how to set up Selenium for UI testing in Python, in a real-life project the use of BDD is essential for collaboration between QAs, developers, and business roles (e.g. Product Owners, Business Analysts etc). Quality is everyone’s responsibility, which means the tests themselves need to be easily understood by all stakeholders.

### Tech stack
As this is a Python project, build and dependency management is handled by Pipenv, so there is a `Pipfile` (and associated `.lock` file) defining the versions of the dependencies:
* Python v3.8.1
* Selenium v3.141.59
* Pytest v6.2.4
* Pytest BDD v4.1.0
* [Sttable](https://github.com/aBulgakoff/sttable) v0.0.1
* Webdriver-Manager v3.4.2

The code is written in Python and built using v3.8.1. There are more up-to-date Pythons versions available - v3.9.6 being the latest at the time of writing. However, I used Python v3.8.1 (released 18th December 2019) as it is the version I am most used to and what was installed when I began this project.

The Selenium version is from November 2018 but is the latest Selenium v3 release and also the latest production release (all the v4 releases are currently alpha or beta).

I have chosen to use the latest Pytest release (v6.2.4, released May 2021) even though it is more recent than the Python version I am using. 

Similarly, I am using the latest Pytest BDD version (v4.1.0, released July 2021). Other BDD frameworks are available for Python (e.g. `behave`) but Pytest BDD is the one I am familiar with so seemed like the natural choice at this stage.

Sttable is a small plugin that adds simple support for data tables within BDD scenarios and feature files. This functionality is native to Cucumber (Java) but seemingly not in Pytest BDD so this additional plugin is required. I have used the latest version at the time of writing.

Webdriver-manager is a third-party plugin that makes it easier to manage the drivers for multiple browsers, making cross-browser testing simpler. It is similar to the extension I commonly use for Selenium Java projects. In this project I am using the latest version (from May 2021).

### Project Structure
The project uses a standard structure and naming convention (hopefully):
* `features`  - this folder contains the Gherkin `.feature` files, one per website page. By separating out the tests for each page into separate feature files we continue the Page Object Model theme of page independence and make it easier to extend the framework in the future. Each feature file is named after the page it tests, e.g. `checkboxes_page.feature` contains the tests for the Checkboxes page.
* `pages` - the Page Object Model implementation of the individual website pages, one class file per page. Each class is named after the corresponding page e.g. `HomePage`, `DropdownPage` etc. Note, the filenames match the page names and do not match the class names exactly. For example, the `HomePage` class in the `home.py` file. There is also a `BasePage` which the other page classes implement/extend through inheritence.
* `step_defs` - a collection of files containing the implementation of the steps from the BDD feature files. As above, there is one steps file per page and each is named after the page under test, e.g. `test_dynamic_controls_page_steps.py`. The filename starts with `test_` as the project uses Pytest and this prefix is required in order for Pytest to recognise this file as a test file (with Pytest/Pytest BDD it is the steps files rather than the features that are executed as each steps file is bound to a feature file via the `scenarios` keyword - see [Running tests](#running-tests)).
NB Unlike the Java equivalent, there is no Common Steps files containing step defintions that are used by more than one feature file. This means there is some duplication of code across individual steps files at this stage, in particular for verifying the page title as I have declared the related variable and method as abstract in the base page class, meaning each page must define these. This is required as the HTML tag for the page title varies from page to page. Deduplicating these steps is something I have yet to work out how to properly resolve in Python.
* `config.json` - a JSON object used to define certain configuration options such as the browser, whether to run headless and the implicit wait timeout.
* `conftest.py` - this is _roughly_ equivalent to the `CommonSteps.java` class from the Selenium Java version of this project. This file contains methods to set up the browser (having read in the required parameters from the `config.json` file) and make that available to the page methods. It also sets up a few methods required to fully utilise data tables in feature files. Finally, steps that are common across multiple feature files (with the exception of the page title steps noted above) are contained within this file.

### Page Object Model Classes
As noted above, the `pages` folder contains the relevant Page Object Model classes for each tested page. Each page class, including the abstract `BasePage` class, follows the same pattern:
* selector/locator tuples declared as pairs, the first element being the locator method (`By.ID`, `By.XPATH` etc) and the second element being the locator itself (i.e. the ID, xpath etc).
* interaction methods e.g. to click on an element, get an element’s text etc. These methods use the above locator tuples, passing them to `find_element` or `find_elements` calls
  
This way we encapsulate the web elements themselves, only allowing the interactions that have been implemented via our methods, ensuring the tests (in effect, the user) can only interact with the web page in known ways.

The `BasePage` class defines constants for the URL for each page, ensuring they are available to methods within each individual page class. Also declared in the base class are a some common locators for elements used on multiple pages to avoid the need to declare the locator in each page class (following the DRY principle). Interaction methods for the page header and footer are declared in the `BasePage` class too, again to reduce code duplication. In order to get round the fact that the title element on the tested pages doesn't use a consistent HTML tag or class, an abstract `get_page_title_text` method is declared in the `BasePage` class ensuring that each individual page class implements a method to get the text of the page title, using a `PAGE_TITLE` locator specific to whatever to that page’s HTML uses for the title.

Note there are no assertions in the page classes as assertions are a test action rather than a page action. Page interaction methods will return the result of that interaction, such as the attribute or text value, to the calling method in the test steps classes, so that it can be asserted as correct there. In other words, we maintain independence between the tests and the pages.

### Supported Browsers
The `conftest.py` module uses the Webdriver-Manager dependency to manage the various browser drivers. The `browser` Pytest fixture returns the relevant WebDriver instance for the chosen browser, with support for:
* Chrome - the default option
* Firefox

The browser to be used can be passed in via a Pytest command line parameter with a key of `browser`, defaulting to Chrome if no such property is specified. Alternatively, the `browser` parameter can be configured via the `config.json` file.

The `headless` pproperty is used to determine whether the browser should run in headless mode. Headless browsers are generally faster and consume fewer resources as they don’t actually render the webpages so are preferred when running automated UI tests. However, when debugging UI tests it is often easier to set this flag to false i.e. run “headed” so that issues with the tests can be more easily identified. `headless` is true by default but can be changed in the `config.json` file; it has not been enabled as a command line paramter at this stage.

The Webdriver-Manager plugin also has support for Edge, Opera and Internet Explorer but I have not enabled these options in this project at this stage.

### Running tests
The tests are easy to run as the project uses Pytest, so running the tests is as simple as running Pytest. As Pipenv is being used for dependency management this means running `pipenv run pytest` within the directory in which the repo has been cloned. The tests for an individual page can be run by passing the associated steps file as a parameter to the command, e.g. to run just the Checkboxes page tests `pipenv run pytest .\step_defs\test_checkboxes_page_steps.py`. Note that it is the steps file, rather than the feature file, which is specified. The steps file is bound to the corresponding feature via the `scenarios` keyword in the steps file, with the feature file path passed in as a parameter. The `browser` property can also be specified on the command line, e.g. `pipenv run pytest --browser Firefox` will run the test suite in Firefox.

NB Each test opens up in a separate browser instance (which is closed at the end of the test) so is not the fastest way to run a test suite, but it is the right way as we should ensure that tests are wholly independent of one another, do not share state and can run in any order. There are no `BeforeAll` and `AfterAll` hooks (that I am aware of), so we can’t open a single browser at the start of the test suite, navigate to the relevant page in the setup for each individual test scenario and close the browser at the end of the test suite. Having a separate browser per test also allows for test parallelisation which wouldn't otherwise be possible.

#### Test Reports
A report is generated for each test run as part of the GitHub Actions workflow (in the `Run tests` step). This is a simple report showing a list of the steps classes (each linked to a feature file) that have been executed and the overall result. In the event of a failing scenario, the details of the failure (actual versus expected result) are shown to allow easy debugging.

### CI Pipeline
This repo contains a CI pipeline implemented using [GitHub Actions](https://github.com/features/actions). Any push to the `main` branch or any pull request on the `main` branch will trigger the pipeline, which runs in a Linux VM on the cloud within GitHub. The pipeline consists of two separate jobs which run in parallel:
* `run-tests-on-chrome`
* `run-tests-on-firefox`
  
Each job checks out the repo then runs the test suite on Chrome/Firefox via `pipenv run pytest` or `pipenv run pytest --browser Firefox`. At the end of the steps the environment tears itself down and produces a [status report](https://github.com/mathare/selenium-python-pytest-bdd/actions).

In addition to the automated triggers above, the CI pipeline has a manual trigger actionable by clicking "Run workflow" on the [Continuous Integration](https://github.com/mathare/selenium-python-pytest-bdd/actions/workflows/ci.yml) page. This allows the user to select the branch to run the pipeline on, so tests can be run on a branch without the need for a pull request. This option is only visible if you are the repo owner.