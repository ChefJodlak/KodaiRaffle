import cfscrape
import requests
import time
import json

class Raffle:
    def __init__(self, raffleid, captchaapi, email, proxy):
        self.raffleid = raffleid
        self.captchaapi = captchaapi
        self.email = email
        self.proxy = proxy
        self.sitekey = '6LceuKAUAAAAANlszS-ySauzunmtpFRKPFPsReaB'
        self.token = self.gettokens()

    def parseproxy(self):
        proxy = self.proxy.split(":")
        return {'http': 'http://'+proxy[2]+':'+proxy[3]+'@'+proxy[0]+':'+proxy[1],
         'https': 'https://'+proxy[2]+':'+proxy[3]+'@'+proxy[0]+':'+proxy[1]}

    def gettokens(self):
        tokens, useragent = cfscrape.get_tokens("https://raffles.kodai.io/raffles/"+self.raffleid, proxies=self.parseproxy())
        return tokens['__cfduid']

    def getcaptcha(self):
        print("Getting Captcha from 2Captcha")
        s = requests.Session()

        # here we post site key to 2captcha to get captcha ID (and we parse it here too)
        captcha_id = s.post(
            "http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".
                format(self.captchaapi, self.sitekey,
                       "https://raffles.kodai.io/raffles/"+self.raffleid)).text.split('|')[1]
        # then we parse gresponse from 2captcha response
        recaptcha_answer = s.get(
            "http://2captcha.com/res.php?key={}&action=get&id={}".format(self.captchaapi, captcha_id)).text
        print("Solving Captcha...")
        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            time.sleep(1)
            recaptcha_answer = s.get(
                "http://2captcha.com/res.php?key={}&action=get&id={}".format(self.captchaapi, captcha_id)).text
        recaptcha_answer = recaptcha_answer.split('|')[1]
        return recaptcha_answer

    def sendrequest(self, recaptcha):
        url = 'https://raffles.kodai.io/api/raffles/submitEntry'
        data = {"social":"N/A","raffle_id":self.raffleid,"email_address":self.email,"g-recaptcha-response":recaptcha}
        headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8", "accept": "*/*",
                   "x-requested-with": "XMLHttpRequest", "accept-language": "pl-pl",
                   "accept-encoding": "br, gzip, deflate", "origin": "https://raffles.kodai.io",
                   "referer": "https://raffles.kodai.io/raffles/"+self.raffleid,
                   "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/79.0.3945.73 Mobile/15E148 Safari/605.1",
                   "content-length": "659"}
        cookies = {'__cfduid': self.token}

        response = requests.post(url, data=json.dumps(data), headers=headers,
                                 cookies=cookies, proxies=self.parseproxy())

        print(self.email + ' ' + response.text)

    def doraffle(self):
        print('Signing {}'.format(self.email))
        captcha = self.getcaptcha()
        self.sendrequest(captcha)
