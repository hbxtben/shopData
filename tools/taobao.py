#!/usr/bin/env python
# encoding: utf-8


def comment():
    url="http://item.jd.com/2608430.html#comments-list"
    comments=[]
    pageTool=PageData()
    pageTool.makePageChange(url)
    for i in range(6):
        try:
            wait(pageTool.driver,8).until(lambda the_driver:the_driver.find_element_by_xpath("//a[@href='#comment']").is_displayed())
        except Exception:
            break
        pageTool.makePageChange('',"//a[@href='#comment']")
        options=pageTool.getPageData("//div[@class='p-comment']")
        comments.extend(options)
        pageTool.makePageChange("//a[@class='ui-pager-next']")
    for i in comments:
        print i
    print len(comments)

def taobao():
    url="https://s.taobao.com/search?q=%E5%B8%BD%E5%AD%90&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20160911"
    datalist=[]
    pageTool=PageData()
    pageTool.makePageChange(url)
    for page in range(20):
        print "page %d" % page
        try:
            wait(pageTool.driver,3).until(lambda theDriver:theDriver.find_element_by_xpath("//div[@data-index='2']"))
        except Exception:
            print "no data"
            break
        try:
            #name.extend(pageTool.getPageData("//a[@class='J_ClickStat']"))
            #hotNum.extend(pageTool.getPageData("//div[@class='deal-cnt']"))
            #fee.extend(pageTool.getPageData("//div[@class='price g_price g_price-highlight']/strong"))
            optionsName=pageTool.driver.find_elements_by_xpath("//a[@class='J_ClickStat']")
            optionsHot=pageTool.driver.find_elements_by_xpath("//div[@class='deal-cnt']")
            optionsFee=pageTool.driver.find_elements_by_xpath("//div[@class='price g_price g_price-highlight']/strong")
            for i in range(len(optionsName)):
                data=[]
                data.append(optionsName[i].text.encode("utf-8"))
                data.append("帆布鞋")
                data.append(float(optionsFee[i].text))
                data.append(optionsHot[i].text.encode("utf-8"))
                data.append("淘宝")
                data.append(str(date.today()).encode("utf-8"))
                datalist.append(data)
