from bs4 import BeautifulSoup as Soup
import json
import requests
from common import *

entries = []
WEBSITE = 'http://www.sbjf.org/sbjco/schmaltz/yiddish_phrases.htm'
SITE_TITLE = "SBJF"
source_object = {"site":WEBSITE, "title":SITE_TITLE}


def main():
    parseSBJF()

def parseSBJF():
    response = requests.get(WEBSITE)
    page = Soup(response.content, "lxml")
    stack = [page]
    while(len(stack)>0):
        node = stack.pop()
        for child in node.contents:
            if child.name == 'small':
                parseList(child)
            elif child.name:
                stack.append(child)
    print("Done")
def parseList(node):
    entry = {"language":"Yiddish", "english":[], "hebrew":[]}
    entryDone = False
    foundTerm = False
    breaklineCount = 0;
    for line in [line for line in node.contents if line.name or len(line.strip())>0]:
        if line.name == "em":
            continue
        if line.name == "br":
            breaklineCount += 1
            if breaklineCount>1:
                entryDone=True
            continue
        else:
            breaklineCount = 0
        if entryDone:
            if len(entry["english"])>0 and not entry["english"][0].endswith("csulb") and not entry["english"][0].startswith("email"):
                addEntry(entry)
            entry = {"language":"Yiddish", "english":[], "hebrew":[]}
            entryDone = False
            foundTerm = False
        if not foundTerm:
            split = line.split(":", 1)
            term = split[0]
            foundTerm = True
            for t in term.split("/"):
                entry["english"].append(t.strip().lower())
            if len(split) > 1:
                entry["definition"] = [{"text":split[1].strip(),"source":source_object}]
            else:
                pass
        else:
            if "definition" in entry:
                entry["definition"][0]["text"] += " "+line.strip()
            else:
                entry["definition"] = [{"text":line.strip(),"source":source_object}]
    addEntry(entry)

if __name__ == '__main__':
    main()