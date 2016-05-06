#!/usr/bin/python
# _*_ coding: utf-8 _*_

import os
import sys
import re
import xml.etree.ElementTree as ET
import configparser

#---- XML読込
tree = ET.parse('program_data.xml')
root = tree.getroot()
root.findall(".")

#---- コンフィグ読込
cfg = configparser.ConfigParser()
cfg.read("./pythonini.cfg")

#---------------------------------------
# Xpathを利用してXMLからデータを取得する
#---------------------------------------
def XpathGet(xpath):
   ret = root.findall(xpath)
   for lin in ret:
      print("Xpath:{}".format(lin.text))


#----- main -----
if __name__ == '__main__':

   # Xpathを利用してXMLからデータを取得する
   XpathGet(cfg.get('program','bkd1') + "/param")
   XpathGet(xpath="./program/[@name='bkd2']/param")
   XpathGet(xpath="./program/[@name='bkd3']/param")

   print("-"*10)
   XpathGet(cfg.get('program','bkd1') + "/param")
   XpathGet(cfg.get('program','bkd1') + "/opt")
   XpathGet(cfg.get('program','bkd1') + "/mem")
   XpathGet(cfg.get('program','bkd1') + "/norlogfile")
   XpathGet(cfg.get('program','bkd1') + "/errlogfile")
   print("-"*10)
   XpathGet(cfg.get('program','bkd2') + "/param")
   XpathGet(cfg.get('program','bkd2') + "/opt")
   XpathGet(cfg.get('program','bkd2') + "/mem")
   XpathGet(cfg.get('program','bkd2') + "/norlogfile")
   XpathGet(cfg.get('program','bkd2') + "/errlogfile")
