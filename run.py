'''
- Put all targets(domain names) in target.txt without http/https. for ex.(blindf.com)
- Create an empty urls.txt file in the same folder
- Run this script.
- The script will take 1 target at a time from the target.txt and save all wayback urls in the urls.txt file. Then this script
will call html_injection_check.py file and perform attack.
- This process will be continued until reaches End of line of the target.txt
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import os
import re

read_target = open("target.txt","r")
for target in read_target:
    user_input = target

    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
    target_url = "https://web.archive.org/cdx/search/cdx?url=*."+user_input+"/*&output=text&fl=original&collapse=urlkey"
    wayback_result= requests.get(target_url, headers=header, verify=False)
    soup = BeautifulSoup(wayback_result.text,'html.parser')

    #Saving wayback urls to urls.txt file
    write_urls_to_file = open("urls.txt", "w+", encoding='utf-8')
    write_urls_to_file.write(unquote(soup.prettify()))
    write_urls_to_file.close()

    #reading urls from the urls.txt Line by line:
    read_urls = open("urls.txt", "r", encoding='utf-8')
    read_urls = read_urls.readlines()

    blacklist = [".png",".ico",".jpg",".css",".js",".txt",".JPG",".PNG",".jpeg",".JPEG",".ttf",".svg",".wp-json",".gif","wp-content"]
    whitelist = ["?","%3F"]

    def empty():
        return 0

    write_url = open("urls.txt", "w", encoding='utf-8')

    for line in read_urls:
        if any(word in line for word in blacklist):
             empty()
        elif any(word in line for word in whitelist):
            if re.match("http", line):          # check http/https in the beginning of the line
                write_url.write(line)
                print(line)
            else:
                print("false")
    write_url.close()
    os.system('python3 html_injection_check.py')  #HTML inj. check for the current urls in urls.txt
read_target.close()

