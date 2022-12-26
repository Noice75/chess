import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import json
import time
import bot
import threading

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:\\Users\\{self.user}\\AppData\\Local\\Google\\Chrome\\User Data")
driver = uc.Chrome(options=chrome_options)
b = []
bruh = None
game = True
played = 0
win = 0

def checkWin():
    global game
    global win
    global played
    while True:
        try:
            if(bruh in WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="header-title-component"]')))):
                win += 1
                played += 1
                with open('status.json','w') as file:
                    data = json.dumps({'win':win,'played':played,'lost':played-win},indent=4)
                    file.write(data)
                print(f'Wins = {win}, Lost = {played-win}, Played = {played}')
                game = False
            else:
                played += 1
                with open('status.json','w') as file:
                    data = json.dumps({'win':win,'played':played,'lost':played-win},indent=4)
                    file.write(data)
                print(f'Wins = {win}, Lost = {played-win}, Played = {played}')
                game = False
        except:
            pass
checkWinThread = threading.Thread(target=checkWin)
checkWinThread.start()

def getColor():
    try:
        WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"square-47")]')))[-1].click()
        WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"hint square-46")]')))
        WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"square-47")]')))[-1].click()
        color = 'white'
    except:
        color = 'black'
    print(color)
    return color

def start():
    global bruh
    driver.maximize_window()
    driver.get('https://www.chess.com/play/online/new')
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large ui_v5-button-full"]')))[0].click() #play
    while True:
        try:
            print(len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="user-tagline-rating user-tagline-white"]')))) > 1)
            if(len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="user-tagline-rating user-tagline-white"]')))) > 1):
                break
        except:
            continue
    bruh = getColor()
    bot.gameStart(bruh)
start()

def owo():
    hi = WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"highlight square-")]')))
    a = []
    for i in hi:
        a.append(i.get_attribute("class").split("-")[-1])
    if(len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"square-{a[0]}")]')))) > 1):
        print(f"Moved from {a[1]} to {a[0]} - player side")
        movedFrom = a[1]
        movedTo = a[0]
    else:
        print(f"Moved from {a[0]} to {a[1]} - player side")
        movedFrom = a[0]
        movedTo = a[1]
    return movedFrom,movedTo

def move(moveFrom,moveTo):
    print(f"Trying to move from {moveFrom} to {moveTo} - bot side")
    try:
        y = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"square-{moveFrom}")]')))[-1].click()
    except:
        WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="promotion-piece bq"]')))[-1].click()
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

while True:
    if(bruh == 'white'):
        a = owo()
        if(a != b):
            x = bot.move(a[0],a[1])
            move(x[0],x[1])
            b = a
    else:
        a = bot.owo()
        if(a != b):
            x = move(a[0],a[1])
            bot.move(x[0],x[1])
            b = a