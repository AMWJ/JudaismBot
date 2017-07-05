from bs4 import BeautifulSoup as Soup
import json
import re
import requests
from common import *
from nltk.corpus import words

entries = []
WEBSITE = 'https://raw.githubusercontent.com/JudaismBot/JudaismBot/master/tooltip_dictionary/tooltip_dictionary_v0.9.txt'
SITE_TITLE = "Judaism Tooltip"
source_object = {"site":WEBSITE, "title":SITE_TITLE}


def main():
    parseTooltip()

def parseTooltip():
    response = requests.get(WEBSITE)
    entryDone = False
    foundTerm = False
    for line in [line for line in response.content.splitlines() if len(line)>0]:
        versions = set([''])
        parenOptions = []
        braceOptions = ""
        inBraces = False
        line_string = line.decode("utf-8")
        i = 0
        while True:
            c = line_string[i]
            if c == ',':
                break
            elif c == '(':
                parenOptions.append("")
                i+=1
            elif c == '[':
                inBraces = True
                i+=1
            elif c == ')':
                if line_string[i+1]=='?':
                    versions = set([version+option for version in versions for option in parenOptions]).union(versions)
                    parenOptions = []
                    i+=2
                else:
                    versions = set([version+option for version in versions for option in parenOptions])
                    parenOptions = []
                    i+=1
            elif c == ']':
                if line_string[i+1]=='?':
                    versions = set([version+option for version in versions for option in braceOptions]).union(versions)
                    braceOptions = ''
                    inBraces = False
                    i+=2
                else:
                    versions = set([version+option for version in versions for option in braceOptions])
                    braceOptions = ''
                    inBraces = False
                    i+=1
            elif c == '|':
                parenOptions.append("")
                i+=1
            elif c == '$':
                i+=1
            elif len(parenOptions)>0:
                parenOptions[-1]+=c
                i+=1
            elif inBraces:
                braceOptions += c
                i+=1
            else:
                if line_string[i+1]=='?':
                    versions = set([version+c for version in versions]).union(versions)
                    i += 2
                else:
                    versions = set([version+c for version in versions])
                    i += 1
            versions = set([version.replace("'","") for version in versions])
        entry = {"language":"Hebrew", "english":list(versions), "hebrew": [],"definition": [{"text":line_string[i+1:],"source":source_object}]}
        addEntry(entry)
    print("Done")

if __name__ == '__main__':
    main()