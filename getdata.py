#!/usr/bin/env python
# encoding: utf-8

import selenium
import json
import re
import MySQLdb as mysqldb
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from datetime import date


class PageData:
    '''
    爬取页面内部的所需数据
    @getPageData()  返回x_args要求的数据序列
    @getPage() 返回页面的源代码
    @getHisPage 得到西帖网某件物品页面
    @getHisData 得到历史数据
    '''
    def __init__(self):
        self.driver=webdriver.PhantomJS()

    def __del__(self):
        self.driver.quit()

    # def getPageData(self,x_args,url=''):
    #     if url!='':
    #         self.driver.get(url)
    #     data=[]
    #     elements=self.driver.find_elements_by_xpath(x_args)
    #     for iter in elements:
    #         data.append(iter.text)
    #     return data

    def makeCompile(self):
        self.patterns={
            'dateStr' : re.compile(r"xAxis:(.*?)}",re.S|re.I),
            'feeStr' : re.compile(r"series:(.*?)}",re.S|re.I),
            'hisData' : re.compile(r"(\d{1,5}\.\d{1,3})"),
            'hisSides' : re.compile(r'id="bgc".*?(\d+?\.\d{2,3}?).+?(\d+?\.\d{2,3}?)',re.S|re.I),
            'http' : re.compile(r"http"),
            'suning' : re.compile(r"(.+?)\/\d*?(\/\d*?\.html).*?"),
        }
    def getHisPage(self,url):
        try:
            self.driver.get("http://www.xitie.com/")
            elem=self.driver.find_element_by_xpath("//input[@name='no']")
            elem.send_keys(url)
            elem.send_keys(Keys.RETURN)
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
            html=self.driver.page_source
        except Exception:
            html=''
        return html

    def getHisData(self,url):
        hisData=[]
        mainData=dict()
        html = self.getHisPage(url)
        try:
            dateStr=self.patterns['dateStr'].search(html).group()
            feeStr=self.patterns['feeStr'].search(html).group()
            dateData=self.patterns['hisData'].findall(dateStr)
            feeData=self.patterns['hisData'].findall(feeStr)
            sideData=self.patterns['hisSides'].search(html)
            topData={'top':sideData.group(1)}
            lowData={'low':sideData.group(2)}
            hisData.append(dateData)
            hisData.append(feeData)
            hisData.append(topData)
            hisData.append(lowData)
            hisData=json.dumps(hisData)
        except AttributeError:
            return ""
        else:
            return hisData


class DB:
    '''
    数据库类：
    insert(self,form,datalist)
    query(self,sql)
    '''
    #cursor()方法可获得操作游标,游标可进行执行sql语句等
    def __init__(self):
        self.db = mysqldb.connect("localhost","root","jiushi19870508","shopdata",charset='utf8')
        self.cursor = self.db.cursor()

    def inserts(self,datalist):
        sql="INSERT INTO shop_things(goodsName,goodsCls,goodsBrand,goodsFee,goodsHis,goodsPage,goodsHot,goodsFrom,datetime) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
            (datalist[0][0],datalist[0][1],datalist[0][2],datalist[0][3],datalist[0][4],datalist[0][5],datalist[0][6],datalist[0][7],datalist[0][8])
        for data in datalist[1:]:
            sql+=",('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
        self.query(sql)

    def query(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception,e:
            print e
            self.db.rollback()
        else:
            print "sql success~~~"+"\n"+"\n"

    def __del__(self):
        self.db.close()

def test():
    url="https://click.simba.taobao.com/cc_im?p=%C3%B1%D7%D3&s=1033133195&k=409&e=5gJM3hSe0FMqrgGTM5F4DTybKHT0GlD3F5wOPwzvpkUQz4KUb3GdnrMxVdffOCaj5cwJeAE4WQoC52jayUyPVZ0jwczOPRAp%2Bkyd%2Bt9sorIwUCE5d5Vl%2Bqu5%2FecpFHKVKDr95K5lYKHjr8uj%2FpZGRUVH4p304btcjN1QIfG%2FgqiymRJWDMFhQTWvgv9JbvXPp1s9JRhRTTCovVZckn6VvMi2KlehLP4XIKany4WihAU8kRaJIeD6%2B4uTDULK0s9uML%2Fr34dIBZHnTvBs2STfTdF0BoQvds%2BAk0r4AcqXk%2FoCJWfjKMoypEPMRxjLWImLaFhSkeaOKWHeHdATMBhHa%2FDeFwQKNclrV1CxYv1XaWmJwwBF5qvVVeh1adowqKWf%2B9zod3RqTen3omisrqsT0Q%3D%3D"
    pageTool=PageData()
    print pageTool.getHisData(url)
