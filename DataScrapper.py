import asyncio
from pyppeteer import launch
import urllib.request
from bs4 import BeautifulSoup
import unicodedata
import operator


async def response_check(resp):
    if resp != None:
        req = resp.request
        if req.resourceType in ['xhr']:
            url = resp.url
            print (url)
            if 'd_su_' in url:
                print (url)
                rep_text = await resp.text()
                r.write (url)
                r.write ("\n")
                r.write (rep_text)
                r.write ("\n")

async def request_check(req):
    await req.continue_()


async def main():
    browser = await launch(executablePath="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    #browser = await launch(executablePath="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    page = await browser.newPage()
    await page.setRequestInterception(True)
    page.on('request', request_check)
    page.on('response', response_check)
    await page.goto('https://www.flashscores.co.uk/match/0YH8p8kJ/#match-summary', waitUntil='networkidle0')
    
    await browser.close()

r = open('socceraznqiaxjniqjxsixnsresponse.text','w')
asyncio.get_event_loop().run_until_complete(main())
r.close()
