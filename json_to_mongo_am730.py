import pymongo
import glob
import json
from urllib.parse import unquote


collection = "am730Documents"
user = "charleschen"
password = "pass903"


database = "nlpDocuments"
host = '10.6.126.128:32774'

client = pymongo.MongoClient(host, username=user, password = password, authSource=database);

mydb = client[database]
mycol = mydb[collection]



urls = []
for document in mycol.find():
    if document['url'] not in urls:
        urls.append(document['url'])
    else:
        print("Duplicates found. {}".format(document['url']))
        mycol.delete_one(document)
   


for f_name in glob.glob('./downloaded/daily_docs_jun_24/*.json'):
    f = open(f_name, "r")
    
    for x in f:
        y = json.loads(x)
        url = unquote(y['url'])
        cat = url.strip().split("/")
        
        if len(cat) == 5:
            pass
        elif len(cat) == 6:
            y['category'] = cat[4].replace(".", "/")
        else:
            print("bad category")
        mycol.insert_one(y);





