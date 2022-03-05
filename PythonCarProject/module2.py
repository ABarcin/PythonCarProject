import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pprint
from selenium.webdriver.common.by import By
url = "https://www.cars.com/for-sale/searchresults.action"
browser=webdriver.Firefox()

#first 50 cars
def firstFiveCars(url):
    with requests.get(url) as res:
        if res.status_code == 200:
            info = dict()
            info["cars"] = []
            browser.get(url)
            drp=Select(browser.find_element(by=By.ID,value="pagination-dropdown"))
            drp.select_by_index(4)
            time.sleep(2)
            lists=browser.find_elements(by=By.CSS_SELECTOR,value=".vehicle-card")
            carCount=50
    return getCars(info,carCount)
#cars = firstFiveCars(url)

def getCarsByBrand(brand=None,extcolor=None,tans=None,year=None):
    with requests.get(url) as res:
        if res.status_code == 200:
            info = dict()
            info["cars"] = []
            browser.get(url)
            if brand!=None:
                drp=browser.find_element(by=By.ID,value="make_select")
                drp=Select(drp)
            drp.select_by_value(brand)

            time.sleep(1)
            carCounts=browser.find_element(by=By.XPATH,value="/html/body/section/div[2]/div[6]/div/div[4]/div[2]/div/span").text
            carCount=carCounts.split(' ')[0]
            carCount=carCount.split(',')
            if len(carCount)>1:
                carCount=carCount[0]+carCount[1]
    return getCars(info,carCount)

def getCars(info,carCount):
    if int(carCount)>10:
        for x in range(2):
            car = dict()
            if x==0:
                browser.find_element(by=By.CLASS_NAME,value="vehicle-card-link").click()
                title=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[1]/h1").text
                car["title"] = title

                price=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[2]/span").text
                car["price"] = price

                titles=title.split(' ')
                car["brand"] = titles[1]

                car["modelYear"]=titles[0]

                imgDiv=browser.find_element(by=By.ID,value="swipe-index-0")
                car["img"]=imgDiv.get_attribute('src')

                basics=browser.find_element(by=By.CLASS_NAME,value="fancy-description-list")
                carAttributes=basics.text.split('\n')
                car["color"]=carAttributes[1]
                car["transmission"]=carAttributes[11]
                info["cars"].append(car)
            else:
                browser.find_element(by=By.CLASS_NAME,value="srp-carousel-next-link").click()
                title=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[1]/h1").text
                car["title"] = title

                price=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[2]/span").text
                car["price"] = price

                titles=title.split(' ')
                car["brand"] = titles[1]

                car["modelYear"]=titles[0]

                imgDiv=browser.find_element(by=By.ID,value="swipe-index-0")
                car["img"]=imgDiv.get_attribute('src')

                basics=browser.find_element(by=By.CLASS_NAME,value="fancy-description-list")
                carAttributes=basics.text.split('\n')
                car["color"]=carAttributes[1]
                car["transmission"]=carAttributes[11]
                info["cars"].append(car)
        return info
cars=getCarsByBrand(brand="bmw")
pprint.pprint(cars)