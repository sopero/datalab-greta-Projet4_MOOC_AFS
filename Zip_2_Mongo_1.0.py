#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 12:00:46 2019

@author: rousseau
"""

from sqlalchemy import create_engine
from sqlalchemy.sql import text
import glob
import configparser
import requests, pprint
import requests, pprint, os
from demjson import decode
from pymongo import MongoClient # librairie qui va bien
import zipfile, json, ast

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"


# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

bdd = client['MOOC_GRP_AFS'] # BDD "Datalab" de mongoDB sur serveur
bdd
print("'MOOC_GRP_AFS' Collections:")
for cn in bdd.list_collection_names():
    print("-"+cn)
collec = client['MOOC_GRP_AFS']['Fun_Mooc5']

'''
base = "https://www.fun-mooc.fr/courses/"
course = "course-v1:UPSUD+42001+session12"
post = "be3e32ab79b94365915554010e643d35/threads/5d7947d71c89dcf269014846"


#exit()

response = requests.get(
    base+course+"/discussion/forum/"+post,
    params={'ajax': 1, 'resp_skip': 0, 'resp_limit': 25},
#    "https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f?ajax=1&resp_skip=0&resp_limit=25",
    #params={'q': 'requests+language:python'},
    #headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    headers={
#        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
#        "Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "LvmImlOzFWNoC8oQbAdPUvlP7a4ab3KZ",
        "X-Requested-With": "XMLHttpRequest",
#        'Referer': 'https://www.fun-mooc.fr/courses/course-v1:UPSUD+42001+session12/discussion/forum/be3e32ab79b94365915554010e643d35/threads/5d7947d71c89dcf269014846f',
        'Cookie': 'csrftoken=Sj6GTIlFiUpaAZ4YihKE4UDPw5ViKpUh; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2227077206-e813-458b-90f0-77afefc55917%22%2C%22options%22%3A%7B%22end%22%3A%222020-11-02T09%3A14%3A36.186Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; acceptCookieFun=on; sessionid=yfcfkaa0ddcrhoinizoood03zu1w9jmb; edxloggedin=true; edx-user-info="{\"username\": \"sperrotDL\"\054 \"version\": 1\054 \"email\": \"perrot.sondra@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/sperrotDL\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'
    },
)


print(response.content)
#pprint.pprint(response.json())
'''

list = glob.glob("/home/rousseau/Projet4/zips/*zip")

print(list)
#~ exit()

for zip in list:
    print("-"+zip)
    zf = zipfile.ZipFile(zip, 'r') # le ZIP
#    n=0
    for zipName in zf.namelist():
        txt = zf.read(zipName).decode("utf-8")
        try:
            x = ast.literal_eval(txt)
#            pprint.pprint(x)
            flag = 'username' in x['content']
#            print(zipName+": "+x['content']['title']+", "+str(flag))
            #~ break
            collec.insert_one(x)
        except SyntaxError:
            print("erreur de lecture du fichier",zipName)
            #pass
#collec = client['MOOC_GRP_AFS']['FunF5']    
        #collec.insert_one(x)
        
NivMax = 0

def applat(mesg, niv):
    global NivMax
    l = len(mesg['body'])
    username = 'anonymous'
    if 'username' in mesg: username = mesg['username']
    #c = len(mesg['endorsed_responses']+mesg['non_endorsed_responses'])

    #~ pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=mesg['username'])
    childs = [] # liste des enfants
    if 'children' in mesg: childs += mesg['children']
    if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
    if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
    for child in childs:
#        applat(child+l, niv+1)
        l+=applat(child,niv+1)
    #print("nombre de caractères cumulés ",l)
    if niv > NivMax:
        NivMax = niv
    print("%s %s %s : %s = %d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], username,len(mesg['body']),l))
    return l

cursor = collec.find()
for doc in cursor:
    if 'content' in doc:
        #~ pprint.pprint(doc)
        print("-------------------------------")
        longueur = applat(doc['content'], 0)
        #~ print(longueur)q

print("Niv max=%d" % NivMax)
#collec = client['MOOC_GRP_AFS']['Fun_Mooc5']         
#collec.insert_one(response.json())        
collec.insert_one(x,{'ordered' : False})
