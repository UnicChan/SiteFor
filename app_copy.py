from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bases import Base, Comments
from sqlalchemy import delete
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
from time import sleep

engine = create_engine("sqlite:///base.db")
session = sessionmaker(bind=engine)
s = session()

# r = s.query(Comments).all()
# for element in r:
#     print(element.name)



while True:
    url = "https://vk.com/topic-133638473_39796848?offset=0"
    headers = {
       'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    amount = soup.find('span', class_="ui_crumb_count").text

    stmt = delete(Comments)
    s.execute(stmt)
    s.commit()

    for p in range (0, int(amount), 20):
        # print(p)

        url = f"https://vk.com/topic-133638473_39796848?offset={p}"
        r = requests.get(url, headers=headers)
        sleep(3)
        
        soup = BeautifulSoup(r.text, 'lxml')

        com_all = soup.findAll('div', class_="bp_post clear_fix")

        for comment in com_all:
            name = comment.find('a', class_="bp_author").text
            name_href = comment.find('a', class_="bp_author").get('href')
            text_post = comment.find('div', class_="bp_text").text

            urlm = f"https://vk.com{name_href}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            }
            m = requests.get(urlm, headers=headers)
            soupm = BeautifulSoup(m.text, 'lxml')    
            #print(soup)
            avatar = soupm.find('img', class_="page_avatar_img")
            if name_href == "/clubpoparim":
                avatar = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgPZzRIn2horWiaCYTWJjefDbiM0kgtwrxmyqiCRktHWxNu0W-XyuL7twLryhJGYmvXuv87DAJ5UK86ViqokiZPczsfMyh5qzjpQNOa-C5jAcBUds1ooKuGDZlavEcmMIX06xjGUpQNm5WQc1p7HP38F3rVqj0odn_00A71-7xFTgg19khrpIH8u2sG/s320/awd.png"
            elif (avatar is None) or (soupm.find('img', class_="page_avatar_img").get('src') == "/images/deactivated_hid_200.gif"):
                avatar = "http://sun9-48.userapi.com/s/v1/if1/LdZgHQt3nzZty23xg9DOZG2vU3AGbV1Y5Uq-hkQDhlnq7JdF9Dpu16a5VthMfIRpa4BuSC-V.jpg?size=200x200&quality=96&crop=0,0,400,400&ava=1"
            else:
                avatar = soupm.find('img', class_="page_avatar_img").get('src')



            comments = Comments(name=name, name_href=name_href, text_post=text_post, avatar=avatar)
            s.add(comments)
            s.commit()
    sleep(600)