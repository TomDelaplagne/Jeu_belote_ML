from player_class import Player
from deck_class import Deck
import os


class Game:
    def __init__(self, file=None):
        # if file != None :
        #     f = open(file, 'r')

        name1 = input("p1 name ")
        name2 = input("p2 name ")
        name3 = input("p3 name ")
        name4 = input("p4 name ")
        self.deck = Deck()
        self.p1 = Player(name1)
        self.p2 = Player(name2)
        self.p3 = Player(name3)
        self.p4 = Player(name4)

        self.players =  [self.p1, self.p2, self.p3, self.p4]
        self.idPlayerToPlay = 0


    def draw(self, p1n, p1c, p2n, p2c, p3n, p3c, p4n, p4c):
        d = "{} drew {} {} drew {} {} drew {} {} drew {}"
        d = d.format(p1n,
                     p1c,
                     p2n,
                     p2c,
                     p3n,
                     p3c,
                     p4n,
                     p4c)
        print(d)

    def draw_cards(self):
        #reset deck
        self.deck = Deck()
        for i in self.players:
            i.card = []
        print("beginning Game!")
        for i in range(8):
            p1c = self.deck.rm_card()
            p2c = self.deck.rm_card()
            p3c = self.deck.rm_card()
            p4c = self.deck.rm_card()
            p1n = self.p1.name
            p2n = self.p2.name
            p3n = self.p3.name
            p4n = self.p4.name

            self.players[0].card.append(p1c)
            self.players[1].card.append(p2c)
            self.players[2].card.append(p3c)
            self.players[3].card.append(p4c)

            self.draw(p1n,
                    p1c,
                    p2n,
                    p2c,
                    p3n,
                    p3c,
                    p4n,
                    p4c)
        print("il reste " + str(len(self.deck.cards))+" dans le paquet")

        print(self.players[0].card)
        print(self.players[1].card)
        print(self.players[2].card)
        print(self.players[3].card)

        suits = ["trefles",
             "coeurs",
             "piques",
             "carreaux"]

        values = ["7", "8", "9", "J", "Q", "K", "10", "A"]

        for i in self.players:
            cardTemp = []
            for couleur in suits:
                newCouleur = []
                for j in i.card:
                    if j.suits[j.suit] == couleur:
                        newCouleur.append(j)
                for j in newCouleur:
                    k = newCouleur.index(j) - 1
                    print(newCouleur[k], j)
                    while k>=0 and values.index(str(newCouleur[k].values[newCouleur[k].value])) > values.index(str(j.values[j.value])):
                        newCouleur[k+1] = newCouleur[k] # decalage
                        k = k-1
                    newCouleur[k+1] = j
                for k in newCouleur:
                    cardTemp.append(k)
            i.card = cardTemp[:]
            



    def lineVoid(self):
        print("--------------------------------------------")
    
    def whichAtout(self):
        ints = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        suits = ["trefles",
             "coeurs",
             "piques",
             "carreaux"]
        prises = []
        passed = []
        while (len(passed)<3):
            for i in self.players:
                os.system('clear')
                if len(prises)>0:
                    print("historique des prises : ")
                    for j in prises:
                        print("le joueur " + j[2].name + " a pris a " +  str(j[1]) + " " + suits[j[0]])
                    self.lineVoid()
                print("c'est au tour de " + i.name + " de jouer")
                m = input("voir ses cartes ? (press any key)")
                
                
                for j in range(len(i.card)):
                    print("(" + str(j) + ") " + str(i.card[j]))

                self.lineVoid()
                oupsi = True
                m = None
                while not(m in ints[:5]):
                    m = input("quel couleur d'atout voulez-vous ?\n(0) trefles\n(1) coeurs\n(2) piques\n(3) carreaux\n(4) passe \n")
                if m != '4':
                    passed = []
                    isEntier = False
                    while not(isEntier):
                        q = input("A combien vous voulez prendre ? ")
                        try:
                            isEntier = (float(q) == int(q))
                        except ValueError:
                            print("ceci n'est pas un entier ! ")
                    
                    if int(q)<80 or (len(prises)>0 and prises[-1][1]>=int(q)):
                        self.lineVoid()
                        print("prise pas legale !")
                        print("attention a bien enchérir sinon votre enchere ne sera pas comptée !")
                        
                        m = None
                        while not(m in ints[:5]):
                            m = input("quel couleur d'atout voulez-vous ?\n(0) trefles\n(1) coeurs\n(2) piques\n(3) carreaux\n(4) passe \n")
                        if m != '4':
                            passed = []
                            isEntier = False
                            while not(isEntier):
                                q = input("A combien vous voulez prendre ? ")
                                try:
                                    isEntier = (q == int(q))
                                except ValueError:
                                    print("ceci n'est pas un entier ! ")

                        elif m == '4':
                            oupsi = False
                            passed.append(True)
                    if not(int(q)<80 or (len(prises)>0 and prises[-1][1]>=int(q))):
                        prises.append([int(m), int(q), i])
                elif (m == '4') and oupsi:
                    passed.append(True)
                if len(passed)>=3 and len(prises)!=0:
                    break
                elif len(prises)==0 and len(passed)>=4:
                    os.system('clear')
                    print(f"Tout le monde a passé")
                    self.lineVoid()
                    input("press any key to continue")
                    self.play_mene()
                    self.allPassed = True
                    return
        print(prises)
        os.system('clear')
        m = prises[len(prises)-1][0]
        self.atout = [suits[int(m)], m, self.players.index(prises[len(prises)-1][2]), prises[len(prises)-1][1]]
        print("la couleur d'atout est le " + self.atout[0])


    def isCouleurinCards(self, couleur, cards):
        suits = ["trefles",
             "coeurs",
             "piques",
             "carreaux"]
        for j in cards:
            if suits[j.suit] == couleur:
                return True
        return False


    def play_pli(self):
        suits = ["trefles",
             "coeurs",
             "piques",
             "carreaux"]
        ints = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        os.system('clear')
        self.pli = []
        self.couleur_demandee = None
        for i in range(4):
            print("l'atout est le " + self.atout[0])
            if self.couleur_demandee != None:
                print("la couleur demandee est le " + self.couleur_demandee)
            self.lineVoid()
            print("c'est au tour de " + self.players[(self.idPlayerToPlay+i)%4].name + " de jouer")
            m = input("voir ses cartes ? (press any key)")
            for j in range(len(self.players[(self.idPlayerToPlay+i)%4].card)):
                print("(" + str(j) + ") " + str(self.players[(self.idPlayerToPlay+i)%4].card[j]))
            r = 'N'
            while r == 'N':
                m = None
                self.carte_jouable = False
                while  not(self.carte_jouable):
                    m = input("Quel carte voulez-vous jouer ? ")
                    while not(m in ints[:len(self.players[(self.idPlayerToPlay+i)%4].card)]):
                        m = input("Quel carte voulez-vous jouer ? ")
                    # check if the card is playable it means that the card need to be the color of self.couleur_demandee 
                    if self.couleur_demandee == None:
                        break
                    elif not(suits[self.players[(self.idPlayerToPlay+i)%4].card[int(m)].suit] == self.couleur_demandee):
                        if suits[self.players[(self.idPlayerToPlay+i)%4].card[int(m)].suit] == self.atout:
                            #verifier qu'il y a pas de carte avec la couleur demandée dans la main du joueur
                            if self.isCouleurinCards(self.couleur_demandee, self.players[(self.idPlayerToPlay+i)%4].card):
                                print("vous ne pouvez pas jouer cette carte")
                                self.carte_jouable = False
                            else:
                                self.carte_jouable = True
                            
                        else :
                            #verifier qu'il n'y a pas de carte de la couleur demandée ni de carte d'atout dans sa main
                            if self.isCouleurinCards(self.atout, self.players[(self.idPlayerToPlay+i)%4].card) or self.isCouleurinCards(self.couleur_demandee, self.players[(self.idPlayerToPlay+i)%4].card):
                                print("vous ne pouvez pas jouer cette carte")
                                self.carte_jouable = False
                            else:
                                self.carte_jouable = True
                    else : 
                        self.carte_jouable = True
            
                r = input("vous voulez jouer le " + str(self.players[(self.idPlayerToPlay+i)%4].card[int(m)]) + " ? (Y/N)")
            os.system('clear')
            if self.couleur_demandee == None:
                self.couleur_demandee = self.players[(self.idPlayerToPlay+i)%4].card[int(m)].suits[self.players[(self.idPlayerToPlay+i)%4].card[int(m)].suit]
           
            
            
            self.pli.append(self.players[(self.idPlayerToPlay+i)%4].card[int(m)])
            self.players[(self.idPlayerToPlay+i)%4].card.pop(int(m))
            
            #print the card of all players who have palyed there card in the pli already
            print("Le pli : ")
            for j in range(len(self.pli)):
                print(self.players[(self.idPlayerToPlay + j)%4].name + " a joué le " + str(self.pli[j]))
            self.lineVoid()
            
        # print(self.pli)
        os.system('clear')
        print("l'atout est le " + self.atout[0])
        print("la couleur demandee est le " + self.couleur_demandee)
        
        NAtout = ["7", "8", "9", "J", "Q", "K", "10", "A"]
        NAtoutPoints = [0,0,0,2,3,4,10,11]
        Atout = ["7",
            "8", "Q",
            "K", "10", "A", "9", 
            "J"]
        AtoutPoints = [0, 0, 3, 4, 10, 11, 14, 20]
        idCartePlusForte = -1
        idCartePlusForteAtout = -1
        self.isatout = False
        for i in range(len(self.pli)):
            print(self.players[(self.idPlayerToPlay+i)%4].name + " a joue le " + str(self.pli[i]))
            if self.pli[i].suits[self.pli[i].suit] == self.couleur_demandee or self.pli[i].suits[self.pli[i].suit] == self.atout[0]:
                if self.pli[i].suits[self.pli[i].suit] == self.atout[0]:
                    self.isatout = True
                    if Atout.index(self.pli[i].values[self.pli[i].value]) > idCartePlusForteAtout:
                        # print(self.pli[i].values[self.pli[i].value])
                        cartePlusForte = self.pli[i]
                        idCartePlusForteAtout = Atout.index(self.pli[i].values[self.pli[i].value])
                        self.idPlayerToPlay_wait = (self.idPlayerToPlay+i)%4
                elif not(self.isatout) and NAtout.index(self.pli[i].values[self.pli[i].value]) > idCartePlusForte:
                    # print(self.pli[i].values[self.pli[i].value])
                    idCartePlusForte = NAtout.index(self.pli[i].values[self.pli[i].value])
                    cartePlusForte = self.pli[i]
                    self.idPlayerToPlay_wait = (self.idPlayerToPlay+i)%4
        self.lineVoid()
        print("la carte qui est la plus forte est le : " + str(cartePlusForte))
        
        gagnant = self.players[(self.pli.index(cartePlusForte)+self.idPlayerToPlay)%4]
        print(f"le joueur {gagnant.name} a gagne le pli")
        points = 0
        if (self.nbPlis == 8):
            print(f"il remporte les points du 10 de der")
            points+=10
        for i in self.pli:
            if i.suits[i.suit] == self.atout[0]:
                points += AtoutPoints[Atout.index(i.values[i.value])]
            else:
                points += NAtoutPoints[NAtout.index(i.values[i.value])]
        print(f"il a remporte : {str(points)} points")
        self.players[(self.pli.index(cartePlusForte)+self.idPlayerToPlay)%4].points += points
        self.idPlayerToPlay = self.idPlayerToPlay_wait

    def affichePoints(self):
        self.lineVoid()
        equipe1somme = 0
        equipe2somme = 0
        print("Classement :")
        for i in range(len(self.players)):
            if i%2==0:
                equipe1somme += self.players[i].points
            if i%2==1:
                equipe2somme += self.players[i].points
        if equipe1somme > equipe2somme:
            print("1er : equipe 1 _ " + self.players[0].name + " et " + self.players[2].name + " avec : " + str(equipe1somme) + " points")
            print("2eme : equipe 2 _ " + self.players[1].name + " et " + self.players[3].name + " avec : " + str(equipe2somme) + " points")
        elif equipe2somme > equipe1somme:
            print("1er : equipe 2 _ " + self.players[1].name + " et " + self.players[3].name + " avec : "+str(equipe2somme)+" points")
            print("2eme : equipe 1 _ " + self.players[0].name + " et " + self.players[2].name + " avec : "+str(equipe1somme)+" points")
        else:
            print("les deux equipes sont a egalite avec : "+ str(equipe1somme) + " points")
            


    def isPriseReussie(self):
        os.system("clear")
        equipesomme = 0
        print(f"Le contrat était de : {str(self.atout[-1])} {self.atout[0]}")
        for i in range(len(self.players)//2):
            equipesomme += self.players[(i*2 + self.atout[2])%4].points
        print(f"l'equipe {str(self.atout[2]%2 + 1)} a fait : {equipesomme} dans cette mene")
        if (self.atout[-1] <= equipesomme):
            print(f"l'equipe {str(self.atout[2]%2 + 1)} gagne la mene !\nElle remporte : {str(equipesomme)} + {str(self.atout[-1])} = {str(equipesomme + self.atout[-1])} points")
            print(f"la defense remporte {str(162 - equipesomme)} points")
            if self.atout[2]%2 + 1 == 1:
                self.equipe2somme += 162 - equipesomme
                self.equipe1somme += equipesomme + self.atout[-1]
            elif self.atout[2]%2 + 1 == 1:
                self.equipe1somme += 162 - equipesomme
                self.equipe2somme += equipesomme + self.atout[-1]

        else:
            print(f"l'equipe {str(self.atout[2]%2 + 1)} tombe !")
            print(f"la defense remporte la mene et remporte : 162 + {str(self.atout[-1])} = {str(162 + self.atout[-1])} points")
            if self.atout[2]%2 + 1 == 1:
                self.equipe2somme += 162 + self.atout[-1]
            elif self.atout[2]%2 + 1 == 2:
                self.equipe1somme += 162 + self.atout[-1]
        self.lineVoid()


        
    def classementTotal(self):
        for i in self.players:
            i.points = 0
        print("Classement Total :")
        if self.equipe1somme > self.equipe2somme:
            print("1er : equipe 1 _ " + self.players[0].name + " et " + self.players[2].name + " avec : " + str(self.equipe1somme) + " points")
            print("2eme : equipe 2 _ " + self.players[1].name + " et " + self.players[3].name + " avec : " + str(self.equipe2somme) + " points")
        elif self.equipe2somme > self.equipe1somme:
            print("1er : equipe 2 _ " + self.players[1].name + " et " + self.players[3].name + " avec : "+str(self.equipe2somme)+" points")
            print("2eme : equipe 1 _ " + self.players[0].name + " et " + self.players[2].name + " avec : "+str(self.equipe1somme)+" points")
        else:
            print("les deux equipes sont à égalité avec : "+ str(self.equipe1somme) + " points")

    def play_mene(self):
        self.draw_cards()
        self.whichAtout()
        if self.allPassed == False:
            self.nbPlis = 1
            while (len(self.players[0].card) > 0):
                print("C'est le " + str(self.nbPlis) +"eme pli")
                m = input("Jouer le pli ? (press any key)")
                self.play_pli()
                self.affichePoints()
                self.nbPlis+=1
            self.lineVoid()
            print("La mene est finie !")
            input("Fin de mene ? (press any key)")
            self.isPriseReussie()
            self.classementTotal()
            self.lineVoid()
            input("Mene suivante ? (press any key)")
        else:
            self.allPassed = False



    def play_game(self):
        self.allPassed = False
        self.equipe1somme = 0
        self.equipe2somme = 0
        while (self.equipe1somme<701 and self.equipe2somme<701):
            self.play_mene()
        print("La partie est finie !! Bravo a tous")
        if self.equipe2somme < self.equipe1somme:
            print(f"l'equipe 1 gagne la partie, bravo à {self.players[0].name} et à {self.players[2].name} !")
        elif self.equipe2somme > self.equipe1somme:
            print(f"l'equipe 2 gagne la partie, bravo à {self.players[1].name} et à {self.players[3].name} !")
        else:
            print("égalité grrrr ca me gonfle personne gagne tant pis j'ai la flemme de programmer un tie break. Faites un shifoumi au pire")
        input("fin de partie (press enter)")