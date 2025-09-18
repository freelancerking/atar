#Required scope: files:write    
#Invite bot to channel: /invite @botname

HACKER_GROUP = 'Warlock'   
IMAGES_DIR = './Images'   
JSON_DIR = './json' 
SLACK_TOKEN = 'xoxb-1595657012006-7231095552162-JF5xT2Wi3eWLiKZ2Fu7yBh8j'   #From OAuth & Permissions
CHANNEL_ID = 'C01JE842AKS'  
APOLLO_KEY = '38SCQiDOokUgmIKqDI-XLA'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
import time
import requests
import base64
from datetime import datetime   
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import warnings
from ransomware import *

warnings.filterwarnings("ignore")

FILENAME = 'LOG.txt'

''' send_to_wordpress() moved to ransomware.py '''  

def post_image(message, file_name): 
    result = slack_client.files_upload_v2(
        channels=CHANNEL_ID,
        initial_comment=message,
        file=file_name,
    )
    return result

def savehtml(filename, html):
    f = open(filename, "w", encoding="utf8")
    f.write(html)
    f.close()

def get_text_between(start_text, end_text, html):
    start = html.find(start_text)
    if start >= 0:
        start += len(start_text)
        end = html.find(end_text, start)
        if end >= 0:
            return html[start:end]
    return ""       

def extract_domain(mytext):
    myregex = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
    return re.findall(myregex, mytext)[0]    
   
if not os.path.exists(FILENAME):
    os.mknod(FILENAME)

slack_client = WebClient(token=SLACK_TOKEN)

# set up Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=socks5://localhost:9050')
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors");
options.add_argument('--headless')
custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
options.add_argument(f'user-agent={custom_user_agent}')
options.binary_location="./headless-chromium"
service = webdriver.chrome.service.Service(executable_path='./chromedriver')
driver = webdriver.Chrome(options=options, service=service)
#driver = webdriver.Chrome(options=options)
driver.maximize_window()

# load the web page
url = f'http://elqfbcx5nofwtqfookqml7ltx2g6q6tmddys6e25vgu3al2meim6cbqd.onion/'
driver.get(url)

# wait for the page to load
time.sleep(30)

driver.find_element(By.XPATH,"//button[text()='ok']").click()
time.sleep(2)

json_file = f'{JSON_DIR}/{HACKER_GROUP}-{datetime.now().strftime("%m%Y")}.json' 
    
existing_content = []
with open(FILENAME, "r") as file:
    existing_content = [line.strip() for line in file]

with open(FILENAME, "a") as file:    
    json_data = []    
    if os.path .exists(json_file):
        with open(json_file) as f:
            json_data = json.load(f)

    start = time.time()     #for limiting posts to 50 per hour
    count = 0
    for result in driver.find_elements(By.XPATH,"//div[@class='client-card']"):     
        company_name = result.find_element(By.XPATH, ".//h2").text.strip()

        if company_name not in existing_content:
            print("New Victim: " + company_name)
            existing_content.append(company_name)   
            file.write(company_name + "\n")

            name_apollo, country, city, address, revenue, industry, web = get_apollo_data2(company_name)    
            victim = web       

            post_link = ''        
            description = ''
            try:
                dt = datetime.now().strftime("%Y-%m-%d-%H%M%S")      
                screenshot_name = f'{IMAGES_DIR}/{HACKER_GROUP}-{dt}.png'   
                driver.save_screenshot(screenshot_name) 
                message = f'################### New Victim {HACKER_GROUP} ###################\nGroup Name: {HACKER_GROUP}\nVictim Name: {web}\nPost Link: {post_link}\n#######\nPost Text: {description[0:100]}\n#######\nCompany Name: {company_name}\nIndustry: {industry}\nCountry: {country}\nCity: {city}\nAddress: {address}\nAnnual Revenue: {revenue}\n################### END New Victim {HACKER_GROUP} ###################'                               
                post_image(message, screenshot_name) 
                json_data.append({
                    "group": HACKER_GROUP, 
                    "date": dt, 
                    "victim": web,
                    "post_link": post_link,
                    "description": description,
                    "company_name": company_name,   
                    "industry": industry,
                    "country": country,
                    "city": city,
                    "address": address,
                    "annual_revenue": revenue,
                    "image": screenshot_name
                })  
                send_to_wordpress(web, screenshot_name, company_name, HACKER_GROUP, description, industry, country, post_link)             
                count += 1  
                end = time.time()
                if count >= 50 and end - start < 3600: #if we reach 50 posts in less than 1 hour, we stop scraping            
                    exit()
            except Exception as e:  
                print(e)
        #end if victim not in existing_content:
    #end for result in driver.find_elements(By.XPATH,"//div[@class='publication-wrapper']"):    
driver.quit() 

with open(json_file, 'w') as fp:
    json.dump(json_data, fp, indent=4)
