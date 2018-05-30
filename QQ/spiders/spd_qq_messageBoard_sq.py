# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from QQ.items import QQ_MessageBoardItem
import re
import time, datetime

# QQ留言板爬虫
class spd_qq_messageBoard_class(Spider):
    name = "spd_qq_messageBoard_sq"
    start_urls = (
        'https://user.qzone.qq.com/371312563/334',
    )
    ignore_page_incremental = True

    def start_requests(self):

        cookies = {
            'tvfe_boss_uuid':'e539e3a2004266fc',
            'mobileUV':'1_15a133fc27e_119d5',
            'RK':'VIUj1Hr+fb',
            'pgv_pvi':'1082606592',
            'cuid':'5261410576',
            'UM_distinctid':'15cd5ac89a8407-03d6ce459719bb-323f5c0f-240000-15cd5ac89a997b',
            '_gscu_661903259':'985808951uzi5r54',
            'pac_uid':'1_376976240',
            '__Q_w_s__QZN_TodoMsgCnt':'1',
            'gid':'30177e60-7d5a-4e81-8053-65fa8b1d79e0',
            '__Q_w_s_hat_seed':'1',
            'o_cookie':'376976240',
            'pgv_pvid':'8390529638',
            'Loading':'Yes',
            'qz_screen':'2048x1152',
            'pgv_info=ssid':'s8268853734',
            'QZ_FE_WEBP_SUPPORT':'1',
            'cpu_performance_v8':'6',
            'pgv_si':'s4960348160',
            'ptisp':'ctc',
            'ptcz':'f06286f90a46e546b9df0cbb01cfdd682edd74f67cfda0eddb0e147a1797daf3',
            'pt2gguin':'o0376976240',
            'uin':'o0376976240',
            'skey':'@DeznHJcLi',
            'p_uin':'o0376976240',
            'p_skey':'nSBT7jEwdLCDMwXKpRyTlB-aj*kOmULCvU7Yn07KeeU_',
            'pt4_token':'Gd*29zs0XZZ0aV9ZCRp2-yfebz98rMOW*ybgzfpQdec_',
            'rv2':'80C4559A9AE077CC0A61EB93EFA4A116C02B3A154BE221B919',
            'property20':'DDB5C9B4BD74169AAE485A6E505C138525AD922F22B71504B73740A8D0DABB216E4FF094B8F93096',
            'x-stgw-ssl-info':'a20adeae9d54034df96569c8e80c5824|0.112|1507560624.510|2|r|I|TLSv1.2|ECDHE-RSA-AES128-GCM-SHA256|7500|0',
        }

        for page in range(23):
            starPage=str((page) * 10)
            url_link = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=376976240&hostUin=570381449&num=10&' \
                       'start='+starPage+'&' \
                       'hostword=0&essence=1&r=0.11778180570319363&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=1068883706&qzonetoken=f41791b9be8ade7e04df8813e816da4c9908f720fd0419864e3b57e3ae8bb87ae20e477589f20c7338&g_tk=1068883706'
            request = scrapy.http.FormRequest(url_link, callback=self.parse_content, cookies=cookies, )
            request.meta['starPage'] = starPage
            yield request


    def parse_content(self, response):
        content = response.body
        commentListStr = re.findall('"commentList":([\s\S]+)\}\}',content)[0]
        totalStr = re.findall('total":(.+)\,',content)[0]
        #总楼层
        total = int(totalStr)
        starPage = int(response.meta['starPage'])
        #实际楼层
        floor = total - starPage
        commentList = eval(commentListStr)

        for comment in commentList:
            item = QQ_MessageBoardItem()
            item['floor'] = floor
            item['id'] = comment['id']
            item['secret'] = comment['secret']
            item['pasterid'] = comment['pasterid']
            item['bmp'] = comment['bmp']
            item['pubtime'] = comment['pubtime']
            item['modifytime'] = comment['modifytime']
            item['effect'] = comment['effect']
            item['type'] = comment['type']
            item['uin'] = comment['uin']
            item['nickname'] = comment['nickname']
            item['capacity'] = comment['capacity']
            item['htmlContent'] = comment['htmlContent']
            item['ubbContent'] = comment['ubbContent']
            item['signature'] = comment['signature']
            if comment['replyList'] <> []:
                    for reply in comment['replyList']:
                        item['content'] = reply['content']
                        item['time'] = reply['time']
                        item['nick'] = reply['nick']
            floor = floor - 1
            yield item


