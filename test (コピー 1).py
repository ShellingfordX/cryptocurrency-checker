#!/usr/bin/env python
# -*- coding: utf-8 -*-

#sudo apt-get install python-gi
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

#sudo apt-get install gir1.2-appindicator3-0.1
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3

#sudo apt-get install python-requests
import requests

#Ctrl+C で終了するため
import signal

import os

#sudo apt install -y python-configparser
import configparser

APPINDICATOR_ID = "myappindicator"
CONFIG_PATH = os.path.expanduser('~') + "/デスクトップ/config"
ICON = os.path.dirname(os.path.realpath(__file__)) + "/bitcoin.png"

class MyIndicator():

    def __init__(self):
        self.menu=Gtk.Menu()
        self.ind=AppIndicator3.Indicator.new(APPINDICATOR_ID, "/usr/share/linuxmint/logo.png", AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        label=self.get_price()
        self.ind.set_label(label, "")

        #更新間隔の設定と繰り返し処理
        self.interval=1 # in seconds
        GLib.timeout_add_seconds(self.interval, self.handler_timeout)
        
        self.build_menu()
        

        
    def build_menu(self):
    
        
        item=[" "] * 3
        item[0]=Gtk.MenuItem()
        item[0].set_label("Settings")
        item[0].connect("activate",self.handler_menu_exit)
        item[0].show()
        self.menu.append(item[0])
        
        item[1]=Gtk.MenuItem()
        item[1].set_label("About")
        item[1].connect("activate",self.handler_menu_about)
        item[1].show()
        self.menu.append(item[1])
        
        item[2]=Gtk.MenuItem()
        item[2].set_label("Exit")
        item[2].connect("activate",self.handler_menu_exit)
        item[2].show()
        self.menu.append(item[2])
        
        self.menu.show()
        self.ind.set_menu(self.menu)
        
    def handler_menu_reload(self, evt):
        self.handler_timeout()
    
    def handler_timeout(self):
        l=self.get_price()
        self.ind.set_label(l, "")
        GLib.timeout_add_seconds(self.interval, self.handler_timeout)
        
        
    def handler_menu_about(self, source):
        dialog=Gtk.AboutDialog()
        dialog.set_program_name("コインチェックチェッカー")
        dialog.set_version("0.1")
        dialog.set_copyright("Copyright 2018 221B Baker Street")
        dialog.set_comments("A usefull indicator that displays in the task tray how much your choice of cryptocurrency is.")
        dialog.set_website('http://baker-street.jugem.jp')
        dialog.run()
        dialog.destroy()
    
    def handler_menu_exit(self, evt):
        Gtk.main_quit()
        
    def get_price(self, pair="btc_jpy"):
        url = "https://coincheck.com/api/rate/"+pair
        response = requests.get(url)
        json = response.json()
        if pair == "btc_jpy":
            crypt = "BTC"
            self.ind.set_icon(ICON)
        return crypt + ":" + json["rate"] + " Yen"
        
"""
class DialogWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.set_defualt_size(250,150)
        self.set_border_with(6)
        
        button=Gtk.Button("OK")
        button.connect("clicked",self.on_button_clikced)
        self.add(button)
        
    def on_button_clicked(self,widget):
        pass
"""

    

        
win = MyIndicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
print(config["SETTINGS"]["Cryptocurrency"])

Gtk.main()


