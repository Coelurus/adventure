
#mapa se nahodně vytvari pri chuzi

import random

krysa = {"name":"krysak","hp":5,"dmg":5}
ptak = {"name":"ptak","hp":5,"dmg":4}
dement = {"name":"dement","hp":5,"dmg":3}
monsters = [krysa,ptak,dement]
locations = ["mistnost","mucirna",]

patro = {}
#print(len(patro))

class Lokace:
    
    def __init__(self, monster, room):
        
        self.room = room
        if self.room == "chodba" or self.room == "start":
            self.monster = None
            self.lock = None   
        else:
            self.monster = monster
            
        self.fog = True
        self.lock = random.choice([True, False])

    def getMonster(self):
        return self.monster

y, x = 0, 0
patro[str(y) +","+ str(x)] = Lokace("", "start")

"""
print(len(patro))
print(patro[str(y) +","+ str(x)].monster)

x += 1

patro[str(y) +","+ str(x)] = Lokace(random.choice(monsters), random.choice(locations))
print(len(patro))
print(patro[str(y) +","+ str(x)].monster)

patro["3,1"] = Lokace(random.choice(monsters), random.choice(locations))
patro["3,-1"] = Lokace(random.choice(monsters), random.choice(locations))
patro["1,3"] = Lokace(random.choice(monsters), random.choice(locations))
patro["1,-3"] = Lokace(random.choice(monsters), random.choice(locations))
patro["-2,2"] = Lokace(random.choice(monsters), random.choice(locations))
patro["0,-1"] = Lokace(random.choice(monsters), random.choice(locations))
patro["-1,-2"] = Lokace(random.choice(monsters), random.choice(locations))
patro["2,1"] = Lokace(random.choice(monsters), random.choice(locations))

def play(y,x,u):
    d = patro[str(y) +","+ str(x)].monster
    if u == True:
        print(d, "pred utokem")
        print("provedeni utoku")
        d["hp"] = d["hp"] - 1
        print(d, " po utoku")
    else:
        print(d, "nic se nestalo")

play(y,x,True)
play(y,x,False)
play(y,x,True)
"""

def mapa(patro):
    y = []
    x = []
    for key in patro.keys():
        coor = key.split(",")
        print(coor)
        
        cy = int(coor[0])
        cx = int(coor[1])

        y.append(cy)
        x.append(cx)

    print("y")
    for i in y:
        print(i,end=" ")
    print()
    print("x")
    for i in x:
        print(i,end=" ")

    print()
    print("__________")

    souradnice = {}
    
    while min(y) < 0:
        for i in range(len(y)):
            y[i] += 1
            
    while min(x) < 0:
        for i in range(len(x)):
            x[i] += 1

    for i in range(len(y)):
        if y[i] in souradnice:
            ar = souradnice.get(y[i])
            ar.append(x[i])
            souradnice[y[i]] = ar
        else:
            a = []
            a.append(x[i])
            souradnice[y[i]] = a

    print(souradnice)
    print(max(y))
    print(max(x))
    mapa = ""
    for i in range(max(y)+1):
        svitek = ""
        #print("y", i,end=" ")
        #print("a",souradnice[i])
        for j in range(max(x)+1):
            #print("j",j,end=" ")
            if j in souradnice[i]:
                #print("r",end=" ")
                svitek += "R "
            else:
                #print("_",end=" ")
                svitek += "_ "
        #print("")
        mapa = svitek + "\n" + mapa
    print(mapa)
    
print()
print("..............")
mapa(patro)    
            