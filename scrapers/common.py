import pymongo
import json

termsCollection = None

file = open("keys.conf", "r")
conf = json.loads(file.read())
db_username = conf["db_username"]
db_password = conf["db_password"]
db_uri = 'mongodb://%s:%s@ds032340.mlab.com:32340/judaismterms' % (db_username, db_password)
database_client = pymongo.MongoClient(db_uri)
db = database_client.get_default_database()
termsCollection = db["terms"]


def addEntry(entry):
    existing_term = termsCollection.find_one({"english":{"$in":entry["english"]}})
    if existing_term:
        sources = [term["source"]["title"] for term in existing_term["definition"]]
        if entry["definition"][0]["source"]["title"] not in sources:
            existing_term["english"] = set(existing_term["english"]).union(set(entry["english"]))
            existing_term["hebrew"] = set(existing_term["hebrew"]).union(set(entry["hebrew"]))
            existing_term["definition"] = existing_term["definition"]+entry["definition"]
            existing_term["language"] = entry["language"]
    else:
        termsCollection.insert(entry)