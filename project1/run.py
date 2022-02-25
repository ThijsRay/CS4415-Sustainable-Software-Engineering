from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from pyJoules.energy_meter import measure_energy
# import powertop

def main():
    use_adblocker = True
    browser = get_browser(use_adblocker)
    visit_nu(browser, use_adblocker)
    browser.quit()

def get_browser(use_ublock):
    return get_firefox(use_ublock)

def get_chromium(use_ublock):
    options = ChromiumOptions()
    if use_ublock:
        options.add_argument("load-extension=/home/katja/uBlock0.chromium")
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
    # Todo: fix correct DNS server
    options.set_preference("network.trr.mode", 2)
    options.set_preference("network.trr.custom_uri", "https://1.1.1.1")
    options.set_preference("network.trr.uri", "https://1.1.1.1")
    browser = webdriver.Firefox(options=options)
    if use_ublock:
        browser.install_addon("/home/katja/uBlock0_1.41.7b0.firefox.signed.xpi", temporary=True)
    browser.implicitly_wait(3)
    return browser


def visit_nu(browser, use_ublock):
    browser.get("https://nu.nl")
    # accept cookies
    wait = WebDriverWait(browser, 10)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='sp_message_iframe']")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[3]/button[1]"))).click()
    browser.switch_to.default_content()

    # Remove popup
    elem_path = "/html/body/div[11]/div[2]/div/div/i"
    if use_ublock:
        elem_path = "/html/body/div[10]/div[2]/div/div/i"
    wait.until(EC.element_to_be_clickable((By.XPATH, elem_path))).click()
    
    # Scroll through the page to load different elements
    for _ in range(15):
        ActionChains(browser).send_keys(Keys.PAGE_DOWN).pause(2).perform()

    # browser.get_full_page_screenshot_as_file("/tmp/nu_with_ads.png")

if __name__ == "__main__":
    main()
