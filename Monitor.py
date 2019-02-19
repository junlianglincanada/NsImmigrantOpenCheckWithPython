#from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#import time
import smtplib
import datetime
#from email import encoders
#from email.message import Message
#from email.mime.audio import MIMEAudio
#from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apscheduler.schedulers.blocking import BlockingScheduler

from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('no-sandbox')

siteLoginName = ""
siteLoginPassword = ""
outlookAccountEmail = ""
outlookAccountPassword = ""
outlookFromEmail = ""
outlookToEmail = "" # use , to seperate multiple email address

def check_job():
    #driver = webdriver.PhantomJS()
    driver = webdriver.Chrome(options=options)
    thing_url = "https://accesstobusiness.snsmr.gov.ns.ca/a2b_web/portal/home.jsf"
    driver.get(thing_url)
    login = driver.find_element_by_partial_link_text("Login")
    login.click()
    username = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(siteLoginName)
    login = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "login-button")))
    login.click()
    password = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(siteLoginPassword)
    login = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "login-button")))
    login.click()
    immiUrl = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"Immigrate")))
    driver.execute_script("arguments[0].click();", immiUrl)
    apply = ui.WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,"Apply Now")))
    driver.execute_script("arguments[0].click();", apply)
    driver.implicitly_wait(10)
    driver.find_elements_by_class_name("icon-green-arrow")[4].click()
    applyList = driver.find_elements_by_class_name("icon-green-arrow")
    opened = 1
    if len(applyList)>0:
        opened = 2
    else:
        opened = 1
    currentDT = datetime.datetime.now()
    if (opened == 2):
        print("start to send email " + currentDT.strftime("%Y-%m-%d %H:%M:%S"))
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(outlookAccountEmail, outlookAccountPassword)
        msg = MIMEMultipart()
        message = '''
                NS Demand: Express Entry (Category B) is opened right now!
            '''
        message +=  currentDT.strftime("%Y-%m-%d %H:%M:%S")
        msg['From'] = outlookFromEmail
        msg['To'] = outlookToEmail
        msg['Subject'] = "NS Demand: Express Entry (Category B) is opened right now!"
        msg.attach(MIMEText(message, 'plain'))
        # send the message via the server set up earlier.
        server.send_message(msg)
        server.quit()
    else:
        print("not open at " + currentDT.strftime("%Y-%m-%d %H:%M:%S"))
    driver.quit()


scheduler = BlockingScheduler()
scheduler.add_job(check_job,'interval',minutes=5)
scheduler.start()