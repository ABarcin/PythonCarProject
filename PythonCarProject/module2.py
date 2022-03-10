import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import json
from selenium.webdriver.common.by import By
from flask import Flask,request
from flask import make_response
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pprint

app = Flask(__name__)
url = "https://www.cars.com/for-sale/searchresults.action"

#Tek methodda ister parametre göndersin ister göndermesin multi yada filtresiz olarak tüm araçlar listelenebiliyor.
@app.route('/cars/list', methods=['get'])
def getFiftyCars():
    with requests.get(url) as res:
        if res.status_code == 200:
            Cars= []
            global title,brand,color,trans,img,year,price
            browser=webdriver.Firefox()
            browser.get(url)
            trans=request.args.get('trans') # requestte karşılık gelen parametre var ise alıyor
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
                    if value==trans.lower():
                        label=chcTran[x].find_element(by=By.CLASS_NAME,value="sds-label")
                        time.sleep(2)
                        label.click()
                        time.sleep(2)

            if brand!=None:
                drp=browser.find_element(by=By.ID,value="make_select")
                drp=Select(drp)
                drp.select_by_value(brand.lower())

            if extcolor!=None:
                buttonColors = browser.find_element(By.ID, "trigger_exterior_colors")
                time.sleep(2)
                buttonColors.click()
                chcColor=browser.find_element(by=By.XPATH,value="//*[@id=\"panel_exterior_colors\"]")
                chcColor=chcColor.find_elements(by=By.CLASS_NAME,value="sds-checkbox")
                for x in range(len(chcColor)):
                    value=chcColor[x].find_element(by=By.CLASS_NAME,value="sds-input")
                    value=value.get_attribute('value')
                    if value==extcolor.lower():
                        label=chcColor[x].find_element(by=By.CLASS_NAME,value="sds-label")
                        time.sleep(2)
                        label.click()
                        time.sleep(2)

            if year!=None:
                yearSelect=Select(browser.find_element(by=By.ID,value="year_year_min_select"))
                time.sleep(1) 
                yearSelect.select_by_value(year.lower())
                time.sleep(2) #time.sleep leri kaldırınca patlıyor kritik bölgeye al yada farklı bir yol bul
            if brand==None and trans==None and extcolor==None and year==None:
                drp=Select(browser.find_element(by=By.ID,value="pagination-dropdown"))
                drp.select_by_value("50")  #100 araçseçilince next butonu gelmiyor farklı bir yoldan çöz
                time.sleep(3)
                carCount=50
            else:
                carCount=50
            if int(carCount)>49:
                carCount="49" 

        for x in range(int(carCount)):
            car = dict()
            if x==0:
                browser.find_element(by=By.CLASS_NAME,value="vehicle-card-link").click()
                tempTitle=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[1]/h1").text
                title = tempTitle

                tempPrice=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[2]/span").text
                price = tempPrice

                titles=tempTitle.split(' ')
                brand = titles[1]

                year=titles[0]
                try:
                    imgDiv=browser.find_element(by=By.ID,value="swipe-index-0")   #çoğu araçta olmasına rağmen 360 derece foto eklenen araçlarda yok bu yüzden try kullanıldı
                    img=imgDiv.get_attribute('src')
                except :
                    imgDiv=browser.find_element(by=By.CLASS_NAME,value="row-pic")
                    img=imgDiv.get_attribute('src')
                carColor=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/div[2]/section[1]/dl/dd[1]").text
                color=carColor
                carTrans=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/div[2]/section[1]/dl/dd[6]").text
                trans=carTrans
                #car=Car(title, price,brand,color,trans,year,img)
                Cars.append([title, price,brand,color,trans,year,img])
            else:
                nextCLick=browser.find_element(by=By.CLASS_NAME,value="srp-carousel-next-link")
                time.sleep(1)
                try:
                    nextCLick.click()
                except :
                    return json.dumps(Cars)
                tempTitle=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[1]/h1").text
                title = tempTitle

                tempPrice=browser.find_element(by=By.XPATH,value="/html/body/section/div[5]/section/header/div[2]/span").text
                price = tempPrice

                titles=tempTitle.split(' ')
                brand = titles[1]

                year=titles[0]
                try:
                    imgDiv=browser.find_element(by=By.ID,value="swipe-index-0")
                    img=imgDiv.get_attribute('src')
                except :
                    imgDiv=browser.find_element(by=By.CLASS_NAME,value="row-pic")
                    img=imgDiv.get_attribute('src')

                basics=browser.find_element(by=By.CLASS_NAME,value="fancy-description-list")
                carAttributes=basics.text.split('\n')
                color=carAttributes[1]
                trans=carAttributes[11]
                #car=Car(title, price,brand,color,trans,year,img)
                Cars.append([title, price,brand,color,trans,year,img])

    return json.dumps(Cars)

@app.route('/cars/filters', methods=['get'])
def getCarFilters():
     with requests.get(url) as res:
        if res.status_code == 200:
            Filters= []
            browser=webdriver.Firefox()
            browser.get(url)
            brand=browser.find_element(by=By.ID,value="make_select")
            options = [x for x in brand.find_elements(by=By.TAG_NAME,value="option")]
            for element in options:
                Filters.append(element.get_attribute("value"))
            Filters.append("nextfilter")
            color=browser.find_element(by=By.ID,value="panel_exterior_colors")
            options = [x for x in color.find_elements(by=By.TAG_NAME,value="input")]
            for element in options:
                Filters.append(element.get_attribute("value"))
            Filters.append("nextfilter")
            trans=browser.find_element(by=By.ID,value="panel_transmissions")
            options = [x for x in trans.find_elements(by=By.TAG_NAME,value="input")]
            for element in options:
                Filters.append(element.get_attribute("value"))
            Filters.append("nextfilter")
            year=browser.find_element(by=By.ID,value="year_year_min_select")
            options = [x for x in year.find_elements(by=By.TAG_NAME,value="option")]
            for element in options:
                Filters.append(element.get_attribute("value"))
        browser.close()
        return json.dumps(Filters)

if __name__ == '__main__':
    app.run(debug=True)