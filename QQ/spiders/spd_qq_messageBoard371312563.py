# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from QQ.items import QQ_MessageBoardItem
import re
import time, datetime

# QQ留言板爬虫
class spd_qq_messageBoard_class(Spider):
    name = "spd_qq_messageBoard371312563"
    start_urls = (
        'https://user.qzone.qq.com/371312563/334',
    )
    ignore_page_incremental = True

    def start_requests(self):

        cookies = {
            'tvfe_boss_uuid': 'e539e3a2004266fc',
            'mobileUV': '1_15a133fc27e_119d5',
            'RK': 'VIUj1Hr+fb',
            'pgv_pvi': '1082606592',
            'cuid': '5261410576',
            'UM_distinctid': '15cd5ac89a8407-03d6ce459719bb-323f5c0f-240000-15cd5ac89a997b',
            '_gscu_661903259': '985808951uzi5r54',
            'pac_uid': '1_376976240',
            '__Q_w_s__QZN_TodoMsgCnt': '1',
            'gid': '30177e60-7d5a-4e81-8053-65fa8b1d79e0',
            'luin': 'o0376976240',
            'lskey': '00010000d0d50ae60b268b3eb6501426087c99bf1df0ce787df551932e8c3ba79d7d7431e03ad3f68859f14b',
            '__Q_w_s_hat_seed': '1',
            'o_cookie': '376976240',
            'pgv_pvid': '8390529638',
            'qz_screen': '2048x1152',
            'QZ_FE_WEBP_SUPPORT': '1',
            'cpu_performance_v8': '7',
            'ptisp': 'ctc',
            'ptcz': 'f06286f90a46e546b9df0cbb01cfdd682edd74f67cfda0eddb0e147a1797daf3',
            'pt2gguin': 'o0376976240',
            'uin': 'o0376976240',
            'skey': '@W8XpaiFer',
            'p_uin': 'o0376976240',
            'p_skey': 'MpRgtI0Vfd54eIW40BIvqiR7jf14yxxUw81Avl1tP6Q_',
            'pt4_token': 'f5ZgvNxhVZ2oGSpnOaKKELq05qHngaQWjvPFpiBdNd4_',
            'rv2': '80D265E2E2F6BCFE9F7315DF851F4C504D9D9615917B290DE5',
            'property20': 'E153A7AA65F366EBF85B47B0E8AE0C792A4D8836C7E3420D005D8EE2974E349201DFC5C3E195BF10',
            'x-stgw-ssl-info': 'c3fc43948c1eb267bbe8765c71ba5464|0.102|1507398521.464|2|.|I|TLSv1.2|ECDHE-RSA-AES128-GCM-SHA256|7500|0',
            'pgv_si': 's7437732864',
            'pgv_info': 'ssid=s2524336221',
        }

        for page in range(81):
            starPage=str((page) * 10)
            url_link = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=376976240&hostUin=371312563&num=10&' \
                       'start='+starPage+'&' \
                       'hostword=0&essence=1&r=0.8458069268440465&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=500194255&qzonetoken=f05c1d12c0653e248e4b554b7f3efe372b94e839aa1f7c61c93cddb09c450933f79feb4d3fae24fe&g_tk=500194255'
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


