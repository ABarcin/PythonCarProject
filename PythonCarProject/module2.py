import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from flask import Flask,request
from flask import make_response
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

url = "https://www.cars.com/for-sale/searchresults.action"
browser=webdriver.Firefox()

@app.route('/cars/list', methods=['GET'])
def getFiftyCars():
    with requests.get(url) as res:
        if res.status_code == 200:
            info = dict()
            info["cars"] = []
            browser.get(url)
            trans=request.args.get('trans')
            brand=request.args.get('brand')
            extcolor=request.args.get('extcolor')
            year=request.args.get('year')
            if trans!=None:
                buttonTrans = browser.find_element(By.ID, "trigger_transmissions")
                time.sleep(2)
                buttonTrans.click()
                time.sleep(2)
                chcTran=browser.find_element(by=By.ID,value="panel_transmissions")
                chcTran=chcTran.find_elements(by=By.CLASS_NAME,value="sds-checkbox")
                
                for x in range(len(chcTran)):
                    value=chcTran[x].find_element(by=By.CLASS_NAME,value="sds-input")
                    value=value.get_attribute('value')
                    if value==trans:
                        label=chcTran[x].find_element(by=By.CLASS_NAME,value="sds-label")
                        time.sleep(2)
                        label.click()
                        time.sleep(2)

            if brand!=None:
                drp=browser.find_element(by=By.ID,value="make_select")
                drp=Select(drp)
                drp.select_by_value(brand)

            if extcolor!=None:
                buttonColors = browser.find_element(By.ID, "trigger_exterior_colors")
                time.sleep(2)
                buttonColors.click()
                chcColor=browser.find_element(by=By.XPATH,value="//*[@id=\"panel_exterior_colors\"]")
                chcColor=chcColor.find_elements(by=By.CLASS_NAME,value="sds-checkbox")
                for x in range(len(chcColor)):
                    value=chcColor[x].find_element(by=By.CLASS_NAME,value="sds-input")
                    value=value.get_attribute('value')
                    if value==extcolor:
                        label=chcColor[x].find_element(by=By.CLASS_NAME,value="sds-label")
                        time.sleep(2)
                        label.click()
                        time.sleep(2)

            if year!=None:
                yearSelect=Select(browser.find_element(by=By.ID,value="year_year_min_select"))
                time.sleep(1)
                yearSelect.select_by_value(year)
                time.sleep(2)
            if brand==None and trans==None and extcolor==None and year==None:
                drp=Select(browser.find_element(by=By.ID,value="pagination-dropdown"))
                drp.select_by_value("50")
                time.sleep(3)
                carCount=50
            else:
                element = browser.find_element(By.XPATH, "/html/body/section/div[2]/div[6]/div/div[4]/div[2]/div/span")
                carCounts=element.text
                carCount=carCounts.split(' ')[0]
                tryCarCountSplit=carCount.split(',')
                if len(tryCarCountSplit)>1:
                    carCount=tryCarCountSplit[0]+tryCarCountSplit[1]
                else:
                    carCount=carCount[0]
            if int(carCount)>49:
                carCount="45"

        for x in range(int(carCount)):
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
                try:
                    imgDiv=browser.find_element(by=By.ID,value="swipe-index-0")
                    car["img"]=imgDiv.get_attribute('src')
                except :
                    imgDiv=browser.find_element(by=By.CLASS_NAME,value="row-pic")
                    car["img"]=imgDiv.get_attribute('src')
                carColor=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/div[2]/section[1]/dl/dd[1]").text
                car["color"]=carColor
                carTrans=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/div[2]/section[1]/dl/dd[6]").text
                car["transmission"]=carTrans
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
                try:
                    imgDiv=browser.find_element(by=By.ID,value="swipe-index-0")
                    car["img"]=imgDiv.get_attribute('src')
                except :
                    imgDiv=browser.find_element(by=By.CLASS_NAME,value="row-pic")
                    car["img"]=imgDiv.get_attribute('src')

                basics=browser.find_element(by=By.CLASS_NAME,value="fancy-description-list")
                carAttributes=basics.text.split('\n')
                car["color"]=carAttributes[1]
                car["transmission"]=carAttributes[11]
                info["cars"].append(car)
    return info
if __name__ == '__main__':
    app.run(debug=True)