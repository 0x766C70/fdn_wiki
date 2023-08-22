#!/usr/bin/env python
# coding: utf8

# @uthor belette 
# version v.0.2

## import
import requests
import json
import os
import stat
import socket
import argparse
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
import datetime
import uuid
import time
import calendar
import urllib3
urllib3.disable_warnings()

## argurments check
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action='version', version='%(prog)s : version v.0.1')
parser.add_argument("-c", "--create", action='store_const', const='create', dest='funct', help='create variables', metavar='')
parser.add_argument("-u", "--update", nargs='*', dest='update', help='update Cachet component')
parser.add_argument("-g", "--get", action='store_const', const='get', dest='funct', help='retrieve component status')
parser.add_argument("-d", "--debug", help='debug level', action='store_const', const='debug', metavar='')

whattodo = parser.parse_args()
args, leftovers = parser.parse_known_args()

if args.update is not None :
  if len(whattodo.update) != 5:
    parser.error("Please use this synthax: cagios.py --update HOSTNAME SERVICENAME STATUS STATUSTYPE OUTPUT ")

if args.debug is not None :
  logging.basicConfig(level=logging.DEBUG)
  logging.getLogger("requests").setLevel(logging.DEBUG)
else :
  logging.basicConfig(level=logging.INFO)
  logging.getLogger("requests").setLevel(logging.WARNING)

## variables
def writevar(name,value):
  write = {name:value}
  try:
    with open('var.json', 'a') as var:
      json.dump(write, var)
      var.write(os.linesep)
      var.close()
  except IOError as e:
    logger.info("impossible to write var.json, please check permission/disk space...")
    exit(1)
def readvar(name,file):
  data = []
  with open(file, 'r') as var:
    for line in var:
       data.append(json.loads(line))
    for key in data:
      if name in key:
        return key[name]

def defvariables():
  if calendar.timegm(time.gmtime()) - calendar.timegm(time.localtime()) != 0:
    print("Your system is in UTC?")
  logpath = input("Full path to write JSON data: ")
  while logpath is '':
    logpath = input("Please enter Full path to write JSON data: ")
  if logpath.endswith("/"):
    writevar("logpath",logpath)
  else:
    writevar("logpath",logpath + "/")
  baseURL = input("Cachet API url: ")
  while baseURL is '':
    baseURL = input("Please enter Cachet API url: ")
  writevar("baseURL",baseURL)
  apikey = input("API Key: ")
  while apikey is '':
    apikey = input("Please enter API key: ")
  writevar("apikey",apikey)
  incprefix = input("Incident Prefix: ")
  while incprefix is '':
    incprefix = input("Please enter the Incident Prefix: ")
  writevar("incprefix",incprefix)
  logger.info("var.json created successfully")

## logging
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
handler = logging.FileHandler(readvar("logpath","var.json") + "cagios.log")
logger.addHandler(handler)
handler.setFormatter(formatter)

if whattodo.update is not None:
  component = whattodo.update[0]
  service = whattodo.update[1]
  status = whattodo.update[2]
  status_type = whattodo.update[3]
  severite = whattodo.update[4]

## http methods
def getRequest(url):
  logger.debug("url is " + str(url) + "\n")
  request = requests.get(url)
  logger.debug("HTTP GET response is " + str(request) + "\n")
  return request

def putRequest(url, data):
  logger.debug("url is " + str(url) + "\n")
  sessionCookie = readvar("apikey","var.json")
  #headers = {'X-Cachet-Token':sessionCookie, 'Accept': 'application/json'}
  headers = {'X-Cachet-Token':sessionCookie}
  request = requests.put(url, headers = headers, json = data)
  logger.debug("HTTP PUT response is " + str(request) + "\n")
  return request

def postRequest(url, data):
  logger.debug("url is " + str(url) + "\n")
  sessionCookie = readvar("apikey","var.json")
  headers = {'X-Cachet-Token':sessionCookie, 'Accept': 'application/json'}
  request = requests.post(url, headers = headers, json = data)
  logger.debug("HTTP POST response is " + str(request) + "\n")
  return request

## monitoring
def monitoring():
  url = readvar("baseURL","var.json") + "ping"
  response = requests.get(url)
  json_response = json.loads(response.text)
  if json_response['data'] == "Pong!":
    logger.debug("Connectivity OK")
  else:
    logger.debug("Connectivity issue")
    print("Il semblerait que Cachet ne reponde pas :(")

## components 
def getComponentsList():
  url = readvar("baseURL","var.json") + "components?per_page=100"
  response = getRequest(url)
  json_response = json.loads(response.text)
  logger.debug("Components list is " + str(json_response) + "\n")
  result = ""
  for key in json_response['data']:
    component_name = key['name']
    component_status = key['status_name']
    if "rationnel" in key['status_name']:
      component_status = "OK"
    result += component_name + " [" + component_status + "]\n"
  return result

def getComponentId(component):
  url = readvar("baseURL","var.json") + "components?per_page=100"
  response = getRequest(url)
  json_response = json.loads(response.text)
  logger.debug("Components list is " + str(response.text) + "\n")
  for key in json_response['data']:
    component_name = key['name']
    component_id = key['id']
    if component_name == component:
      logger.debug("Component id is " + str(component_id) + "\n")
      return component_id

def updateComponent(component,status):
  url = readvar("baseURL","var.json") + "components/" + str(getComponentId(component))
  data = {"status": status}
  response = putRequest(url, data)
  json_response = json.loads(response.text)
  logger.debug("Components update" + str(json_response) + "\n")
  print(response.text)

## execution scheme
try:
  with open('var.json') as file:
    logger.debug("read var.json")
except IOError as e:
  if whattodo.funct is 'create':
    logger.debug("var.json doesn't exist or not accessible trying to create a fresh var.json file now...")
  else:
    logger.info("var.json doesn't exist or not accessible please check permission or run 'cagios.py --create'")
    exit(1)
if whattodo.funct is 'create':
  try:
    os.remove('var.json')
  except OSError:
    pass
  defvariables()
  monitoring()
elif whattodo.funct is 'get':
  monitoring()
  getComponentsList()
elif whattodo.update is not None:
  monitoring()
  updateComponent(component,status)
