import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://gorod.mos.ru/api/service/auth/auth"
USERNAME = ""
PASSWORD = ""
DOWNLOAD_PATH = 'C:\\Users\\adminmonitor\\Downloads'
CHROMEDRIVER_PATH = "C:/Users/adminmonitor/Downloads/chromedriver-win64/chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_PATH,
    "download.prompt_for_download": False,
})

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
    time.sleep(2)

try:
    driver.get(URL)
    username_field = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/form[1]/div[1]/div/div[1]/div')
    username_field.click()
    actions = ActionChains(driver)
    actions.move_to_element(username_field).click().send_keys(USERNAME).perform()

    password_field = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/form[1]/div[2]/div/div')
    password_field.click()
    actions.move_to_element(password_field).click().send_keys(PASSWORD).perform()

    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/form[1]/button')
    login_button.click()
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[3]/div/div[1]/div[2]/div/div[4]/div/div/div').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/aside/div/div[2]/div[4]/a/div[2]/div').click()
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div/div/div/form/div[2]/main/div[9]/div/div[3]/div/a[2]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/form/footer/button[3]/span[2]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div/div[4]/button[2]/span[2]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/aside/div/div[2]/div[6]/a/div[2]/div').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/form/footer/button[3]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div/div[4]/button[2]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[1]/aside/div/div[2]/div[4]/a/div[2]/div').click()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/div/form/div[2]/main/div[16]/div/div[3]/div/a[2]')
    scroll_to_element(driver, element)
    element.click()
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div/div/div/form/footer/button[3]/span[2]/span').click()
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div/div[4]/button[2]/span[2]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/header/div[1]/div[1]/div/div/span').click() ##Шапка Наш город
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[3]/div/div[1]/div[2]/div/div[6]/div/div/div').click()
    time.sleep(180)
    driver.find_element(By.XPATH,'//*[@id="q-app"]/div/div[2]/main/div/div[1]/div/div[2]/div[1]/table/tbody/tr[3]/td[5]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div[1]/div/div[2]/div[1]/table/tbody/tr[2]/td[5]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div[1]/div/div[2]/div[1]/table/tbody/tr[1]/td[5]').click()
    time.sleep(5)

finally:
    driver.quit()