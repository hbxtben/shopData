#!/usr/bin/env python
# encoding: utf-8


from getdata import *


class ShopValue:
    def __init__(self):
        self.pageTool = PageData()
        self.hisTool = PageData()
        self.hisTool.makeCompile()

        self.webList = ['http://www.jd.com/', 'https://www.tmall.com/', 'https://www.amazon.cn/',
                        'http://www.suning.com/']

        self.xpathList = [
            [
                "//input[@clstag='h|keycount|2015|03a']",
                "//ul[@class='J_valueList v-fixed']",
                "//ul[@class='J_valueList v-fixed']/li/a",  # brand -text
                "//div[@class='gl-i-wrap']",
                "//div[@class='gl-i-wrap']/div[@class='p-name p-name-type-2']/a",  # Name -title
                "//div[@class='gl-i-wrap']/div[@class='p-commit']",  # Hot -text
                "//div[@class='gl-i-wrap']/div[@class='p-price']/strong",  # Fee -text
                "//div[@class='gl-i-wrap']/div[@class='p-img']/a",  # Url -href
                "//div[@class='gl-i-wrap']/div[@class='p-img']/a/img",  # Page -src
                "//button[@clstag='h|keycount|2015|03c']"  # 需要改成click
            ],
            [
                "//div[@class='s-combobox-input-wrap']/input",
                "//ul[@class='av-collapse row-2']",
                "//ul[@class='av-collapse row-2']/li/a",  # -text
                "//div[@class='product  ']",
                #天猫一号 Name 属性
                "//div[@class='product  ']/div/p[@class='productTitle']/a",  # -title
                "//div[@class='product  ']/div/p[@class='productStatus']/span",  # -text
                "//div[@class='product  ']/div/p[@class='productPrice']/em",  # -text
                "//div[@class='product  ']/div/div[@class='productImg-wrap']/a",  # -href
                "//div[@class='product  ']/div/div[@class='productImg-wrap']/a/img"  # -src
                #天猫二号 Name 属性
                "//div[@class='product  ']/div/div[@class='productTitle productTitle-spu']",  # -text
            ],
            [
                "//input[@id='twotabsearchtextbox']",
                "//div[@class='refinements']/ul[@id='ref_125596071']",
                # "//ul[@id='ref_125596071']/li",                                      #-text
                # "//ul[@id='s-results-list-atf']",
                "//a[@class='a-link-normal s-access-detail-page  a-text-normal']",  # -title
                # "//div[@class='a-row a-spacing-none']/span/a[@class='a-size-small a-link-normal a-text-normal']",   #-text
                "//span[@class='a-size-base a-color-price s-price a-text-bold']",  # -text
                "//div[@class='a-section a-spacing-none a-inline-block s-position-relative']/a",  # -href
                "//div[@class='a-section a-spacing-none a-inline-block s-position-relative']/a/img"  # src
            ],
            [
                "//input[@id='searchKeywords']",
                "//div[@class='brand-item brand-con']",
                "//div[@class='brand-item brand-con']/div/a",  # -text
                "//ul[@class='clearfix']",
                "//p[@class='sell-point']/a",  # -title
                "//p[@class='com-cnt']",  # -text
                "//p[@class='prive-tag']/em",  # -text
                "//div[@class='img-block']/a",  # -href
                "//div[@class='img-block']/a/img",  # -src
            ]
        ]
        self.shopName = [u"京东", u"天猫", u"亚马逊", u"苏宁易购"]

    def getValue(self,Key):
        resultData={}
        for shopIter in range(1):
            MidData = {}
            self.pageTool.driver.get(self.webList[shopIter])
            self.pageTool.driver.find_element_by_xpath(self.xpathList[shopIter][0]).send_keys(Key)
            if shopIter == 0:
                self.pageTool.driver.find_element_by_xpath(self.xpathList[shopIter][9]).click()
            else:
                self.pageTool.driver.find_element_by_xpath(self.xpathList[shopIter][0]).send_keys(Keys.RETURN)
            resultData[self.shopName[shopIter]] = ""


            #得到第一个商品的信息
            try:
                wait(self.pageTool.driver, 3).until(lambda theDriver: theDriver.find_element_by_xpath(self.xpathList[shopIter][3]).is_displayed())
            except Exception:
                print 11111
                resultData[self.shopName[shopIter]] = ""
                continue

            #天猫屎一样的布局 fuck
            if shopIter != 1:
                Name = self.pageTool.driver.find_element_by_xpath(
                    self.xpathList[shopIter][4]).text  # text
            else:
                try:
                    Name = self.pageTool.driver.find_elements_by_xpath(self.xpathList[shopIter][4])[0].text  # text
                except:
                    try:
                        Name = self.pageTool.driver.find_elements_by_xpath(self.xpathList[shopIter][9])[0].text
                    except:
                        resultData[self.shopName[shopIter]] = ""


            Hot = self.pageTool.driver.find_elements_by_xpath(
                self.xpathList[shopIter][5])[0].text  # text
            Fee = self.pageTool.driver.find_elements_by_xpath(
                self.xpathList[shopIter][6])[0].text  # float(text)
            Url = self.pageTool.driver.find_elements_by_xpath(
                self.xpathList[shopIter][7])[0].get_attribute("href")  # href
            Page = self.pageTool.driver.find_elements_by_xpath(
                self.xpathList[shopIter][8])[0].get_attribute("src")  # src

            # solve the history fee data problem
            try:
                if shopIter == 3:
                    hispat = self.hisTool.patterns['suning'].search(Url)
                    Url = hispat.group(1) + hispat.group(2)
            except AttributeError:
                pass

            hisData = self.hisTool.getHisData(Url)
            hisData = hisData if hisData != '' else ''

            MidData["goodsName"] = Name
            MidData["goodsFee"] = Fee
            MidData["goodsHis"] = hisData
            MidData["goodsPage"] = Page
            MidData["goodsHot"] = Hot
            MidData["goodsFrom"] = self.shopName[shopIter]

            resultData[self.shopName[shopIter]]=MidData
        result=json.dumps(resultData)
        print result


