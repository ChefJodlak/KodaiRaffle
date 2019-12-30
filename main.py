from raffle import Raffle

raffleid = '7TPI2CV9M8XS41'
captchaapi = ''

with open('email.txt') as f:
    emails = f.readlines()

with open('proxies.txt') as f:
    proxies = f.readlines()

for email, proxy in zip(emails, proxies):
    raffle = Raffle(raffleid, captchaapi, email.rstrip(), proxy.rstrip())
    raffle.doraffle()

