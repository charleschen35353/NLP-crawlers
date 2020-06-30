import pymongo
import glob
import json
from urllib.parse import unquote


collection = "bbcDocuments"
user = "charleschen"
password = "pass903"


database = "nlpDocuments"
host = '10.6.126.128:32774'

client = pymongo.MongoClient(host, username=user, password = password, authSource=database);

mydb = client[database]
mycol = mydb[collection]

#jsons_data = pd.DataFrame(columns=["title", "url" , "content", "category", "lang", "author", "source", "publish"])


for f_name in glob.glob('./downloaded/BBC_news_docs/*.json'):
    f = open(f_name, "r")
    
    for x in f:
        y = json.loads(x)
        url = unquote(y['url'])
        cat = url.strip().split("/")
        if len(cat) == 6:
            c = cat[-1].split("-")[:-1]
            if c == []:
                y['category'] = "undefined"
            else:
                s = ""
                for w in c:
                    s+= w+"-"
                y['category'] = s[:-1]
        else:
            print("bad category")

        mycol.insert_one(y);




