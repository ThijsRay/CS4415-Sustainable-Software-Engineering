from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

options = FirefoxOptions()
options.set_preference("privacy.trackingprotection.cryptomining.enabled", False)
options.set_preference("privacy.trackingprotection.enabled", False)
options.set_preference("privacy.trackingprotection.fingerprinting.enabled", False)
options.set_preference("privacy.trackingprotection.pbmode.enabled", False)
options.set_preference("privacy.trackingprotection.annotate_channels", False)

options.set_preference("network.trr.mode", 2)
options.set_preference("network.trr.custom_uri", "https://1.1.1.1")
options.set_preference("network.trr.uri", "https://1.1.1.1")
browser = webdriver.Firefox(options=options)
browser.get("https://nu.nl")

browser.implicitly_wait(3)
accept_cookies = browser.find_elements(By.XPATH, "/html")
print(accept_cookies)
accept_cookies.click()

browser.get_full_page_screenshot_as_file("/tmp/nu_with_ads.png")
browser.quit();

#browser = webdriver.Firefox()
#browser.install_addon("/home/thijs/Projects/TU Delft/Sustainable/project1/uBlock0_1.41.5b2.firefox.signed.xpi", temporary=True)
#browser.get("https://nytimes.com")
#browser.get_full_page_screenshot_as_file("/tmp/nytimes_without_ads.png")
#browser.quit();
