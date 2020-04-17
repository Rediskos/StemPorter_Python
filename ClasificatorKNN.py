import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import numpy as np
import math
from tqdm import tqdm
import corr
import StemPorter 

def corr_text(text):
    ans = ""
    
    for i in text.splitlines():
        for j in i.split():
            j = StemPorter.Stem(j)
            j = corr.checkWord(j)
            j = j.lower()
            ans += j.strip()
            if(len(j) > 0 and j != " "):
                ans += " "
    return ans

Base = {}
AllPoints = []

# dict [x,y,z]:class
def loadBase():
    with open("BD_Med_Sport_Math/Sport/SportPoints.txt", "r", encoding = "utf-8") as inpt:
        for i in inpt.readlines():
            tmp = i.split()
            Base[i.strip()] = "Sport"
            AllPoints.append(tmp)
            
    with open("BD_Med_Sport_Math/Med/MedPoints.txt", "r", encoding = "utf-8") as inpt:
        for i in inpt.readlines():
            tmp = i.split()
            Base[i.strip()] = "Med"
            AllPoints.append(tmp)
            
    with open("BD_Med_Sport_Math/Math/MathPoints.txt", "r", encoding = "utf-8") as inpt:
        for i in inpt.readlines():
            tmp = i.split()
            Base[i.strip()] = "Math"
            AllPoints.append(tmp)
            

def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    
    return corr_text(root.text).split()
            
def calcScore(url, text = False):
    if(text == False):
        tmp = get_text(url)
    else:
        tmp = url
    
    tmp = [i.strip() for i in tmp]
    
    SportScore = 0
    BioScore = 0
    MathScore = 0
    cnt = 0
    
    for i in SportTerms:
        CountWords = tmp.count(i)
        if CountWords != 0:
            SportScore += CountWords
    
    for i in BiosTerms:
        CountWords = tmp.count(i)
        if CountWords != 0:
            BioScore += CountWords
    
    for i in MathTerms:
        CountWords = tmp.count(i)
        if CountWords != 0:
            MathScore += CountWords
    
    
    All = SportScore + BioScore + MathScore
    
    return [SportScore / All * 100, BioScore / All * 100, MathScore / All * 100]
    
def norma(a, b):
    ans = 0
    for i in range(3):
        ans += float(a[i]) * float(b[i]) * float(a[i]) * float(b[i])
    return ans


SportTerms = []
with open("BD/Sport/SportTerms.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            SportTerms.append(j)

MathTerms = []
with open("BD/Math/RealMathTerms.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            MathTerms.append(j)
            
BiosTerms = []
with open("BD/Biologic/RealBio.txt", "r", encoding = "utf-8") as ST:
    for i in ST.readlines():
        for j in i.split():
            BiosTerms.append(j)

print("OUT")

loadBase()

SPORT = "BD_Med_Sport_Math/Sport/"
MEDIC = "BD_Med_Sport_Math/Med/"
MATH = "BD_Med_Sport_Math/Math/"
LABELS = {SPORT:0, MEDIC: 1, MATH: 0}
FORLOSS = {0: "Sport", 1:"Med", 2:"Math"}

loss = 0

for label in LABELS:
    for f in tqdm(os.listdir(label)):
        
        if("Point" in f):
            pass
        else:
            path = os.path.join(label, f)
            for k in range(len(AllPoints), 0, -1)
            with open(path, "r", encoding = "utf-8") as inpt:
                for url in tqdm(inpt.readlines()):
                    scors = {"Sport":0, "Med":0, "Math":0}
                                        
                    url = url.strip()
                    target = calcScore(url, text = False)
                    
                    
                    tmp = sorted(AllPoints, key = lambda x: norma(x, target))
                    
                    #print(tmp)
                    
                    cnt = 2
                    maxv = 0
                    maxName = ""
                    
                    for i in tmp:
                        word = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
                        scors[Base[word]] += 100 / math.log(norma(i, target))
                        if(maxv < scors[Base[word]]):
                            maxv = scors[Base[word]]
                            maxName = Base[word]
                    if(maxName != FORLOSS[LABELS[label]]):
                        loss+= 1
print("Loss is ", loss)