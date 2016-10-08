#!/usr/bin/env python
# encoding: utf-8

from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import webdriver
import json
import MySQLdb as mysqldb
import re

db = mysqldb.connect("localhost","root","jiushi19870508","shopdata",charset='utf8')
cursor=db.cursor()
feePat=re.compile("\d+?\.\d+?")

def inserts(datalist):
    sql="INSERT INTO shop_book(bookname,author,fee,cls,bro,bookimg) VALUES ('%s','%s','%f','%s','%s','%s')" % (datalist[0],datalist[1],datalist[2],datalist[3],datalist[4],datalist[5])
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e:
        print e
        db.rollback()
    else:
        print "sql success~~~"

def OneBook(driver3,driver2,url):
    datalist = []
    driver2.get(url)

    try:
        Name = driver2.find_element_by_xpath("//span[@id='productTitle']").text  # text
        Author = driver2.find_element_by_xpath("//div[@id='byline']/span/a").text  # text
        Fee = driver2.find_element_by_xpath("//span[@class='a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P']").text  # text
        ClsElems = driver2.find_elements_by_xpath("//a[@class='a-link-normal a-color-tertiary']")  # 一共三个，最后一个是 ,text
        BroElems = driver2.find_elements_by_xpath("//div[@class='sims-fbt-checkbox-label']/a")  # text n个一起变成json

        Fee=feePat.search(Fee).group()
        Cls = ClsElems[2].text
        Bro = u""
        for i in range(len(BroElems)):
            Bro+=BroElems[i].text+u"@"

        driver3.get("")
    except Exception,e:
        print e
        return

    datalist.append(Name)
    datalist.append(Author)
    datalist.append(float(Fee))
    datalist.append(Cls)
    datalist.append(Bro)
    datalist.append(bookimg)

    inserts(datalist)
    print u"-------->" + Name

def getBook():
    driver1=webdriver.Chrome()
    driver2=webdriver.Chrome()
    driver3=webdriver.Chrome()
    driver1.get("https://www.amazon.cn/s/ref=amb_link_108929192_2?ie=UTF8&bbn=1826536071&rh=i%3Astripbooks%2Cn%3A658390051%2Cn%3A!2146619051%2Cn%3A!2146621051%2Cn%3A1826536071%2Cp_6%3AA1AJ19PSB66TGU&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-top-3&pf_rd_r=05AH7443MJYZ9E0TR4TJ&pf_rd_t=101&pf_rd_p=289163392&pf_rd_i=1835681071")

    for i in range(70):
        urlElements = driver1.find_elements_by_xpath("//div[@class='a-fixed-left-grid-col a-col-right']/div[@class='a-row a-spacing-small']/a")  # href
        for urlOption in urlElements:
            url=urlOption.get_attribute("href")
            OneBook(driver3,driver2,url)

        try:
            nextP=driver1.find_element_by_xpath("//a[@id='pagnNextLink']").get_attribute('href')
            driver1.get(nextP)
        except Exception:
            break

    driver1.quit()
    driver2.quit()



getBook()