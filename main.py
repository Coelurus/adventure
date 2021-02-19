# D&D game
import random
from termcolor import colored
from colorama import init
init()

mapa = ["pole", "louka", "les","hrad"]  #fakt epická mapa s progresem, musí se předělat

slovnikHrace = {}  #sem se uloží všechno info o hráči
with open("player.txt") as f:
  for line in f:
    key, val = line.split(":")
    val = val.rstrip("\n")
    if key == "inv":
      val = val.split(";")
    slovnikHrace[key] = val
poleInv = slovnikHrace["inv"]

slovnikItemu = {}
with open("items.txt") as g:
  for line in g:
    if line != "\n":
      key, val = line.split(":")
      val = val.rstrip("\n")
      val = val.split("=")
      slovnikItemu[key] = val

slovnikHrace["speed"] = slovnikHrace["baseSpeed"]
slovnikHrace["DMG"] = int(slovnikHrace["baseDMG"]) + int(slovnikItemu[slovnikHrace["lruka"]][1]) + int(slovnikItemu[slovnikHrace["pruka"]][1])
slovnikHrace["armor"] = int(slovnikHrace["baseArmor"]) + int(slovnikItemu[slovnikHrace["helma"]][1]) + int(slovnikItemu[slovnikHrace["torso"]][1]) + int(slovnikItemu[slovnikHrace["kalhoty"]][1])

def encounter(): #vytvoří se pole se slovníky o příšerkách
  soubor = open("entities.txt", "r", encoding="UTF-8")
  radky = soubor.readlines()
  poleMobu = []
  for i in range(int(radky[0])):
    mob = {}
    for line in range(8):
      key, val = radky[line + i * 8 + 1].split(":")
      val = val.rstrip("\n")
      if key == "items":
        val = val.split(",")
      mob[key] = val
    poleMobu.append(mob)
  return poleMobu


def utokHrace(prisera, hrac): #útok hráče
  RNGutok = int(hrac["DMG"]) + random.randint(-int(hrac["DMG"])//5, int(hrac["DMG"])//5)
  if int(prisera["armor"]) >= RNGutok:
    print("   Příšera nezaznamenala", colored("ani škrábnutí.", "red"))
    tah(hrac, prisera)
  else:
    udelenyDamage = RNGutok - int(prisera["armor"])
    prisera["HP"] = int(prisera["HP"]) - udelenyDamage
    print("   Zasáhl jsi příšeru za poškození v hodnotě", colored(str(udelenyDamage) + " DMG", "red"))

    hrac["exp"] = int(hrac["exp"]) + 1

    if int(prisera["HP"]) > 0:
      tah(hrac, prisera)

    else:
      print("   Nepřítel byl drtivě", colored("poražen!", "red"))
      print()
      hrac["exp"] = int(hrac["exp"]) + 5
      mobDrop(prisera, hrac)
      levelUp(hrac)

def mobDrop(prisera, hrac):
  global poleInv
  coDroplo = random.choice(prisera["items"])
  print("Padl vám následující předmět: " + colored(coDroplo, "green"))
  if len(poleInv) == 5:
    print("Máš však všechny kapsy přeplněné těmito předměty: ", end="")
    printItemyInv(poleInv)
    print("Máš tedy možnost předmět vyměnit za jiný[jméno itemu] nebo nechat předmět být[n]", end = "")
    vzit = input(": ")
    if vzit == "n":
      print("Předmět zde zůstane ležet, možná navždy.")
    else:
      vzit = jeTamItem(vzit, poleInv, "")
      poleInv[poleInv.index(vzit)] = coDroplo
  else:
    vzit = input("Chcete ho vzít? Ano[a] / Ne[cokoliv]: ")
    if vzit == "a":
      poleInv.append(coDroplo)
    else:
      print("Předmět zde zůstane ležet, možná navždy.")

def levelUp(hrac): #když hráč porazí příšeru, tak se může vylepšit
  while int(hrac["exp"]) >= int(hrac["level"]) * 10:
    hrac["exp"] = int(hrac["exp"]) - int(hrac["level"]) * 10
    hrac["level"] = int(hrac["level"]) + 1
    print("Jaký stat chcete zlepšit?", colored("Maximální HP", "yellow"),"[h] / ", colored("DMG", "red"),"[d] /", colored("Speed", "blue"), "[s] /",colored("armor", "magenta"), "[a]", end="")
    coVylepsit(hrac)

def coVylepsit(hrac):
  coZlepsit = input(" ")
  print()
  #
  if coZlepsit == "h":
    hrac["MaxHP"] = int(hrac["MaxHP"]) + 3
    hrac["HP"] = int(hrac["HP"]) + 3
    print("   Zlepšilo se ti maximální zdraví na", colored(str(hrac["MaxHP"]) + " HP", "yellow"))
  elif coZlepsit == "d":
    hrac["baseDMG"] = int(hrac["baseDMG"]) + 2
    hrac["DMG"] = int(hrac["DMG"]) + 2
    print("   Zlepšilo se ti základní poškození na", colored(str(hrac["baseDMG"]) + " DMG", "red"))
  elif coZlepsit == "s":
    hrac["baseSpeed"] = int(hrac["baseSpeed"]) + 1
    hrac["speed"] = int(hrac["speed"]) + 1
    print("   Zlepšila se ti základní rychlost na", colored(str(hrac["baseSpeed"]), "blue"))
  elif coZlepsit == "a":
    hrac["baseArmor"] = int(hrac["baseArmor"]) + 1
    hrac["armor"] = int(hrac["armor"]) + 1
    print("   Zlepšila se ti základní odolnost na", colored(str(hrac["baseArmor"]), "magenta"))
  else:
    print("Prosím, opravdu tě to baví? Zadej jednu z požadovaných kláves:", end="")
    coVylepsit(hrac)

def kukNaStaty(prisera, hrac): #Zobrazí se staty
    print("""
    Za svou bojovou kariéru se vaše postava dostala až na level %s.
    Aktuálně máte %s/%s HP.
    Tvoje rychlost je %s, poškození %s a armor %s.
    """%(hrac["level"], hrac["HP"], hrac["MaxHP"], hrac["speed"], hrac["DMG"], hrac["armor"]))
    print(
    """    Příšera se kterou se potýkáš se zve %s a je na %s. levelu.
    V aktuální chvíli má %sHP a odhaduješ že dokáže udělit tak %s DMG.
    Jeho rychlost tipuješ na %s a armor na %s. 
    """%(prisera["name"], prisera["level"], prisera["HP"], prisera["DMG"], prisera["speed"], prisera["armor"]))
    tah(hrac, prisera)

def utek(prisera, hrac):
    if int(hrac["speed"]) > int(prisera["speed"]):
        print("   Takticky jsi ustoupil!")
    else:
        print("   Beháš moc pomalu!")
        tah(hrac, prisera)

def kdoJeRychlejsi(prisera, hrac):
    if int(hrac["speed"]) > int(prisera["speed"]):
        hracJeRychlost = True
    else:
        hracJeRychlost = False
    return hracJeRychlost

def printItemyInv(poleInv):
  text = ""
  for a in poleInv:
    text += colored(a, "cyan") + ", "
  text = text.rstrip(", ")
  print(text)

def pouzitItem(prisera, hrac): #  hrac["inv"]
  global slovnikHrace
  global poleInv
  if len(poleInv) == 0:
    print("V tuto chvíli nemáš v inventáři žádný předmět. Podnikni místo toho něco jiného: ", end="")
    coBudesDelat(prisera, hrac)
  else:
    if len(poleInv) == 1:
      print("V tuto chvíli máš v inventáři následující předmět: ", end="")
      print(colored(poleInv[0], "green"))
    else:
      print("V tuto chvíli máš v inventáři následující předměty: ", end="")
      printItemyInv(poleInv)
    print("Pro použití", colored("itemu","cyan"), end = " ")
    print("[jméno itemu] / vybrat",colored("jinou akci", "yellow"), end = " ")
    pouzijeHo = input("[j]: ")
    pouzijeHo = jeTamItem(pouzijeHo, poleInv, "j")
    print()

    if pouzijeHo == "j":
      print("Nová akce je:", end=" ")
      coBudesDelat(prisera, hrac)
    else:
      useItem(pouzijeHo, hrac, poleInv, prisera)
      tah(hrac, prisera)

def jeTamItem(hledanyItem, poleInv, nebo):
  while hledanyItem not in poleInv or hledanyItem == nebo:
    if hledanyItem == nebo:
      break
    hledanyItem = input("Opravdu to neprojde. Musíte použít jeden z výše uvedených itemů, děkuji. ")
  return hledanyItem

def useItem(item, hrac, poleInv, prisera):
  global slovnikItemu
  if (slovnikItemu[item][2] == "equip"):
    if slovnikItemu[item][3] == "weapon":
      print("Tento předmět si musíš nasadit jako " + colored(slovnikItemu[item][4], "green") + ".")
      print("V momentální době máš v levé ruce předmět " + colored(hrac["lruka"], "cyan") + " a v pravé předmět " + colored(hrac["pruka"],"cyan") + ".")
      print("Kam chceš tedy zbraň nasadit?", colored("Levá ruka", "yellow"), "[l]/", colored("pravá ruka", "yellow"), "[p] / vlastně", colored("nikam", "red"), end = " ")
      kamTeda = input("[n]: ")
      print()
      if kamTeda == "l":
        hrac["lruka"],poleInv[poleInv.index(item)] = poleInv[poleInv.index(item)], hrac["lruka"]
      elif kamTeda == "p":
        hrac["pruka"],poleInv[poleInv.index(item)] = poleInv[poleInv.index(item)], hrac["pruka"]
      else:
        print("Vyber tedy jinou akci: ", end = "")
        coBudesDelat(prisera, hrac)
      hrac["DMG"] = int(hrac["baseDMG"]) + int(slovnikItemu[hrac["lruka"]][1]) + int(slovnikItemu[hrac["pruka"]][1])
    elif slovnikItemu[item][3] == "gear":
      print("Předmět je nutno nasadit do slotu zvaný " + colored(str(slovnikItemu[item][4]),"yellow") + ", kde je momentálně nasazen předmět " + colored(str(hrac[slovnikItemu[item][4]]), "red") + ".")
      if input("Chceš tak učinit? Ano[a] / Ne[n]: ") == "a":
        hrac[slovnikItemu[item][4]],poleInv[poleInv.index(item)] = poleInv[poleInv.index(item)], hrac[slovnikItemu[item][4]]
        hrac["armor"] = int(hrac["baseArmor"]) + int(slovnikItemu[hrac["helma"]][1]) + int(slovnikItemu[hrac["torso"]][1]) + int(slovnikItemu[hrac["kalhoty"]][1])
      print()
    if "žádný" in poleInv: poleInv.remove("žádný")
  else:
    hrac[slovnikItemu[item][0]] = int(hrac[slovnikItemu[item][0]]) + int(slovnikItemu[item][1])
    if int(hrac["HP"]) > int(hrac["MaxHP"]): hrac["HP"] = hrac["MaxHP"]
    if int(slovnikItemu[item][1]) > 0:
      print("   Tvoje " + colored(str(slovnikItemu[item][0]),"red") + " se zvýšilo na " + str(hrac[slovnikItemu[item][0]]) + ".")
    elif int(slovnikItemu[item][1]) < 0:
      print("   Tvoje " + colored(str(slovnikItemu[item][0]),"red") + " se snížilo na " + str(hrac[slovnikItemu[item][0]]) + ".")
    else:
      print("Nic se nestalo...")
    poleInv.pop(poleInv.index(item))

def coBudesDelat(prisera, hrac):
  coDelat = input("")
  print()
  if coDelat == "u":
    utokHrace(prisera, hrac)
  elif coDelat == "s":
    kukNaStaty(prisera, hrac)
  elif coDelat == "z":
    utek(prisera, hrac)
  elif coDelat == "i":
    pouzitItem(prisera, hrac)
  else:
    print("Co je tak těžkého na tom vybrat správné tlačítko? No: ", end="")
    coBudesDelat(prisera, hrac)

def utokPrisery(hrac, prisera):
  if int(hrac["armor"]) >= int(prisera["DMG"]): print("   Trapný pokus nepřítele o útok tě vůbec", colored("nezranil", "red") + ".")
  else: 
    kolikDostal = int(prisera["DMG"]) - int(hrac["armor"])
    hrac["HP"] = int(hrac["HP"]) - kolikDostal
    print("   Zasáhla tě příšera za poškození v hodnotě", colored(str(kolikDostal) + " DMG", "red"))
  print()  

def tah(hrac, prisera):
  global hracJeRychlost
  if hracJeRychlost == False:
    utokPrisery(hrac, prisera)
  else:
    hracJeRychlost = False
  if int(hrac["HP"]) > 0 and int(prisera["HP"]) > 0:
    print("Co hrdinského podnikneš?\nMáš možnost",colored("zaútočit", "red"),"[u] či",colored("shlédnout staty", "yellow"),"[s] či",colored("použít item", "green"),"[i] nebo",colored("zdrhnout", "blue"),"[z]: ", end="")
    coBudesDelat(prisera, hrac)

#gra
print("Milý příteli")
for i in range(len(mapa)):
  if int(slovnikHrace["HP"]) > 0:
    print()
    print("Došel jsi na lokaci", colored(mapa[int(slovnikHrace["level"]) - 1], "yellow") + ".")
    knihovnaMobu = encounter()
    slovnikMoba = random.choice(knihovnaMobu)
    print("Ejhle! Přepadla tě příšera, je to", colored((slovnikMoba["name"]), "blue") + ".")
    print()
    hracJeRychlost = kdoJeRychlejsi(slovnikMoba, slovnikHrace)
    tah(slovnikHrace, slovnikMoba)
  else:
    print()
    print(colored("YOU DIED", "red"))
    break
else:
  print()
  print(colored("Vítězství je tvé!", "green"))