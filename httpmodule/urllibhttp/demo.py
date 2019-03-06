import ssl
import socket
from urllib import request
from urllib import parse
from urllib import error
from urllib import robotparser
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
# print(response.read().decode('utf-8'))

# HTTPError
'''
它有三个属性。
code，返回 HTTP Status Code，即状态码，比如 404 网页不存在，500 服务器内部错误等等。
reason，同父类一样，返回错误的原因。
headers，返回 Request Headers。
'''
try:
    response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.HTTPError as e:
    print(e.reason, e.code, e.headers, sep='\n')


'''
解析链接 parse模块
'''
# scheme://netloc/path;parameters?query#fragment
result = parse.urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(request)

'''
有了 urlparse() 那相应地就有了它的对立方法 urlunparse()。
它接受的参数是一个可迭代对象，但是它的长度必须是 6，否则会抛出参数数量不足或者过多的问题
'''
data = ['https', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(parse.urlunparse(data))

'''
urlsplit()
这个和 urlparse() 方法非常相似，只不过它不会单独解析 parameters 这一部分，只返回五个结果。
上面例子中的 parameters 会合并到 path中，用一个实例感受一下：
'''
result = parse.urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
print(result)


'''
urljoin()
有了 urlunparse() 和 urlunsplit() 方法，我们可以完成链接的合并，不过前提必须要有特定长度的对象，链接的每一部分都要清晰分开。
生成链接还有另一个方法，利用 urljoin() 方法我们可以提供一个 base_url（基础链接），新的链接作为第二个参数，
方法会分析 base_url 的 scheme、netloc、path 这三个内容对新链接缺失的部分进行补充，作为结果返回。
可以发现，base_url 提供了三项内容，scheme、netloc、path，如果这三项在新的链接里面不存在，那么就予以补充，如果新的链接存在，
那么就使用新的链接的部分。base_url 中的 parameters、query、fragments 是不起作用的。
'''
print(parse.urljoin('http://www.baidu.com', 'FAQ.html'))
print(parse.urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
print(parse.urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(parse.urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(parse.urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(parse.urljoin('http://www.baidu.com', '?category=2#comment'))
print(parse.urljoin('www.baidu.com', '?category=2#comment'))
print(parse.urljoin('www.baidu.com#comment', '?category=2'))

'''
urlencode
'''
data = {
    'name': 'muzi',
    'age': '18'
}
base_url = 'http://www.baidu.com?'
result = base_url + parse.urlencode(data)
print(result)

'''
parse_qs()
'''
str = 'name=germey&age=22'
print(parse.parse_qs(str))

'''
quote()
quote() 方法可以将内容转化为 URL 编码的格式，有时候 URL 
中带有中文参数的时候可能导致乱码的问题，所以我们可以用这个方法将中文字符转化为 URL 编码
'''
key = '蝴蝶'
res = 'http://www.baidu.com?k=' + parse.quote(key)
print(res)
print(parse.unquote(res))

'''
robotparser
有常用的几个方法分别介绍一下：
set_url()，用来设置 robots.txt 文件的链接。如果已经在创建 RobotFileParser 对象时传入了链接，那就不需要再使用这个方法设置了。
read()，读取 robots.txt 文件并进行分析，注意这个函数是执行一个读取和分析操作，如果不调用这个方法，接下来的判断都会为 False，
所以一定记得调用这个方法，这个方法不会返回任何内容，但是执行了读取操作。
parse()，用来解析 robots.txt 文件，传入的参数是 robots.txt 某些行的内容，它会按照 robots.txt 的语法规则来分析这些内容。
can_fetch()，方法传入两个参数，第一个是 User-agent，第二个是要抓取的 URL，返回的内容是该搜索引擎是否可以抓取这个 URL，返回结果是 True 或 False。
mtime()，返回的是上次抓取和分析 robots.txt 的时间，这个对于长时间分析和抓取的搜索爬虫是很有必要的，你可能需要定期检查来抓取最新的 robots.txt。
modified()，同样的对于长时间分析和抓取的搜索爬虫很有帮助，将当前时间设置为上次抓取和分析 robots.txt 的时间。
'''
rp = robotparser.RobotFileParser()
rp.set_url('http://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'http://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', 'http://www.jianshu.com/search?q=python&page=1&type=collections'))

rp = robotparser.RobotFileParser()
rp.parse(request.urlopen('http://www.baidu.com/robots.txt').read().decode('utf-8').split('\n'))
print(rp.can_fetch('*', 'http://www.baidu.com/p/b67554025d7d'))
print(rp.can_fetch('*', 'http://www.baidu.com/search?q=python&page=1&type=collections'))
