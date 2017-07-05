import praw
import json
import pymongo
import datetime
import re
import sentence_splitter

COMMENT_FRACTION = .2   #For any given opportunity to comment, this bot only this number of times.
                        #This is a measure to ensure the bot is not too annoying, at least initially.

terms = {}
last_db_update = datetime.datetime.now()
termsCollection = None
hour = datetime.timedelta(hours = 1)

def main():
    global terms
    global last_db_update
    global termsCollection
    file = open("keys.conf", "r")
    conf = json.loads(file.read())
    client_id = conf["client_id"]
    client_secret = conf["client_secret"]
    reddit_username = conf["reddit_username"]
    reddit_password = conf["reddit_password"]
    db_username = conf["db_username"]
    db_password = conf["db_password"]

    db_uri = 'mongodb://%s:%s@ds032340.mlab.com:32340/judaismterms' % (db_username, db_password)
    database_client = pymongo.MongoClient(db_uri)
    db = database_client.get_default_database()
    termsCollection = db["terms"]
    update_terms_list()

    reddit = praw.Reddit(user_agent = "rJudaismShamash (by u/AMWJ)", client_id = client_id, client_secret=client_secret, username=reddit_username, password=reddit_password)
    print(reddit.user.me())
    subreddit = reddit.subreddit('test+Judaism')
    comment_stream = subreddit.stream.comments(pause_after=2)
    inbox_stream = reddit.inbox.stream(pause_after=0)
    while True:
        for comment in comment_stream:
            if comment is None:
                break
            process_comment(comment)
        
        if datetime.datetime.now() - last_db_update > hour:
            update_terms_list()

        for message in inbox_stream:
            if message is None:
                break
            parse_message(message)

def process_comment(comment):
    global terms
    body = comment.body
    sentences = sentence_splitter.split_into_sentences(body)
    for sentence in sentences:
        stripped_sentence = strip(sentence)
        print(sentence)
        print(stripped_sentence)
        for key in terms.keys():
            if key in stripped_sentence:
                print(stripped_sentence)

def update_terms_list():
    global terms
    terms = {}
    for term in termsCollection.find({}):
        for spelling in term["english"]:
            terms[spelling] = term
        for spelling in term["hebrew"]:
            terms[spelling] = term

def parse_message(message):
    pass

def strip(phrase):
        phrase = re.sub('[^A-Za-z0-9 ]+', '', phrase)
        return re.sub('\s+',' ', phrase).lower()


if __name__ == '__main__':
    main()