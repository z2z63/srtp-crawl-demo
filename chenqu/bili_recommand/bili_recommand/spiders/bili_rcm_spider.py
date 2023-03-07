import time
from pathlib import Path
import scrapy
from scrapy.http.response.html import HtmlResponse
from urllib import parse


class BiliRcmSpider(scrapy.Spider):
    name = "bili_rcm"

    def start_requests(self):
        for i in range(20):
            url = "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd"
            url_params = {
                'y_num': 5,
                'fresh_type': 3,
                'feed_version': 'V8',
                'fresh_idx_1h': i + 1,
                'fetch_row': 1,
                'fresh_idx': i + 1,
                'brush': i,
                'homepage_ver': 1,
                'ps': 10,
                'outside_trigger': None,
                'w_rid': '08dd27da4962ef154b717254bf50f9fc',
                'wts': '1676121978',
            }
            url += '?' + parse.urlencode(url_params)
            yield scrapy.Request(url, self.parse)

    def parse(self, response: HtmlResponse, **kwargs):
        for item in response.json()['data']['item']:
            video_title = item['title']
            video_url = item['uri']
            video_upload_user_nickname = item['owner']['name']
            video_upload_user_uid = item['owner']['mid']
            video_upload_user_avatar_url = item['owner']['face']
            video_duration = item['duration']
            video_upload_date = item['pubdate']
            video_stat_danmaku = item['stat']['danmaku']
            video_stat_like = item['stat']['like']
            video_stat_view = item['stat']['view']

            yield {
                "title": video_title,
                "url": video_url,
                "upload_user": {
                    "nickname": video_upload_user_nickname,
                    "avatar": video_upload_user_avatar_url,
                    "uid": video_upload_user_uid
                },
                "duration": video_duration,
                "upload_date": video_upload_date,
                "stat": {
                    "like": video_stat_like,
                    "danmaku": video_stat_danmaku,
                    "view": video_stat_view
                },
                "scrab_time": round(time.time())
            }


# class JDSpider(scrapy.spiders):
#     name = "jd-item"
    