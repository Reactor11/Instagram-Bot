from selenium import webdriver
import os
import sys
import requests
import time
from lxml.html import fromstring
import numpy as np
import re
import logging 
import urllib.request

logging.basicConfig(filename="scrapeImgur.log", format='%(levelname)s  %(message)s',filemode='a')  
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
logger.info("---------------------------------STARTED EXECUTION---------------------------------")

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[3][contains(text(),"IN")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return list(proxies)

url = "https://imgur.com/gallery"
if(sys.platform == 'linux'):
    webDriveLoc = os.path.abspath(os.getcwd()) + "/chromedriver"
    logger.info("Linux operating system, chromeDriver location : " + webDriveLoc)
else:
    webDriveLoc = os.path.abspath(os.getcwd()) + "\\chromedriver.exe"
    logger.info("Linux operating system, chromeDriver location : " + webDriveLoc)
PROXY = get_proxies()

chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument("window-size=1920,1080")
chrome_option.add_argument("--incognito")
# if(len(PROXY)!=0):
#     chrome_option.add_argument('--proxy-server=%s' % PROXY[np.random.randint(0,len(PROXY))])
# chrome_option.add_argument("--headless")

logger.info("Setting up Chrome options : " + " ".join(chrome_option.arguments))

driver = webdriver.Chrome(executable_path=webDriveLoc,options=chrome_option)
logger.info(driver)
driver.get(url)
# time.sleep(5)
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
# time.sleep(5)

linksList = set()
for tag in driver.find_elements_by_tag_name('a'):
    x = re.findall("https://imgur.com/gallery/[a-zA-z0-9]*[^/]",tag.get_attribute('href'))
    if(len(x)!=0):
        linksList.add(x[0])
linksList = list(linksList)
# driver.quit()

# linksList = ['https://imgur.com/gallery/zY4fAAF', 'https://imgur.com/gallery/iZqLakX','https://imgur.com/gallery/wIXX8S6']
imageLinksList = list()
videoLinksList = list()
for link in linksList:
    try:
        driver.get(str(link))
        time.sleep(3)
        for tag in driver.find_elements_by_class_name('image-placeholder'):
            imageLinksList.append(tag.get_attribute('src'))
            logger.info("Image link : " + tag.get_attribute('src'))
#         videoXPath = '//*[@id="root"]/div/div[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div/div[1]/video/source'
#         for tag in driver.find_element_by_xpath(videoXPath):
#             videoLinksList.append(tag.get_attribute('src'))
#             logger.info("Video link : " + tag.get_attribute('src'))
    except :
        logger.error("Cannot parse the link : " + link)
#         logger.error("Exception caught is : " )

for link in imageLinksList:
    urllib.request.urlretrieve(link, 'images/' + link.split('/')[-1])
    logger.info("Image saved to : images/" + link.split('/')[-1])
# for link in videoLinksList:
#     urllib.request.urlretrieve(link, 'videos/' + link.split('/')[-1])
