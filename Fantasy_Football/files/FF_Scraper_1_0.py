#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
import time
import numpy as np


# In[2]:


def load_Driver():
    return Firefox(executable_path='geckodriver.exe')
    


# In[3]:


def get_webpage(week):
    webpage="https://fantasy.espn.com/football/leaders?statSplit=singleScoringPeriod&scoringPeriodId={}".format(week)
    return webpage


# In[4]:


def get_players():
    players=[]
    players_raw=driver.find_elements_by_class_name("player-column__athlete")
    for player in players_raw:
        players.append(player.text.split("\n")[0])
    return players


# In[5]:


def get_rush_yds():
    rush_yds=[]
    rush_yds_raw=driver.find_elements_by_xpath("//*[@title='Rushing Yards']")
    for rush_yd in rush_yds_raw:
        if not rush_yd.text == "YDS":
            rush_yds.append(rush_yd.text)
    return rush_yds


# In[6]:


def get_pass_yds():
    pass_yds=[]
    pass_yds_raw=driver.find_elements_by_xpath("//*[@title='Passing Yards']")
    for pass_yd in pass_yds_raw:
        if not pass_yd.text == "YDS":
            pass_yds.append(pass_yd.text)
    return pass_yds


# In[7]:


def get_rec_yds():
    rec_yds=[]
    rec_yds_raw=driver.find_elements_by_xpath("//*[@title='Receiving Yards']")
    for rec_yd in rec_yds_raw:
        if not rec_yd.text == "YDS":
            rec_yds.append(rec_yd.text)
    return rec_yds


# In[8]:


def get_rush_tds():
    rush_tds=[]
    rush_tds_raw=driver.find_elements_by_xpath("//*[@title='TD Rush']")
    for rush_td in rush_tds_raw:
        if not rush_td.text == "TD":
            rush_tds.append(rush_td.text)
    return rush_tds


# In[9]:


def get_pass_tds():
    pass_tds=[]
    pass_tds_raw=driver.find_elements_by_xpath("//*[@title='TD Pass']")
    for pass_td in pass_tds_raw:
        if not pass_td.text == "TD":
            pass_tds.append(pass_td.text)
    return pass_tds


# In[10]:


def get_rec_tds():
    rec_tds=[]
    rec_tds_raw=driver.find_elements_by_xpath("//*[@title='TD Reception']")
    for rec_td in rec_tds_raw:
        if not rec_td.text == "TD":
            rec_tds.append(rec_td.text)
    return rec_tds


# In[11]:


def get_pass_ints():
    pass_ints=[]
    pass_ints_raw=driver.find_elements_by_xpath("//*[@title='Interceptions Thrown']")
    for pass_int in pass_ints_raw:
        if not pass_int.text == "INT":
            pass_ints.append(pass_int.text)
    return pass_ints


# In[12]:


def get_fumls():
    fumls=[]
    fumls_raw=driver.find_elements_by_xpath("//*[@title='Total Fumbles Lost']")
    for fuml in fumls_raw:
        if not fuml.text == "FUML":
            fumls.append(fuml.text)
    return fumls


# In[13]:


def next_page():
    button=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div[5]/div[2]/div[2]/div/div/div/div/div/button[2]")
    button.click()
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "player-column__athlete")))


# In[14]:


def go_to_first_page():
    button=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div[5]/div[2]/div[2]/div/div/div/div/div/div/ul/li[1]")
    button.click()
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "player-column__athlete")))


# In[15]:


def accept_cookies():
    button=driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']")
    button.click()
    WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CLASS_NAME, "player-column__athlete")))


# In[16]:


def read_player_file():
    players_file=open("../Team.txt", 'r')
    players=players_file.read().split("\n")
    players_file.close()
    players=[player for player in players if player != ""]
    return players
    


# In[17]:


def get_data():
    wanted_players=read_player_file()
    
    page=1
    players=[]
    
    pass_yds=[]
    rush_yds=[]
    rec_yds=[]
    
    pass_tds=[]
    rush_tds=[]
    rec_tds=[]
    
    pass_ints=[]
    fumls=[]
    
    go_to_first_page()
    while page<=22:
        print("searching on page {} of 22".format(page))
        
        players+=get_players()
        
        pass_yds+=get_pass_yds()
        rush_yds+=get_rush_yds()
        rec_yds+=get_rec_yds()
        
        pass_tds+=get_pass_tds()
        rush_tds+=get_rush_tds()
        rec_tds+=get_rec_tds()
        
        pass_ints+=get_pass_ints()
        fumls+=get_fumls()
        
        next_page()
        page+=1
        
        
        if all(elem in players  for elem in wanted_players):
            print("all players found")
            break
    
    
    ff_score=[]
    for player in wanted_players:
        i=players.index(player)
        score= float(rec_yds[i])/10+float(rush_yds[i])/10+float(pass_yds[i])/25+float(pass_tds[i])*4+float(rush_tds[i])*6+float(rec_tds[i])*6-2*float(pass_ints[i])-2*float(fumls[i])
        ff_score.append([player,str(score)])
    
    return(ff_score)


# In[18]:


def print_file(data):
    f = open("../ff_score.txt", "w")
    f.write("Player\t\tScore\n----------------------------------------------\n")
    for d in data:
        f.write(d[0])
        f.write("\t")
        f.write(d[1])
        f.write("\n")
    f.close()


# In[20]:


week = int(input("Requested Week "))
driver=load_Driver()
driver.get(get_webpage(week))
WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

accept_cookies()

print_file(get_data())

driver.close()


# In[ ]:




