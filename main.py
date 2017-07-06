import praw
import json
import pymongo
import datetime
import re
import sentence_splitter
from markdown import markdown
from trie import Trie
from bs4 import BeautifulSoup as Soup

COMMENT_FRACTION = .2   #For any given opportunity to comment, this bot only this number of times.
                        #This is a measure to ensure the bot is not too annoying, at least initially.

terms = {}
trie = Trie()
last_db_update = datetime.datetime.now()
termsCollection = None
hour = datetime.timedelta(hours = 1)
wordRegex = re.compile("\S+")
alphaNumericRegex = re.compile("\w")

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
    subreddit = reddit.subreddit('Judaism')
    comment_stream = subreddit.stream.comments(pause_after=2)
    inbox_stream = reddit.inbox.stream(pause_after=0)
    while True:
        for comment in comment_stream:
            if comment is None:
                break
            matches = [match for match in process_comment(comment)]
            for match in matches:
                sentence, start, end, term = match
                sentence = sentence[:start]+"**"+sentence[start:end]+"**"+sentence[end:]
                print(sentence)
        
        if datetime.datetime.now() - last_db_update > hour:
            update_terms_list()

        for message in inbox_stream:
            if message is None:
                break
            parse_message(message)

def process_comment(comment):
    for find in process_body(comment.body):
        yield find

def process_body(body):
    global terms
    termsFound = set()
    sentences = sentence_splitter.split_into_sentences(removeMarkdown(body))
    for sentence in sentences:
        indices = []
        node = trie
        words = list(wordRegex.finditer(sentence))
        i = 0
        while i<len(words):
            match = words[i]
            stripped = strip(match.group())
            if stripped in node.hash:
                indices.append((match.start(),match.end()))
                node = node.hash[stripped]
            else:
                phrase = None
                while node.parent is not None:
                    if node.phrase is not None:
                        if terms[node.phrase]["_id"] not in termsFound:
                            start = indices[0][0]
                            end = indices[-1][1]
                            l_offset, r_offset = strip_nonalnum(sentence[start:end])
                            yield (sentence, start+l_offset, end+r_offset, terms[node.phrase])
                            termsFound.add(terms[node.phrase]["_id"])
                        indices = []
                        node = trie
                        i-=1
                    else:
                        indices.pop()
                        node = node.parent
                        i-=1
            i+=1


def update_terms_list():
    global terms
    terms = {}
    for term in termsCollection.find({}):
        for spelling in term["english"]:
            terms[spelling] = term
            trie.add(spelling)
        for spelling in term["hebrew"]:
            terms[spelling] = term
            trie.add(spelling)

def parse_message(message):
    pass

def strip(phrase):
        phrase = re.sub('[^A-Za-z0-9 ]+', '', phrase)
        return re.sub('\s+',' ', phrase).lower()

def removeMarkdown(md):
    html = markdown(md)
    return ''.join(Soup(html, "lxml").findAll(text=True))

def strip_nonalnum(word):
    for start, c in enumerate(word):
        if c.isalnum():
           break
    for end, c in enumerate(word[::-1]):
        if c.isalnum():
           break
    return (start, -end)

if __name__ == '__main__':
    main()