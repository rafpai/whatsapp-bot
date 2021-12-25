#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
from selenium.webdriver import PhantomJS

import tkinter as tk
from tkinter import ttk

import time
import datetime


# In[2]:


FONT=("Verdana", 12)


# In[3]:


def load_Driver():
    #return Firefox(executable_path='WebDrivers/geckodriver.exe')
    return PhantomJS(executable_path='C:/Users/Rafael/Desktop/Börse/WebDrivers/phantomjs.exe')
    


# In[4]:


driver=load_Driver()


# In[5]:


webpage="https://aktienkurs-orderbuch.finanznachrichten.de/tui1.htm"
driver.get(webpage)



def get_StockPrice():
    Kurs=driver.find_element_by_id("additionalOfferInformation_152").text
    Kurs=Kurs.split(' ')[0]
    Kurs=float(Kurs.split(',')[0])+float(Kurs.split(',')[1])*0.001
    return Kurs


# In[6]:


def popup(msg):
    popup = tk.Tk()
    popup.wm_title("!Börse!")
    label = ttk.Label(popup, text=msg, font=FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


# In[ ]:


MyVolume=100
MyPrice=3.36
BrokerFee=10.22
Investment=MyVolume*MyPrice+BrokerFee

Alerts=[False,False,False,False,False,False,False]
t = time.localtime()
today=datetime.date.today().weekday()
print(today)
T_min=t.tm_min+60*t.tm_hour
Kurs=get_StockPrice()

def give_Alert(Kurs,Alerts):
    A=0

    if (0.5*Investment/MyVolume>=Kurs):
        if (not Alerts[0]):
            Alerts[0]=True
            A=-0.5
    if (0.8*Investment/MyVolume>=Kurs):
        if (not Alerts[1]):
            Alerts[1]=True
            A=-0.8
    if (Investment/MyVolume<=Kurs):
        if (not Alerts[2]):
            Alerts[2]=True
            A=1           
    if (1.5*Investment/MyVolume<=Kurs):
        if (not Alerts[3]):
            Alerts[3]=True
            A=0.5
    if (2*Investment/MyVolume<=Kurs):
        if (not Alerts[4]):
            Alerts[4]=True
            A=2
    if (3*Investment/MyVolume<=Kurs):
        if (not Alerts[5]):
            Alerts[5]=True
            A=3
    if (4*Investment/MyVolume<=Kurs):
        if (not Alerts[6]):
            Alerts[6]=True
            A=4

    if (A != 0):
        text="Aktie bei {} * Investment \nGewinn: {}".format(A, round(Kurs*MyVolume-Investment,2))
        popup(text)




if (today != 5 and today != 6):       
    popup("Tagesstartkurs={} \nGewinn: {}".format(Kurs, round(Kurs*MyVolume-Investment,2)) )       

    while (T_min<1080 and T_min>540):
        t = time.localtime()
        T_min=t.tm_min+60*t.tm_hour
        
        Kurs=get_StockPrice()
        give_Alert(Kurs,Alerts)
        time.sleep(300)

    popup("Tagesendkurs={} \nGewinn: {}".format(Kurs, round(Kurs*MyVolume-Investment,2)) )
else:
    popup("Wochenende \nletzter Tagesendkurs={} \nGewinn: {}".format(Kurs, round(Kurs*MyVolume-Investment,2)) )
driver.quit()            


# In[ ]:




