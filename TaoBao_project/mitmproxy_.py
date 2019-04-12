import mitmproxy.http
from mitmproxy import ctx

t0 = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});'
t1 = 'window.navigator.chrome = {runtime: {},// etc.};'
t2 = '''
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
'''
t3 = '''
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
'''
t4 = '''
Object.defineProperties(navigator,{
 userAgent:{
   get: () => Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36;
 }
})
'''


class Tb(object):
    def response(slef, flow: mitmproxy.http.HTTPFlow):
        if '115.js' in flow.request.url or 'um.js' in flow.request.url:
            flow.response.text = t3 + t2 + t4 + t0 + flow.response.text
            ctx.log.info("注入成功")


addons = [
    Tb()
]
