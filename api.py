import requests
from pprint import pprint
from dotenv import load_dotenv
import os
import sys
import itertools
from flask import Flask, request
from flask import jsonify
import requests
import os
import urllib 
from flask_cors import CORS
load_dotenv()

key =  os.getenv('PROJECT_API_KEY')

# dictionary = {
#     "tree": [{"item": 'branch'}, {"item": 'leaves'}, {"item": 'squirrel'}],
#     "garden": [{"item": 'branch'}, {"item": 'gnome'}, {"item": 'vegetation'}],
#     "olive": [{"item": 'martini'}, {"item": 'branch'}, {"item": 'sodium'}],
#     "apple": [{"item": 'cider'}, {"item": 'newton'}],
#     "autumn": [{"item": 'leaves'}, {"item": 'fall'}, {"item": 'season'}, {"item": 'halloween'}, {"item": 'branch'}],
#     "pumpkin": [{"item": 'halloween'}, {"item": 'branch'}]
# }
# dictionary = {
#     "tree": getAssociatedWords("tree"),
#     "garden": getAssociatedWords("garden"),
#     "olive": getAssociatedWords("olive")
# } 

def getAssociatedWords(word):
    res = requests.get('https://api.wordassociations.net/associations/v1.0/json/search?apikey=' + key +'&text=' + word + '&lang=en&limit=300')
    res = res.json()
    res = res['response'][0]['items']
    return res

def handleArgs(words):
    dictionary = {}
    for word in words:
        dictionary[word] = getAssociatedWords(word)
    return dictionary

def findGroupings(words):
    groupings = []
    for i in range(1, len(words)):
        groupings.extend(list(itertools.combinations(words, i+1)))
    return groupings

def solve(dictionary):
    solution = {}
    words = []
    for i in dictionary:
        words.append(i)
    groupings = findGroupings(words)
    for g in groupings:
        matches = []
        for i in range(0, len(g)-1):
            a = dictionary[g[i]]
            for j in range(i+1, len(g)):
                b = dictionary[g[j]]
                similiar = []
                for c in a:
                    for d in b:
                        if c["item"] == d["item"]:
                            similiar.append(c)
                
                matches.append(similiar)
        true = []
        if len(matches) != 0:
            initial = matches[0]
            matches.pop(0)
            for i in initial:
                found = True
                for j in matches:
                    if i not in j:
                        found = False
                if found == True:
                    true.append(i)
        k = ""
        for i in g:
            k += i + " "
        solution[k] = true
    return solution

app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods=['POST'])
def main():
    data = request.get_json()
    words = data["words"]
    dictionary = handleArgs(words)
    return jsonify(solve(dictionary))

if __name__ == '__main__':
    app.run()
