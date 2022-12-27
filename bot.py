import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
import time

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
driver = uc.Chrome(options=chrome_options)
driver.get('https://www.chess.com/play/computer')
bruh = 'white'
WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large ui_v5-button-full"]')))[-1].click() #pannel

def start():
    driver.set_window_size(200, 1920)
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-cy="komodo1"]')))[-1].click()
    slider = WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class="slider-input"]')))[-1]
    s = 0
    while s < 12:
        try:
            slider.send_keys(Keys.RIGHT)
            s += 1
        except:
            continue
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large selection-menu-button"]')))[-1].click() #choose
    driver.maximize_window()
start()
def gameStart(color):
    global bruh
    bruh = color
    white = '//div[@data-cy="white"]'
    black = '//div[@data-cy="black"]'
    if(color == 'white'):
        WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, white)))[-1].click() #white
    elif(color == 'black'):
        WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, black)))[-1].click() #black
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-cy="Challenge"]')))[-1].click() #challenge
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large ui_v5-button-full"]')))[-1].click() #play
gameStart('white')
def owo():
    hi = WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"highlight square-")]')))
    a = []
    for i in hi:
        a.append(i.get_attribute("class").split("-")[-1])
    if(len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"square-{a[0]}")]')))) > 1):
        movedFrom = a[1]
        movedTo = a[0]
    else:
        movedFrom = a[0]
        movedTo = a[1]
    return movedFrom,movedTo

def move(moveFrom,moveTo):
    print(f"Trying to move from {moveFrom} to {moveTo} - bot side")
    try:
        WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"square-{moveFrom}")]')))[-1].click()
    except:
        if(bruh == 'white'):
            WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="promotion-piece bq"]')))[-1].click()
        else:
            WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="promotion-piece wq"]')))[-1].click()
    # for i in y:
    #     print(i.get_attribute("class").split())
    #     if("piece" in i.get_attribute("class").split()):
    #         i.click()
    #         break
    x = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"hint square-{moveTo}")]')))
    for i in x:
        print(i.get_attribute("class"), f'square-{moveTo}' in i.get_attribute("class"))
        if(f'square-{moveTo}' in i.get_attribute("class")):
            x = i
            break
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(x,5,5)
    action.click()
    action.perform()
    while owo() == (moveTo,moveFrom):
        continue
    while owo() == (moveFrom,moveTo):
        continue
    return owo()

def reset():
    try:
        WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@aria-label="Close"]')))[-1].click() #close win dialog
    except:
        pass
    try:
        WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@aria-label="Resign"]')))[-1].click() #resign
    except:
        pass
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-basic game-over-controls-buttonlg"]')))[-1].click() #newgame
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large selection-menu-button"]')))[-1].click() #choose


if(__name__ == '__main__'):
    start('white')
    time.sleep(1000)