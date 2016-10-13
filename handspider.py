#!/usr/bin/env python
# encoding: utf-8


from getdata import *



class ShopData:
    def __init__(self):
        self.HisTool = PageData()
        self.HisTool.makeCompile()
        self.pageTool = PageData()
        self.dbengine = DB()
        print u"浏览器准备已完成～"

    def getPageData(self,clsIter,dataBrand,shopName,xpathList,shopID):
        datalist=[]
        try:
            wait(self.pageTool.driver, 2).until(
                lambda theDriver: theDriver.find_element_by_xpath(xpathList[3]).is_displayed())
        except Exception,e:
            if shopID == 3:
                try:
                    wait(self.pageTool.driver, 2).until(lambda theDriver: theDriver.find_element_by_xpath(xpathList[9]).is_displayed())
                except:
                    return
            else:
                print e,"not find the goods"
                return

        #get all the  node from the page
        #then get the data from node

        #解决天猫两类name问题
        optionsName=self.pageTool.driver.find_elements_by_xpath(xpathList[4])
        optionState=0
        if len(optionsName)==0 and shopID==1:
            optionsName=self.pageTool.driver.find_elements_by_xpath(xpathList[9])
        elif len(optionsName)==0 and shopID==3:
            optionsName = self.pageTool.driver.find_elements_by_xpath(xpathList[10])
            optionsHot = self.pageTool.driver.find_elements_by_xpath(xpathList[11])  # text
            optionsFee = self.pageTool.driver.find_elements_by_xpath(xpathList[12])  # float(text)
            optionsUrl = self.pageTool.driver.find_elements_by_xpath(xpathList[13])  # href
            optionsPage = self.pageTool.driver.find_elements_by_xpath(xpathList[14])  # src
            optionState=1
        if optionState==0:
            optionsHot = self.pageTool.driver.find_elements_by_xpath(xpathList[5])  # text
            optionsFee = self.pageTool.driver.find_elements_by_xpath(xpathList[6])  # float(text)
            optionsUrl = self.pageTool.driver.find_elements_by_xpath(xpathList[7])  # href
            optionsPage = self.pageTool.driver.find_elements_by_xpath(xpathList[8])  # src


        rangeNum=len(optionsName)
        rangeNum=rangeNum if rangeNum <= 25 else 25

        for item in range(rangeNum):
            data = []
            data.append(optionsName[item].text)
            data.append(clsIter)
            data.append(dataBrand)
            data.append(optionsFee[item].text)

            #解决西帖网url规则问题
            try:
                hisUrl = optionsUrl[item].get_attribute("href")
                if shopID==2:
                    hispat=self.HisTool.patterns['suning'].search(hisUrl)
                    hisUrl=hispat.group(1)+hispat.group(2)
            except AttributeError:
                pass

            hisData = self.HisTool.getHisData(hisUrl)
            data.append(hisData)

            if shopID==3:
                page=optionsPage[item].get_attribute('data-src')
            else:
                page=optionsPage[item].get_attribute('src')
            data.append(page)
            data.append(optionsHot[item].text)
            data.append(shopName)
            data.append(date.today())
            datalist.append(data)

            print("--------%d>%d   %s" % (item, rangeNum, optionsName[item].text))
        self.dbengine.inserts(datalist)


    #输入网站url，所有类别序列，电商名，xpath序列，电商序列标号
    def getClsData(self,weburl,clsIter,shopName,xpathList,shopID):
        self.pageTool.driver.get(weburl)
        self.pageTool.driver.find_element_by_xpath(xpathList[0]).send_keys(clsIter)
        if shopID==0:
            self.pageTool.driver.find_element_by_xpath(xpathList[9]).click()
        else:
            self.pageTool.driver.find_element_by_xpath(xpathList[0]).send_keys(Keys.RETURN)

        try:
            wait(self.pageTool.driver, 2).until(lambda theDriver: theDriver.find_element_by_xpath(
                xpathList[1]).is_displayed())
        except Exception:
            print shopName+"@"+clsIter+u" ERROR:找不到该类"
            return
        optionsBrand = self.pageTool.driver.find_elements_by_xpath(xpathList[2])
        optionsBrandNum = len(optionsBrand)
        optionsBrandNum = optionsBrandNum if optionsBrandNum<20 else 20

        print shopName+"@"+clsIter + u" has brand num:"+str(optionsBrandNum)

        #only god and me can know this code
        #now only god

        #从品牌列表中进入
        for brandIter in range(optionsBrandNum):
            try:
                wait(self.pageTool.driver, 1).until(lambda theDriver: theDriver.find_element_by_xpath(
                    xpathList[1]).is_displayed())

                #保存品牌页面
                if brandIter==0:
                    self.pageTool.driver.save_screenshot('brandPage.png')
                self.pageTool.driver.get_screenshot_as_file('brandPage.png')

                optionsBrand = self.pageTool.driver.find_elements_by_xpath(xpathList[2])
                dataBrand = optionsBrand[brandIter].text

                #检查数据库
                checksql = 'select * from shop_things where goodsFrom="' + shopName + '" and goodsCls="' + clsIter + '" and goodsBrand="' + \
                           dataBrand + '"'
                sqllong = self.dbengine.cursor.execute(checksql)
                if sqllong != 0:
                    print shopName + "@" + optionsBrand[brandIter].text + u" 已经存入数据库"
                    continue

                optionsBrand[brandIter].click()

                #解决Screenshot: available via screen问题
                self.pageTool.driver.save_screenshot('shopPage.png')
                self.pageTool.driver.get_screenshot_as_file('shopPage.png')

                print(shopName+"@"+clsIter+"@"+dataBrand + "@" + u"》》》 %d/%d" % (brandIter, optionsBrandNum))
            except Exception, e:
                print shopName+"@"+dataBrand+u"--品牌找不到"
                print e
                self.pageTool.driver.back()
                continue
            self.getPageData(clsIter, dataBrand, shopName, xpathList, shopID)
            self.pageTool.driver.back()


    def handSpider(self):
        clsA=[u"女",u"男"]
        #clsB=[u"春",u"夏",u"秋",u"冬天"]
        #clsC=[u"帽子",u"头巾",u"围巾",u"衬衫",u"卫衣",u"T恤",u"小西装",u"外套",u"风衣",u"毛衣",u"针织衫",u"皮衣",u"牛仔裤",u"短裤",u"长裤",u"牛分裤",u"哈伦裤",u"内衣",u"正装",u"睡衣"]
        clsD=[u"手机",u"键盘",u"硬盘",u"显卡",u"鼠标",u"手环",u"牙刷",u"指甲油",u"香水",u"洗发水",u"洗面奶",u"爽肤水",u"护手霜",u"牙膏",u"护发素",u"沐浴乳",u"裤袜",u"发带",u"长裙",u"短裙",u"超短裤",u"口红",u"眼线",u"面膜",u"纸抽",u"单反",u"平板电脑",u"粉底",u"身体乳",u"口罩",u"奶粉"]
        clsE=[u"钱包",u"靴子",u"眼镜",u"手链",u"旅行箱",u"双肩包",u"手表"] #男女
        clsF=[u"洗衣机",u"热水器",u"扫地机器人",u"电压力锅",u"面包机",u"吹风机",u"剃须刀",u"电视",u"空调",u"冰箱",u"微波炉",u"按摩椅",u"净水机",u"儿童文学",u"童话书",u"笔记本",u"显示器",u"手机充电线",u"手机壳",u"饮料",u"啤酒",u"白酒",u"皮带",]
        clsAll=[]
        clsAll.extend(clsD)
        clsAll.extend(clsF)
        for clse in clsE:
            for clsa in clsA:
                clsAll.append(clse+clsa)


        webList=['http://www.jd.com/','https://www.tmall.com/','http://www.suning.com/','https://www.taobao.com']
    
        xpathList=[
            [
                "//input[@clstag='h|keycount|2015|03a']",                           #搜索输入框
                "//ul[@class='J_valueList v-fixed']",
                "//ul[@class='J_valueList v-fixed']/li/a",                            #brand -text
                "//div[@class='gl-i-wrap']",
                "//div[@class='gl-i-wrap']/div[@class='p-name p-name-type-2']/a",   #Name -text
                "//div[@class='gl-i-wrap']/div[@class='p-commit']",                 #Hot -text
                "//div[@class='gl-i-wrap']/div[@class='p-price']/strong",           #Fee -text
                "//div[@class='gl-i-wrap']/div[@class='p-img']/a",                  #Url -href
                "//div[@class='gl-i-wrap']/div[@class='p-img']/a/img",              #Page -src
                "//button[@clstag='h|keycount|2015|03c']"                            #需要改成click
            ],
            #天猫
            [
                "//div[@class='s-combobox-input-wrap']/input",
                "//ul[@class='av-collapse row-2']",
                "//ul[@class='av-collapse row-2']/li/a",                              #-text
                "//div[@class='product  ']",
                "//div[@class='product  ']/div/div[@class='productTitle productTitle-spu']", #-text
                "//div[@class='product  ']/div/p[@class='productStatus']",            #-text
                "//div[@class='product  ']/div/p[@class='productPrice']/em",                #-text
                "//div[@class='product  ']/div/div[@class='productImg-wrap']/a",            #-href
                "//div[@class='product  ']/div/div[@class='productImg-wrap']/a/img",         #-src
                "//div[@class='product  ']/div/p[@class='productTitle']/a",                 #天猫 衣服  name
            ],
            # [
            #     "//input[@id='twotabsearchtextbox']",
            #     "//div[@class='refinements']/ul[@id='ref_125596071']",
            #     "//ul[@id='ref_125596071']/li",                                      #-text ###
            #     "//ul[@id='s-results-list-atf']",                                   ###
            #     "//a[@class='a-link-normal s-access-detail-page  a-text-normal']",   #-text
            #     "//div[@class='a-row a-spacing-none']/span/a[@class='a-size-small a-link-normal a-text-normal']",   #-text ###
            #     "//span[@class='a-size-base a-color-price s-price a-text-bold']",    #-text
            #     "//div[@class='a-section a-spacing-none a-inline-block s-position-relative']/a",  #-href
            #     "//div[@class='a-section a-spacing-none a-inline-block s-position-relative']/a/img" #src
            # ],
            [
                "//input[@id='searchKeywords']",
                "//div[@class='brand-item brand-con']",
                "//div[@class='brand-item brand-con']/div/a",                        #-text
                "//ul[@class='clearfix']",
                "//div[@class='res-info']/p[@class='sell-point']/a",                                        #-title
                "//div[@class='res-info']/p[@class='com-cnt']",                                             #-text
                "//div[@class='res-info']/p[@class='prive-tag']/em",                                       #-text
                "//div[@class='res-img']/div[@class='img-block']/a",                                        #-href
                "//div[@class='res-img']/div[@class='img-block']/a/img",                                    #-src
            ],
            #淘宝
            [
                "//input[@id='q']",
                "//div[@id='J_NavCommonRowItems_0']",
                "//div[@id='J_NavCommonRowItems_0']/a[@class='item icon-tag J_Ajax J_baikeiTrigger']",            #-text
                "//div[@class='item J_MouserOnverReq  ']",
                "//div[@class='item J_MouserOnverReq  ']/div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div[@class='row row-2 title']",  #-text
                "//div[@class='item J_MouserOnverReq  ']/div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div[@class='row row-1 g-clearfix']/div[@class='deal-cnt']",     #-text
                "//div[@class='item J_MouserOnverReq  ']/div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']/div[@class='row row-1 g-clearfix']/div[@class='price g_price g_price-highlight']", #-text
                "//div[@class='item J_MouserOnverReq  ']/div[@class='pic-box J_MouseEneterLeave J_PicBox']/div/div/a[@class='pic-link J_ClickStat J_ItemPicA']",  #-href
                "//div[@class='item J_MouserOnverReq  ']/div[@class='pic-box J_MouseEneterLeave J_PicBox']/div/div/a[@class='pic-link J_ClickStat J_ItemPicA']/img",    #data-src
                "//div[@class='grid-panel']",
                "//div[@class='grid-panel']/div[@class='info-cont']/div[@class='title-row ']",
                "//div[@class='grid-panel']/div[@class='info-cont']/div[@class='sale-row row']/div[@class='col end']",
                "//div[@class='grid-panel']/div[@class='info-cont']/div[@class='sale-row row']/div[@class='col']",
                "//div[@class='grid-panel']/div[@class='img-box']/a",
                "//div[@class='grid-panel']/div[@class='img-box']/a/img",
            ],
        ]

        shopName=[u"京东",u"天猫",u"苏宁易购",u"淘宝"]

        for clsIter in clsAll:
            for shopnumber in range(4):
                self.getClsData(webList[shopnumber],clsIter,shopName[shopnumber],xpathList[shopnumber],shopnumber)

if __name__ == '__main__':
    spider=ShopData()
    spider.handSpider()


