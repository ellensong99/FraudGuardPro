# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 00:39:20 2023

@author: Lydia
"""

## Scrape the 419 scam emails from website "https://www.419scam.org/emails/index.htm"
from bs4 import BeautifulSoup 
import requests
import pandas as pd
url = "https://www.419scam.org/emails/index.htm"
response = requests.get(url)
urls=[]
if response.status_code == 200:
    with open('urls.txt', 'w') as f:
        f.write(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    dates = soup.find_all('a', href=lambda href: href and "419" not in href and "20" in href)
    for i in dates:
        href=i.get("href")
        if len(href) > 17:
            url = "https://www.419scam.org/emails/" + href
            #print(url)
            urls.append(url)
            
scam={}
dfBuilder = []
for url in urls:
    if "2019-02" not in url: #Change this text in demo 
        continue
    else:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            contents = soup.find_all('a', href=lambda href: href and href[0].isdigit())
            for i in contents:
                href=i.get("href")
                email=url[:-9]+href
                print(email)
                response = requests.get(email)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    content = soup.find_all("blockquote")
                    d={}
                    msg = ""
                    los=str(content).split("<br/>")
                    print(content)
                    try:
                        for s in los:
                            if "Reply-To" in s:
                                extract = s.split("</b>")[1]
                                if ";" in extract:
                                    extract = extract.split(";")[1][:-3]
                                d["Sender"] = extract
                            elif "Subject" in s:
                                d["Subject"] = s.split("</b>")[1][1:]
                            elif "<b>" not in s and "blockquote" not in s:
                                msg+=s
                        d["content"] = msg
                        scam[s]= d
                        dfBuilder.append([d["Sender"],d["Subject"], d["content"]])
                    except:
                        pass
                else:
                    print("Failed to retrieve the webpage. Status code:", response.status_code)
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
        
df = pd.DataFrame(dfBuilder, columns=["Sender", "Subject", "Content"])
#df.to_csv("419_2019_02.csv")
