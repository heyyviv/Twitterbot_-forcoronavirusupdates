import tweepy
import time
import requests
import json
from bs4 import BeautifulSoup
import lxml

CONSUMER_KEY='xxxx'#key
CONSUMER_SECRET='xxxx'#sectetkey
ACCESS_KEY='xxxxxxxxx'#acesskey
ACCESS_SECRET='xxxxxx'#secret accesskey

auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api=tweepy.API(auth)
#mentions=api.mentions_timeline()
#"dict_keys(['_api', '_json', 'created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'source', 'source_url'," \
#" 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', " \
#"'in_reply_to_screen_name', 'author', 'user', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', " \
#"'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang'])"
FILE_NAME='log_details.txt'


def see_last_seen(fname):
    last_seen=open(fname,'r')
    last_id=int(last_seen.read().strip())
    last_seen.close()
    return last_id



def store_last_seen(fname,last_id):
    last_seen=open(fname,'w')
    last_seen.write(str(last_id))
    last_seen.close()
    return


#main function
def reply_to_tweet():
    #replying to mention tweet
    last_seen_id=see_last_seen(FILE_NAME)
    mentions=api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id=mention.id
        store_last_seen(FILE_NAME,last_seen_id)
        if '@username' in mention.full_text.lower():
            print("tweeting",flush=True)
            api.update_status('@'+mention.user.screen_name+"Thanks buddy ",mention.id)
    #tweet to twitter account
    url='https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data'
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'lxml')
    #result=soup.find_all(id='thetable')
    result=soup.find('table',attrs={'class':"wikitable"}).tbody
    rows=result.find_all('tr')
    col=[v.text.replace("\n"," ") for v in rows[0].find_all('th')]
    #print(col)
    info={}
    for i in range(2,21):
        datas=rows[i].find_all('td')
        pp=rows[i].find('a')
        info[pp.text]=[]
        if len(datas)==4:
            info[pp.text].append(datas[0].text.replace("\n"," "))
            info[pp.text].append(datas[1].text.replace("\n"," "))
            info[pp.text].append(datas[2].text.replace("\n"," "))

            #value=[datas[0].text.replace("\n"," "),datas[1].text.replace("\n"," "),datas[2].text.replace("\n"," ")]
            #print(value)
    #print(info)
    dialogue=" In India Confirm ->"+str(info['India'][0])+" Death ->"+str(info['India'][1])+" Recoverd ->"+str(info['India'][2])
    api.update_status(status =dialogue)



while(True):
    reply_to_tweet()
    time.sleep(7200)
