from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from argparse import ArgumentParser

def main():
    sites = {
        "nu": visit_nu,
        "sparknotes": visit_sparknotes,
        "dw": visit_dw,
        "wikipedia": visit_wikipedia,
        "stackoverflow": visit_stackoverflow,
        "nytimes": visit_nytimes,
        "hackernews": visit_hn,
        "reddit": visit_reddit
    }

    browsers = {
        "firefox": get_firefox,
        "chromium": get_chromium,
    }

    parser = ArgumentParser(description='Run selenium tests with or without uBlock Origin')
    parser.add_argument('site', choices=sites.keys(), help="Which site to test")
    parser.add_argument('use_adblock', type=bool, help="Whether to use an adblocker")
    parser.add_argument('--repeat', default=1, type=int, help="How many times to repeat the test with the same browser instance")
    parser.add_argument('--browser', default="firefox", type=str, choices=browsers.keys(), help="The browser engine that will be used to run the tests. This defaults to Firefox.")
    args = parser.parse_args()
    
    browser = browsers[args.browser](args.use_adblock)
    for _ in range(args.repeat):
        sites[args.site](browser)
    browser.quit();

def get_chromium(use_ublock):
    options = ChromiumOptions()
    if use_ublock:
        options.add_argument("load-extension=/home/thijs/Projects/TU Delft/Sustainable/CS4415-Sustainable-Software-Engineering/project1/uBlock0.chromium")
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(3)
    return browser

def get_firefox(use_ublock):
    options = FirefoxOptions()
    options.set_preference("privacy.trackingprotection.cryptomining.enabled", False)
    options.set_preference("privacy.trackingprotection.enabled", False)
    options.set_preference("privacy.trackingprotection.fingerprinting.enabled", False)
    options.set_preference("privacy.trackingprotection.pbmode.enabled", False)
    options.set_preference("privacy.trackingprotection.annotate_channels", False)

    # Set the DNS server to cloudflares non-ad blocking DNS server
    options.set_preference("network.trr.mode", 3)
    options.set_preference("network.trr.custom_uri", "https://1.1.1.1/dns-query")
    options.set_preference("network.trr.uri", "https://1.1.1.1/dns-query")

    browser = webdriver.Firefox(options=options)
    if use_ublock:
        browser.install_addon("/home/thijs/Projects/TU Delft/Sustainable/CS4415-Sustainable-Software-Engineering/project1/uBlock0_1.41.5b2.firefox.signed.xpi", temporary=True)
    browser.implicitly_wait(3)
    return browser

def visit_nu(browser):
    browser.get("https://nu.nl")
    # accept cookies
    wait = WebDriverWait(browser, 10)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='sp_message_iframe']")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[3]/button[1]"))).click()
    browser.switch_to.default_content()

    # Remove popup
    wait.until(EC.any_of(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div[2]/div/div/i")),
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div[2]/div/div/i"))
    )).click()

    # Scroll through the page to load different elements
    for _ in range(13):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

    browser.get_full_page_screenshot_as_file("/tmp/nu_with_ads.png")

def visit_sparknotes(browser):
    browser.get("https://www.sparknotes.com/cs/")
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
    browser.execute_script('$("#onetrust-accept-btn-handler").click()')

    for _ in range(3):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()

    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

def visit_dw(browser):
    browser.get("https://www.dw.com")
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/a[2]'))).click()
    for _ in range(4):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()

    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

def visit_wikipedia(browser):
    browser.get("https://en.wikipedia.org/wiki/Main_Page")
    search = browser.find_element(By.ID, "searchInput")
    search.send_keys("TU Delft")
    search = browser.find_element(By.ID, "searchButton").click()
    for _ in range(7):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

def visit_stackoverflow(browser):
    browser.get("https://stackoverflow.com/questions/tagged/selenium")
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/button[1]'))).click()
    for _ in range(2):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

def visit_nytimes(browser):
    browser.get("https://nytimes.com")
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="GDPR-accept"]'))).click()
    for _ in range(12):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

def visit_hn(browser):
    browser.get("https://news.ycombinator.com")
    ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).pause(5).perform()

def visit_reddit(browser):
    browser.get("https://reddit.com")
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Accept all"]'))).click()
    for _ in range(10):
        ActionChains(browser).pause(5).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(browser).pause(5).send_keys(Keys.HOME).pause(5).perform()

if __name__ == "__main__":
    main()
