import requests
import re

r = requests.get('https://www.baidu.com')
print(type(r))
print(r.status_code)
print(r.text)
print(r.cookies)

r = requests.post('http://httpbin.org/post')
r = requests.put('http://httpbin.org/put')


'''
Get
'''

data = {
    'name': 'muzi',
    'age': 22
}

r = requests.get('http://httpbin.org/get', data)
print(r.text)
print(r.json())

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get('https://www.zhihu.com/explore', headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles = re.findall(pattern, r.text)
print(titles)

'''
抓取二进制数据
'''
r = requests.get("https://github.com/favicon.ico")
with open('favicon.ico', 'wb') as f:
    f.write(r.content)


'''
POST
'''
data = {
    'name': 'muzi',
    'age': 22
}
r = requests.post('http://httpbin.org/post', data=data)
print(r.text)

'''
# Informational.
100: ('continue',),
101: ('switching_protocols',),
102: ('processing',),
103: ('checkpoint',),
122: ('uri_too_long', 'request_uri_too_long'),
200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
201: ('created',),
202: ('accepted',),
203: ('non_authoritative_info', 'non_authoritative_information'),
204: ('no_content',),
205: ('reset_content', 'reset'),
206: ('partial_content', 'partial'),
207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
208: ('already_reported',),
226: ('im_used',),

# Redirection.
300: ('multiple_choices',),
301: ('moved_permanently', 'moved', '\\o-'),
302: ('found',),
303: ('see_other', 'other'),
304: ('not_modified',),
305: ('use_proxy',),
306: ('switch_proxy',),
307: ('temporary_redirect', 'temporary_moved', 'temporary'),
308: ('permanent_redirect',
      'resume_incomplete', 'resume',), # These 2 to be removed in 3.0

# Client Error.
400: ('bad_request', 'bad'),
401: ('unauthorized',),
402: ('payment_required', 'payment'),
403: ('forbidden',),
404: ('not_found', '-o-'),
405: ('method_not_allowed', 'not_allowed'),
406: ('not_acceptable',),
407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
408: ('request_timeout', 'timeout'),
409: ('conflict',),
410: ('gone',),
411: ('length_required',),
412: ('precondition_failed', 'precondition'),
413: ('request_entity_too_large',),
414: ('request_uri_too_large',),
415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
417: ('expectation_failed',),
418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
421: ('misdirected_request',),
422: ('unprocessable_entity', 'unprocessable'),
423: ('locked',),
424: ('failed_dependency', 'dependency'),
425: ('unordered_collection', 'unordered'),
426: ('upgrade_required', 'upgrade'),
428: ('precondition_required', 'precondition'),
429: ('too_many_requests', 'too_many'),
431: ('header_fields_too_large', 'fields_too_large'),
444: ('no_response', 'none'),
449: ('retry_with', 'retry'),
450: ('blocked_by_windows_parental_controls', 'parental_controls'),
451: ('unavailable_for_legal_reasons', 'legal_reasons'),
499: ('client_closed_request',),

# Server Error.
500: ('internal_server_error', 'server_error', '/o\\', '✗'),
501: ('not_implemented',),
502: ('bad_gateway',),
503: ('service_unavailable', 'unavailable'),
504: ('gateway_timeout',),
505: ('http_version_not_supported', 'http_version'),
506: ('variant_also_negotiates',),
507: ('insufficient_storage',),
509: ('bandwidth_limit_exceeded', 'bandwidth'),
510: ('not_extended',),
511: ('network_authentication_required', 'network_auth', 'network_authentication')
'''
r = requests.get('http://www.jianshu.com')
if requests.codes.ok == r.status_code:
    print('success')
else:
    print(r.status_code)


'''
高级用法
'''

# 文件上传
file = {'file': open('favicon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files=file)
print(r.text)

# cookie
r = requests.get('https://www.baidu.com')
print(r.cookies)
# 可以发现它是一个 RequestCookieJar 类型，然后我们用 items() 方法将其转化为元组组成的列表
for key, value in r.cookies.items():
    print(key + '=' + value)

headers = {
    'Cookie': '_zap=e875bfac-665a-4bd2-91fc-8ecbf374bede; d_c0="AFAn7r-AIg6PTodtRT7kn_1eSjyG9KN_cxo=|1535613620"; _xsrf=c22e973b-996c-4bfe-b961-29ccc81ad9c2; l_n_c=1; q_c1=6bf6e140e7a9491dbdf1efa0f0b80771|1550664334000|1535613622000; n_c=1; __utmc=51854390; __utmz=51854390.1550664336.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); capsion_ticket="2|1:0|10:1550668223|14:capsion_ticket|44:ZGFkY2RiMzJmMzljNGJjNmI1NDhiZjM3ZTRjNDk1ZWE=|a940e3355ee2f627effd97356e8e7b50201fb8c7db1a4cab05c32a1f39fe0168"; r_cap_id="NGUyNjAzOWNmYjExNGYxM2FiM2QzZTVmMGM5ZWYxNDg=|1550668228|daf129679859737155a406980fec77a1913337dd"; cap_id="ZTUyMTA0NmM2N2IwNDNkMDliOTVjYTg4MTQzYmQ0NjY=|1550668228|4b9c00a66c9f9a7bec3e4f9447d1583cdceacdff"; l_cap_id="NDI3MGUyMDU3YWYxNDFlNDgxMTBmYjBkYjhiMDMzODg=|1550668228|4a736cafd765c663a17a2bd6d640aa55e8e098fe"; z_c0=Mi4xamx5ZEFBQUFBQUFBVUNmdXY0QWlEaGNBQUFCaEFsVk55WjlhWFFBTEs5Q21zbXJsZGJFWlhYRm04OTdNaDFyT3F3|1550668233|c354fd81bef85ae6b102aaad5735d3d9e6e2d5f7; tst=r; __utma=51854390.1481986629.1550664336.1550664336.1552121465.2; __utmv=51854390.100--|2=registration_date=20141107=1^3=entry_date=20141107=1; tgw_l7_route=7c109f36fa4ce25acb5a9cf43b0b6415',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
r = requests.get('https://www.zhihu.com', headers=headers)
print(r.text)
print(r.status_code)

# 会话维持
s = requests.session()
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)

# 代理设置
