from Point import Point
import json
import random
import math

CI_Mag_file = "D:\\Github\\proc_gen\\celest.csv"
bbRGB_file = "D:\\Github\\proc_gen\\bbcolour.txt"
bbRGB2_file = "D:\\Github\\proc_gen\\bbcolour2.txt"

json_file = "D:\\Github\\proc_gen\\celest.json"

def extract_colourIndex_and_Magnitude(csv_file=CI_Mag_file):
    tonum = lambda x: [float(i) for i in x]
    output = []
    with open(csv_file,'r') as f:
        for row in f.read().split("\n"):
            row = row.split(",")
            try:
                row = [float(i) for i in row]
            except ValueError:
                continue
            output.append(row)
    return output

def extract_BlackBody_to_RGB(htmlFile=bbRGB_file):
    tonum = lambda x: [int(i) for i in x]
    data = []
    with open(htmlFile, 'r') as f:
        for row in f.read().split("\n"):
            row = row[33:52].split("K  #")
            row[0] = int(row[0])
            data.append(row)
    return data

def extract_BlackBody2_to_RGB(tableFile=bbRGB2_file):
    tonum = lambda x: [int(i) for i in x]
    data = []
    with open(tableFile, 'r') as f:
        for row in f.read().split("\n"):
            row = [i for i in row.split(" ") if i != '']
            if row[2]=='2deg':
                data.append(tonum(row[0:1]+row[9:12]))
    return [[i[0] for i in data],[i[1:] for i in data]]


def saveData(float_list, json_file):
    with open(json_file, 'w') as f:
        json.dump(float_list, f)

def loadData(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def run_extractors():
    celest_data = extract_colourIndex_and_Magnitude()
    bb_data = extract_BlackBody2_to_RGB()
    saveData((celest_data, bb_data), json_file)


# Load the json data
celest_data,bb_data = loadData(json_file)

# Number of planet (geometric distribution)
def geom(rnd):
    p=1/(1+1.6)
    # CDF: 1-(1-p)**(n+1)
    # PDF: p*(1-p)**n
    if not (0 < rnd <= 1):
        raise ValueError("Must be in range (0,1]")
    return math.floor(math.log(rnd)/math.log(1-p))

# Random percentage modifier
def percent(percent, rnd=None):
    if rnd is None:
        return lambda rnd: 1 + (0.5-rnd)/(2*percent)
    else:
        return 1 + (0.5-rnd)/(2*percent)

## BB interpolation
def bb_interpolate(temp, bb_data=bb_data):
    if not (bb_data[0][0] <= temp <= bb_data[0][-1]):
        raise ValueError("Temperature "+str(temp)+" out of range.")
    if temp in bb_data[0]:
        i = bb_data[0].index(temp)
        return bb_data[1][i]
    for i,T in enumerate(bb_data[0]):
        if T < temp:
            continue
        scale = (temp - bb_data[0][i-1])/100
        return [int(bb_data[1][i-1][k]+scale*(bb_data[1][i][k]-bb_data[1][i-1][k])) for k in range(3)]


class Star(object):
    def __init__(self, pos=0, seed=None):
        self.R = random.Random()
        self.R.seed(seed)

        self.colour_index, self.abs_mag = self.R.choice(celest_data)
        self.colour_index *= percent(5,self.R.random())
        self.abs_mag *= percent(5,self.R.random())
        
        self.luminosity = 10 ** ((self.abs_mag-4.83)/-2.5)
        self.numPlanets = geom(self.R.random())

        X = self.R.normalvariate(0.0325746201, 0.2708663696)
        self.metallicity = X - math.log(2.6)+math.log(self.numPlanets+1)

        E = (0.0049*self.metallicity-0.288)*self.colour_index-0.002*self.metallicity + 3.941
        self.temperature = 10**E

        self.M_rat = 0.967*self.luminosity**0.255 + (5.19E-5)*self.luminosity - 0.0670
        
        sigma = 5.670373E-8
        self.radius = math.sqrt(self.luminosity / (4*math.pi*self.temperature**4*sigma))

        
    def pprint(self):
        output = ""


        
