# # import ahttp as ahttp
# # import requests
# import grequests
# from bs4 import BeautifulSoup
#
# app_icon_spider = [
#     {
#         'app_store': '小米应用商店',
#         'url_template': 'http://app.mi.com/details?id=%s',
#         'app_icon_selector': 'body > div.main > div.container.cf > div.app-intro.cf > div.app-info > img',
#         'app_name_selector': 'body > div.main > div.container.cf > div.app-intro.cf > div.app-info > div > h3'
#     },
#     {
#         'app_store': '应用宝',
#         'url_template': 'https://sj.qq.com/myapp/detail.htm?apkName=%s',
#         'app_icon_selector': '#J_DetDataContainer > div > div.det-ins-container.J_Mod > div.det-icon > img',
#         'app_name_selector': '#J_DetDataContainer > div > div.det-ins-container.J_Mod > div.det-ins-data > '
#                              'div.det-name > div.det-name-int '
#     },
#     {
#         'app_store': '应用汇',
#         'url_template': 'http://www.appchina.com/app/%s',
#         'app_icon_selector': '#pagecontainer > div.main > div.app-msg > div.app-detail > div > img',
#         'app_name_selector': '#pagecontainer > div.main > div.app-msg > div.app-detail > div > h1'
#     },
#     {
#         'app_store': 'APKsHub',
#         'url_template': 'https://cn.apkshub.com/app/%s',
#         'app_icon_selector': '#container > div > div.content > div > div.panel-heading.clearfix > div.cover > img',
#         'app_name_selector': '#container > div > div.content > div > div.panel-body > div.appinfo > ul > '
#                              'li:nth-child(1) > span:nth-child(2) '
#     },
#     {
#         'app_store': '酷安',
#         'url_template': 'https://www.coolapk.com/apk/%s',
#         'app_icon_selector': 'body > div.warpper > div:nth-child(2) > div.app_left > div.apk_left_one > div > img',
#         'app_name_selector': 'body > div.warpper > div:nth-child(2) > div.app_left > div.apk_left_one > div > div > '
#                              'div.apk_topbar_mss > p.detail_app_title '
#     },
#     {
#         'app_store': '魅族应用商店',
#         'url_template': 'http://app.meizu.com/apps/public/detail?package_name=%s',
#         'app_icon_selector': '#theme_content > div.left.inside_left > div.app_download.download_container > img',
#         'app_name_selector': '#theme_content > div.right.inside_right > div > div.detail_top > h3'
#     }
# ]
#
# package_name_spider = [
#     {
#         'app_store': '小米应用商店',
#         'url_template': 'http://app.mi.com/searchAll?keywords=%s',
#         'app_icon_selector': 'body > div.main > div > div.main-con > div.applist-wrap > ul > li > a > img',
#         'package_name_selector': 'body > div.main > div > div.main-con > div.applist-wrap > ul > li > h5 > a',
#         'package_name_pattern': '/details\\?id=|&ref=search'
#     }
# ]
#
#
# class AppIconSpider:
#     @classmethod
#     def search_by_package_name(cls, package_name):
#         app_icons = []
#         # import time
#         # start = time.time()
#         req_list = [  # 请求列表
#             grequests.get(url % package_name) for url in (spider['url_template'] for spider in app_icon_spider)
#         ]
#         res_list = grequests.map(req_list, size=100)  # 并行发送，等最后一个运行完后返回
#         for index, item in enumerate(app_icon_spider):
#             app_icon = {'app_store': item['app_store']}
#             app_url = item['url_template'] % package_name
#             # str_html = requests.get(app_url)
#             str_html = res_list[index]
#             app_icon_img = BeautifulSoup(str_html.text, 'lxml').select(item['app_icon_selector'])
#             app_name_div = BeautifulSoup(str_html.text, 'lxml').select(item['app_name_selector'])
#             if not app_name_div or not app_name_div[0].get_text() or not app_icon_img or not app_icon_img[0].get('src'):
#                 continue
#             else:
#                 app_icon['app_name'] = app_name_div[0].get_text()
#                 app_icon['app_icon_url'] = app_icon_img[0].get('src')
#                 app_icon['app_url'] = item['url_template'] % package_name
#                 app_icons.append(app_icon)
#         # print('---------------')
#         # print(time.time()-start)
#         # print('---------------')
#         return app_icons
#
#     @classmethod
#     def search_package_name(cls, app_name):
#         package_names = []
#         req_list = [  # 请求列表
#             grequests.get(url % app_name) for url in (spider['url_template'] for spider in package_name_spider)
#         ]
#         res_list = grequests.map(req_list, size=100)  # 并行发送，等最后一个运行完后返回
#         # import time
#         # start = time.time()
#         for index, item in enumerate(package_name_spider):
#             app_url = item['url_template'] % app_name
#             # str_html = requests.get(app_url)
#             str_html = res_list[index]
#             package_name_str = BeautifulSoup(str_html.text, 'lxml').select(item['package_name_selector'])
#             app_icon_img = BeautifulSoup(str_html.text, 'lxml').select(item['app_icon_selector'])
#             if not package_name_str or not package_name_str[0].get_text():
#                 continue
#             else:
#                 for i in range(len(package_name_str)):
#                     package_name = {'app_store': item['app_store'],
#                                     'package_name': ((package_name_str[i].get('href'))[12:])[:-11],
#                                     'app_name': package_name_str[i].get_text(),
#                                     'app_icon_url': app_icon_img[i].get('data-src')}
#                     # print(i)
#                     # package_name['app_url'] = app_url
#                     package_names.append(package_name)
#         # print('---------------')
#         # print(time.time()-start)
#         # print('---------------')
#         return package_names
