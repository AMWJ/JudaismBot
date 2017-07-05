from bs4 import BeautifulSoup as Soup
import json
import re
import requests
from common import *
from nltk.corpus import words

entries = []
WEBSITE = 'http://www.mechon-mamre.org/jewfaq/glossary.htm'
SITE_TITLE = "Mechon Mamre"
source_object = {"site":WEBSITE, "title":SITE_TITLE}


def main():
    parseMechonMamre()

def parseMechonMamre():
    response = requests.get(WEBSITE)
    page = Soup(response.content, "lxml")
    stack = [page]
    while(len(stack)>0):
        node = stack.pop()
        for child in node.contents:
            if child.name == 'dl':
                parseList(child)
            elif child.name:
                stack.append(child)
    print("Done")
def parseList(node):
    entry = {"language":"Hebrew", "english":[]}
    entryDone = False
    foundTerm = False
    for line in [line for line in node.contents if line.name or len(line.strip())>0]:
        if line.name == "dt":
            parseTerm(entry, line.text)
        else:
            breaklineCount = 0
        if entryDone:
            if len(entry["english"])>0 and not entry["english"][0].endswith("CSULB") and not entry["english"][0].startswith("email"):
                addEntry(entry)
            entry = {"language":"Yiddish", "english":[]}
            entryDone = False
            foundTerm = False
        if not foundTerm:
            split = line.split(":", 1)
            term = split[0]
            foundTerm = True
            for t in term.split("/"):
                entry["english"].append(t.strip().lower())
            if len(split) > 1:
                entry["definition"] = {"text":split[1].strip(),"source":source_object}
            else:
                pass
        else:
            if "definition" in entry:
                entry["definition"]["text"] += " "+line.strip()
            else:
                entry["definition"] = {"text":line.strip(),"source":source_object}

def parseTerm(entry, term):
    if(term.startswith("Kohein")):
        pass
    else:
        matches = re.findall("([a-zA-Z-'\d][a-zA-Z- '\d]+)(?: \(([^;\)]*)(;[^;\)]*)*\))?(;|$)",term)
        return matches[0][0]
if __name__ == '__main__':
    main()