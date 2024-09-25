pass

import sys

from util import *
sys.path.append(getDir(__file__))
from base import *
sys.path.pop()



class WebPage(YModuleItem):
    def __init__(self):
        super().__init__()
        self.keys.extend(['ref','data','ret','summay'])

    def summay(self):
        print("name:"+self.name+" description:"+self.description)

    def info(self):
        self.summay()
        print("ref:"+self.ref)
        if hasattr(self, "data"):
            print("data:"+json.dumps(self.data))

class WebHost(Function, YModuleList):
    def __init__(self, host, jsonarg = {}):
        super().__init__()
        self.keys.extend(['port'])

    def getSession(self):
        if hasattr(self, "session"):
            return self.session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"})
        self.session.headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
        self.session.headers.update({"Accept-Encoding": "gzip, deflate, br"})
        self.session.headers.update({"Accept-Language": "zh-CN,zh;q=0.9"})
        self.session.headers.update({"Connection": "keep-alive"})
        self.session.headers.update({"Upgrade-Insecure-Requests": "1"})
        self.session.headers.update({"Cache-Control": "max-age=0"})
        self.session.headers.update({"Pragma": "no-cache"})
        self.session.headers.update({"Expires": "0"})

        return self.session
        pass
    def login(self):
        login = self.getPage("login")
        session = self.getSession()
        url = self.getUrl(login)
        logging.info("getCookies:"+url+"data:"+json.dumps(login.data))
        url1 = 'http://192.168.120.30:8080/login'
        r = session.get(url1)
        print(r)
        self.cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
        r = session.post(url, data=login.data, cookies=self.cookies)


    def getUrl(self, page):
        return 'http://'+self.host.ip+':'+str(self.port)+'/'+page.ref

    def getPage(self, name):
        for page in self.pages:
            if page.name == name:
                return page
        return None

    def jsonToTable(self, jsonstr):
        data = []
        logging.info("jsonToTable: "+json.dumps(jsonstr))
        for item in jsonstr["parameter"]:
            data.append(("name",item['name']))
            if 'value' in item:
                data.append(("value",item['value']))
        data.append(("statusCode", 303))
        data.append(("redirectTo", "."))
        data.append(("json",json.dumps(jsonstr)))
        data.append(("Submit", "开始构建"))
        return data
        pass

    def dealPage(self, page, dst):
        session = self.getSession()
        url = self.getUrl(page)
        #如果page有data
        if hasattr(page, "data"):
            bjson = page.data
            data = self.jsonToTable(bjson)
            r = session.post(url, data=data, json=bjson, cookies=self.cookies)
            print(r)
            print(r.content)
        else:
            r = session.get(url, cookies=self.cookies)
            print(r)
            #从r中取出文件
            with open(dst, "wb") as f:
                f.write(r.content)
                f.flush()

            pass
        if hasattr(page, "ret"):
            webbrowser.open_new(page.ret);

    def getPageData(self, urlname, dst = './tmp'):
        self.login()
        page = self.getPage(urlname)
        self.dealPage(page, dst)
