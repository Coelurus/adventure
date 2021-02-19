#predem stanoveny rozmer, nahodne typy mistnosti a monster

import random

krysa = {"name":"krysak","hp":5,"dmg":5}
ptak = {"name":"ptak","hp":5,"dmg":4}
dement = {"name":"dement","hp":5,"dmg":3}
monsters = [krysa,ptak,dement]
locations = ["mistnost","mucirna","chodba"]

WORLD_HEIGHT = 1
WORLD_WIDTH = 2

column = []
row = []

class Lokace:
    
    def __init__(self, monster, location):
        self.room = location
        if self.room == "chodba":
            self.monster = None
        else:
            self.monster = monster
        self.fog = True
        
        if self.room == "stena":
          self.lockedDoor = random.choice([True, False])

    def explore(self):
        self.fog = False

    def getDict(self):
        return self.monster

def createRow():
    a = []
    for x in range(WORLD_HEIGHT):
        a.append(Lokace(random.choice(monsters), random.choice(locations)))
    return a

for y in range(WORLD_HEIGHT):
    column.append([])
    column[y] = createRow()

for y in range(len(column)):
    x = 0
    for j in column[y]:
        print("X ", x + 1)
        print("Y ", y + 1)
        print(j.room)
        print(j.monster)
        print()
        x += 1

'''
def play(x,y,u):
    d = column[y][x].monster
    if u == True:
        print(d, "pred utokem")
        print("provedeni utoku")
        d["hp"] = d["hp"] - 1
        print(d, " po utoku")
    else:
        print(d, "nic se nestalo")

print("mistnost 1")
play(0,0,True)
print()
print("mistnost 2")
play(1,0,False)
print()
print("mistnost 1")
play(0,0,False)

print()
print(column[0][0].getDict(), " pouzitelna metoda na return slovniku do random kodu")
print(column[0][1].getDict(), " pouzitelna metoda na return slovniku do random kodu")
'''