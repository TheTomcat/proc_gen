from Point import Point
import json
import random
import math
import sys
import numpy
import bisect

CI_Mag_file = "D:\\Github\\proc_gen\\celest.csv"
bbRGB_file = "D:\\Github\\proc_gen\\bbcolour.txt"
bbRGB2_file = "D:\\Github\\proc_gen\\bbcolour2.txt"
exomass_file = "D:\\Github\\proc_gen\\exomass.txt"

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

def extract_exomass(listed_file=exomass_file):
    output = []
    with open(listed_file, 'r') as f:
        for row in f.read().split('\n'):
            if row == '':
                continue
            output.append(float(row))
    return output

def saveData(float_list, json_file):
    with open(json_file, 'w') as f:
        json.dump(float_list, f)

def loadData(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def run_extractors():
    celest_data = extract_colourIndex_and_Magnitude()
    bb_data = extract_BlackBody2_to_RGB()
    exo_mass_data = extract_exomass()
    saveData((celest_data, bb_data, exo_mass_data), json_file)


# Load the json data
celest_data,bb_data,exo_mass_data = loadData(json_file)

Earth = {"mass":5.97219E24,
         "density":5.510E3,
         "T_surface":288,
         "v_esc":11.19E3,
         "radius":6378100}

Sun = {"mass":1.989E30,
       "luminosity":3.846E26}

M_e = 5.97219E24
M_ej_rat = 317.828133 
M_j = M_e*M_ej_rat
M_s = 1.989E30
G = 6.67E-11
L_s = 3.846E26 # Luminosity of the Sun
AU = 149597870.7
planet_mass_cat_num = [0.00001,0.1,0.5,2,10,50]
planet_mass_cat_lab = ["Asteroidean","Mercurian","Subeterran",
                       "Terran","Superterran","Neptunian","Jovian"]
planet_TPHC_num = [i+273 for i in [-50,0,50,100]]
planet_TPHC_lab = ["Hypopsychroplanet","Psychroplanet","Mesoplanet",
                   "Thermoplanet","Hyperthemoplanet"]

planet_HZC_num = [-1, 0, 1, 2]
planet_HZC_lab = ["Iron", "Rocky-iron", "Rocky-water", "Water-gas", "Gas"]

def getRange(x, num, lab):
    if x <= num[0]:
        return lab[0]
    if x >= num[-1]:
        return lab[-1]
    return lab[bisect.bisect(num,x)]

massCat = lambda x: getRange(x, planet_mass_cat_num, planet_mass_cat_lab)
TPHC = lambda x: getRange(x, planet_TPHC_num, planet_TPHC_lab)
HZC_Class = lambda x: getRange(x, planet_HZC_num, planet_HZC_lab)


def tohex(RGB):
    return '#'+''.join([hex(i)[-2:] for i in RGB]).upper()

# Number of planet (geometric distribution)
def geom(rnd, mu=1.6):
    p=1/(1+mu)
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

log = lambda x: math.log(x,10)

ESI = lambda x, p: (1 - math.fabs((x-1)/(x+1)))**p
ESI_T = lambda x: (1 - math.fabs((x-288)/(x+288)))**0.179

def albedo(RandomObject):
    A = -1
    while not (0 <= A <= 1):
        A = RandomObject.normalvariate(0.3375,0.1696)
    return A

def window(x,a=0,b=None):
    if b is None:
        b=x+1
    if a<=x<=b:
        return x
    elif x<a:
        return a
    else:
        return b

def exoMassMapping(exomass=None):
    # Make exo_planet regression
    # Map min(exo) ==> 8.7E-5 (Mass of mercury)
    # Map av(ex) ====> 0.176  (Av mass of solar system)
    # Map max(exo) ==> 1.1*max(exo)
    x1,x2,x3 = min(exo_mass_data), sum(exo_mass_data)/len(exo_mass_data), max(exo_mass_data)
    X = numpy.matrix([[x1**2,x1,1],
                     [x2**2,x2,1],
                     [x3**2,x3,1]])
    Y = numpy.matrix([[8.7E-5],[0.176],[1.1*x3]])
    Z = numpy.linalg.solve(X,Y)
    if exomass is None:
        return lambda x: window(float(Z[0])*x*x+float(Z[1])*x+float(Z[2]),x1*0.95)
    else:
        return window(float(Z[0])*exomass*exomass+float(Z[1])*exomass+float(Z[2]),x1*0.95)

exo_mass_mapping = exoMassMapping()

class OrbitingBody(object):
    def __init__(self, semi_major_axis, orbital_period):
        """Class that stores information about orbiting bodies"""
        self.a = semi_major_axis
        self.T = orbital_period

class Star(object):
    def __init__(self, pos=0, seed=None):
        if seed is None:
            seed = random.randint(0,sys.maxsize)
            
        self.R = random.Random(seed)
        self.R.seed(seed)

        self.seed = seed
        
        self.abs_mag,self.colour_index = self.R.choice(celest_data)
        self.colour_index *= percent(5,self.R.random())
        self.abs_mag *= percent(5,self.R.random())

        self.relative_luminosity = 10 ** ((self.abs_mag-4.83)/-2.5)
        self.luminosity = self.relative_luminosity*Sun["luminosity"]
        self.numPlanets = geom(self.R.random())

        X = self.R.normalvariate(0.0325746201, 0.2708663696)
        
        self.metallicity = X - log(2.6)+log(self.numPlanets+1)

        E = (0.0049*self.metallicity-0.288)*self.colour_index-0.002*self.metallicity + 3.941
        self.temperature = 10**E

        self.mass = 0.967*self.luminosity**0.255 + (5.19E-5)*self.luminosity - 0.0670
        
        sigma = 5.670373E-8
        self.radius = math.sqrt(self.luminosity / (4*math.pi*self.temperature**4*sigma))

        self.RGB = bb_interpolate(self.temperature)
        dT = self.temperature-5700
        self.HzInner = (0.720-2.76E-5*dT-3.81E-9*dT**2)*math.sqrt(self.relative_luminosity)
        self.HzOuter = (1.77-1.38E-4*dT-1.43E-9*dT**2)*math.sqrt(self.relative_luminosity)

        self.HZD = lambda R: (2*R-self.HzOuter-self.HzInner)/(self.HzOuter-self.HzInner)
        self.Planets = []
        for n in range(self.numPlanets):
            self.Planets.append(Planet(self, seed=(self.R.random(),)))
        self.Planets.sort(key=lambda key: key.semi_major_axis)
##    def normalisePlanetaryOrbits(self, ):
##        
    def pprint(self, Recursive=False):
        output = ["                    Seed : {}".format(self.seed),
                  "    Colour Index (B-V)_0 : {}".format(self.colour_index),
                  "  Absolute Magnitude M_v : {}".format(self.abs_mag),
                  "      Orbiting Planets n : {}".format(self.numPlanets),
                  "            Luminosity L : {}".format(self.luminosity),
                  "      Metallicity [Fe/H] : {}".format(self.metallicity),
                  "           Temperature T : {}".format(self.temperature),
                  "      Relative Mass M/M0 : {}".format(self.mass),
                  "                Radius R : {}".format(self.radius),
                  "                Colour C : {}".format(self.RGB),
                  "Habitable Zone HZ_i,HZ_o : {},{}".format(self.HzInner, self.HzOuter)]
        print("\n".join(output))
        if Recursive:
            for planet in self.Planets:
                planet.pprint(Recursive)

class Planet(object):
    def __init__(self, star, seed=None):
        self.star = star
        if seed is None:
            seed = random.randint(0,sys.maxsize)
            
        self.R = random.Random(seed)
        self.R.seed(seed)

        self.seed = seed
        m = self.R.choice(exo_mass_data) # Given in multiples of mass of jupiter

        m *= percent(10, self.R.random())

        m = exo_mass_mapping(m) # Take input in m_j, return output in m_j
        self.mass = m * M_j  # [kg]
        d = 1.06E9*(self.mass**(-0.222))
        self.density = d* percent(35, self.R.random())
        self.radius = (3*self.mass/(4*math.pi*self.density))**(1/3)
        a = (0.453*self.mass**0.494) * 14.0184
        self.semi_major_axis =a* percent(10,self.R.random())

        self.orbital_period = math.pi*2*math.sqrt(self.semi_major_axis**3/(G*(self.mass*M_j+self.star.mass*M_s)))
        self.albedo = albedo(self.R)

        self.T_effective = self.star.temperature*math.sqrt(star.radius/(2*self.semi_major_axis))*(1-self.albedo)**(1/4)

        self.T_surface = self.T_effective * (1 + self.albedo*0.517)

        self.escape_velocity = math.sqrt(2*G*self.mass/self.radius)

        self.surface_grav = (self.mass/self.radius**2)/(Earth['mass']/Earth['radius']**2)
        
    def pprint(self, Recursive=False):
        output = ["                 Seed : {}".format(self.seed),
                  "                 Mass : {}".format(self.mass),
                  "                            ({} Earths)".format(round(self.mass/Earth['mass'],5)),
                  "              Density : {}".format(self.density),
                  "               Radius : {}".format(self.radius),
                  "                            ({} Earths)".format(round(self.radius/Earth['radius'],5)),
                  "      Semi-major Axis : {}".format(self.semi_major_axis),
                  "       Orbital Period : {}".format(self.orbital_period),
                  "               Albedo : {}".format(self.albedo),
                  "Effective Temperature : {}".format(self.T_effective-273),
                  "  Surface Temperature : {}".format(self.T_surface-273),
                  "      Escape velocity : {}".format(self.escape_velocity),
                  "      Surface Gravity : {}".format(self.surface_grav),
                  "----------------Classifications----------------",
                  "           Mass class : {}".format(self.seed),
                  "                T-PHC : {}".format(self.seed),
                  "         Thermal Zone : {}".format(self.seed),
                  "       HZ Composition : {}",
                  "        HZ Atmosphere : {}",
                  "          HZ Distance : {}",
                  "------------Earth Similarity Index-------------",
                  "           ESI_Radius : {}",
                  "          ESI_Density : {}",
                  "          ESI_esc_vel : {}",
                  "             ESI_Temp : {}",
                  " =======>ESI : {}"]
        print("\n".join(output))


Q = Star(seed=2705244738682445531)
