import ssl
import socket
from urllib import request
from urllib import parse
from urllib import error
from http import cookiejar

'''
查找相关资料后确定为，Python 2.7.9 之后版本引入了一个新特性：当你urllib.urlopen一个 
https 的时候会验证一次 SSL 证书 ，当目标使用的是自签名的证书时就会爆出该错误消息。
'''
ssl._create_default_https_context = ssl._create_unverified_context
response = request.urlopen('https://www.python.org')
print(type(response))
# print(response.read().decode('utf-8'))
print(response.status)
print(response.getheader('Server'))
print(response.getheaders())

'''
data参数
'''
data = bytes(parse.urlencode({'hello': 'world'}), encoding='utf-8')
response = request.urlopen('http://httpbin.org/post', data)
print(response.read())

'''
timeout参数
'''
try:
    response = request.urlopen('http://httpbin.org/get', timeout=0.1)
except error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('Time out')

'''
Request
由上我们知道利用 urlopen() 方法可以实现最基本请求的发起，但这几个简单的参数并不足以构建一个完整的请求，
如果请求中需要加入 Headers 等信息，我们就可以利用更强大的 Request 类来构建一个请求。
'''
url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'Germey'
}
data = bytes(parse.urlencode(dict), encoding='utf-8')
myRequest = request.Request(url, data, headers, method='POST')
myRequest.add_header('Token', 'muzi')
response = request.urlopen(myRequest)
print(response.read().decode('utf-8'))

'''
高级用法
认证
'''
username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = request.HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handler = request.HTTPBasicAuthHandler(p)
opener = request.build_opener(auth_handler)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except error.URLError as e:
    print(e.reason)

'''
高级用法
代理
'''
proxy_handler = request.ProxyHandler({
    'http': 'http://127.0.0.1:9743',
    'https': 'https://127.0.0.1:9743'
})
opener = request.build_opener(proxy_handler)
try:
    response = opener.open('https://www.baidu.com')
    print(response.read().decode('utf-8'))
except error.URLError as e:
    print(e.reason)

'''
高级用法
Cookies
'''
cookie = cookiejar.CookieJar()
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name + '=' + item.value)

# 保存到文件
filename = 'cookies.txt'
cookie = cookiejar.MozillaCookieJar(filename)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)

# 使用保存的cookie文件
cookie = cookiejar.MozillaCookieJar()
cookie.load('cookies.txt', ignore_expires=True, ignore_discard=True)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
response = opener.open('http://www.baidu.com')
print(response.read().decode('utf-8'))
