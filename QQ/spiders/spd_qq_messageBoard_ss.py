# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from QQ.items import QQ_MessageBoardItem
import re
import time, datetime

# QQ留言板爬虫
class spd_qq_messageBoard_class(Spider):
    name = "spd_qq_messageBoard_ss"
    start_urls = (
        'https://user.qzone.qq.com/1007645150/334',
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
            'welcomeflash':'1007645150_84535',
            'qqmusic_uin':'',
            'qqmusic_key':'',
            'qqmusic_fromtag':'',
            'qzmusicplayer':'qzone_player_1007645150_1507561244398',
            'p_uin':'o0376976240',
            'p_skey':'cdazEsDsWspLZnp5I45i8pB9v-KhHbL1*bGpQ17b3Zw_',
            'pt4_token':'iv4NvLA*nidPhTfBw4NMhPIIj*w8whlS39SbHhNsBSo_',
            'rv2':'809FA1B7F55F15A23E63937DAFA0148280F14F57BF6676D632',
            'property20':'933BA063DD9D256D3F8993BCF5D29F8363D47C0DF5934CE971EED7D9ECF09233EE6250E8B232685D',
            'x-stgw-ssl-info':'d03bcbb1a8c3c82d2d1f4fc22fb7281f|0.135|1507562662.366|6|r|I|TLSv1.2|ECDHE-RSA-AES128-GCM-SHA256|41500|0',
            'ptisp':'ctc',
            'ptcz':'f06286f90a46e546b9df0cbb01cfdd682edd74f67cfda0eddb0e147a1797daf3',
            'pt2gguin':'o0376976240',
            'uin':'o0376976240',
            ' skey':'@DeznHJcLi',
        }

        for page in range(123):
            starPage=str((page) * 10)
            url_link = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=376976240&hostUin=1007645150&num=10&' \
                       'start='+starPage+'&hostword=0&essence=1&r=0.98732437358852&iNotice=0' \
                       '&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=1694984901&qzonetoken=7505914022b4ad68a6b2b56fd61c2e9d9b95c90cfd342a9d16823256c84215f8719eb59b82fda930d1&g_tk=1694984901'
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


