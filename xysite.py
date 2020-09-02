#!/usr/bin/env python
#coding:utf-8
#pip install requests
import sys,os,re,requests,time,json
from threading import Thread

def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            file_body = f.read()
        return file_body
    else:
        return None
def setJsonFile(filepath,jsonobj):
    with open(filepath,"w") as f:
        json.dump(jsonobj,f)
def getJsonFile(filepath,noNone = False):
    read_txt = read_file(filepath)
    if not read_txt is None:
        return json.loads(read_txt)
    else:
        if noNone:
            return {}
        else:
            return None
xyconfig = getJsonFile('xysite.json')
site_list = xyconfig.get('sitelist',[])
sleepTime = xyconfig.get('sleep',120) 

headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://m.baidu.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    }

def rmhtml(html):
    pattern = re.compile(r'<[^>]+>',re.S)
    result = pattern.sub('', html)
    return result.strip()
def search(retxt, txt , i =1):
    rettxt = ""
    matchObj = re.search(retxt, txt, re.S)
    if matchObj:
        rettxt = matchObj.group(i)
    return rettxt
def getAizhanInfo(domain):
    SiteInfo = {'domain':domain,'baidu_ip':'','baidu_mip':'','baidu_br':'','baidu_mbr':'','360_qz':'','shenma_qz':'','sougou_qz':'','google_pr':'','alexa':'','alexa_ip':'','alexa_pv':'','baidu_sl':'','360_sl':'','sm_sl':'','sogou_sl':'','google_sl':'','baidu_c':'','baidu_mc':''}
    url = "https://www.aizhan.com/seo/"+domain
    req = requests.get(url,headers=headers,verify=True)
    htmlstr = req.text
    SiteInfo['baidu_ip'] = search(r'<span id="baidurank_ip" class="red">(.*?)</span>',htmlstr)          #百度来路
    SiteInfo['baidu_mip'] = search(r'<span id="baidurank_m_ip" class="red">(.*?)</span>',htmlstr)       #移动来路

    SiteInfo['baidu_br'] = search(r'statics.aizhan.com/mobile/images/br/(\d*).png',htmlstr)             #百度权重
    SiteInfo['baidu_mbr'] = search(r'statics.aizhan.com/mobile/images/mbr/(\d*).png',htmlstr)           #百度移动权重
    SiteInfo['qz_360'] = search(r'statics.aizhan.com/mobile/images/360/(\d*).png',htmlstr)              #360权重
    SiteInfo['shenma_qz'] = search(r'statics.aizhan.com/mobile/images/sm/(\d*).png',htmlstr)            #神马权重
    SiteInfo['sougou_qz'] = search(r'statics.aizhan.com/mobile/images/sr/(\d*).png',htmlstr)            #搜狗PR
    SiteInfo['google_pr'] = search(r'statics.aizhan.com/mobile/images/pr/(\d*).png',htmlstr)            #谷歌PR

    SiteInfo['alexa'] = search(r'class="w3" style="color:#222">(.*?)</a>',htmlstr)                      #世界排名
    SiteInfo['alexa_ip'] = search(r'<span id="alexa_ip" class="w3">(.*?)</span>',htmlstr)               #alexa_ip 日均IP
    SiteInfo['alexa_pv'] = search(r'<span id="alexa_pv">(.*?)</span>',htmlstr)                          #alexa_pv 日均PV
    shoulu1_baidu = search(r'<td id="shoulu1_baidu">([\s\S]*?)</td>',htmlstr)
    SiteInfo['baidu_sl'] = search(r'target="_blank">([\s\S]*?)</a>',shoulu1_baidu)                      #百度收录
    shoulu1_360 = search(r'<td id="shoulu1_360">([\s\S]*?)</td>',htmlstr)
    SiteInfo['sl_360'] = search(r'target="_blank">([\s\S]*?)</a>',shoulu1_360)                          #360收录
    shoulu1_sm = search(r'<td id="shoulu1_sm">([\s\S]*?)</td>',htmlstr)
    SiteInfo['sm_sl'] = search(r'target="_blank">([\s\S]*?)</a>',shoulu1_sm)                            #神马收录
    shoulu1_sogou = search(r'<td id="shoulu1_sogou">([\s\S]*?)</td>',htmlstr)
    SiteInfo['sogou_sl'] = search(r'target="_blank">([\s\S]*?)</a>',shoulu1_sogou)                      #搜狗收录
    shoulu1_google = search(r'<td id="shoulu1_google">([\s\S]*?)</td>',htmlstr)
    SiteInfo['google_sl'] = search(r'target="_blank">([\s\S]*?)</a>',shoulu1_google)                    #谷歌收录
    SiteInfo['baidu_c'] = search(r'<td id="cc1">(.*?)</td>',htmlstr)                                    #百度PC词
    SiteInfo['baidu_mc'] = search(r'<td id="cc2">(.*?)</td>',htmlstr)                                   #百度移动词
    for key,val in SiteInfo.items():
        SiteInfo[key]=rmhtml(val)
    return SiteInfo

def getChinazInfo(domain):
    SiteInfo = {'baidu_ip':'','baidu_mip':'','baidu_br':'','baidu_mbr':'','360_qz':'','shenma_qz':'','sougou_qz':'','google_pr':'','alexa':'','alexa_ip':'','alexa_pv':'','baidu_sl':'','360_sl':'','sm_sl':'','sogou_sl':'','google_sl':'','baidu_c':'','baidu_mc':''}
    url = "http://mseo.chinaz.com/"+domain

    return SiteInfo

def go():
    while True:
        try:
            xyconfig1 = getJsonFile('xysite.json')
            site_list = xyconfig1.get('sitelist',[])
            sleepTime = xyconfig1.get('time',120) 
            jsonpath = xyconfig1.get('jsonpath','') 
            site_list_info = []
            for site in site_list:
                site_list_info.append(getAizhanInfo(site))
            jsonobj = {"code":0,"msg":"","count":len(site_list),"data":site_list_info}
            setJsonFile(jsonpath+"site_aizhan.json",jsonobj)
        except Exception, e:
            print('getzhanInfo err:' + str(e))
        time.sleep(sleepTime * 60)

Thread(target=go, args=()).start()