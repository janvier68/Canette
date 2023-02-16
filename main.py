"""
avoir exactement type canette
ok : sauvgarde à chaque changement 
ok : reste quanette à chaque paiment 
git hub pour récup donner

open cv 

BUG QUAND ON VEUT PAYER DETE

POUR PAYER HELLE ASSO
pour apyer via hello asso

"""


#ention tout et stocker en entier

# coding: utf-8
import os
from tkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk
import nfc
from nfc.clf import RemoteTarget

#admin fonction rendre cannette gratuit pour limite detemps 

class Canette:
    def __init__(self,nom,prixCotisant,prixNonCotisant,stock,chemainImg) :#ajouter peut être plus data plustard
        self.nom=nom
        self.prixCotisant=prixCotisant
        self.prixNonCotisant=prixNonCotisant
        self.stock=stock
        self.chemainImg=chemainImg

class Etudiant:
    def __init__(self,prenom,cotisant,nb_A_payer,argentDepenser,nbc_acheter,cardNFC) :#ajouter peut être plus data plustard
        self.prenom=prenom
        self.cotisant=cotisant
        self.nb_A_payer=nb_A_payer
        self.nbc_acheter=nbc_acheter
        self.argentDepenser=argentDepenser
        self.cardNFC=cardNFC
    def acheter_instantaner(self,classCanette):#pas sur 
        if classCanette.stock>0:
            self.nbc_acheter+=1
            classCanette.stock-=1
            if self.cotisant>=1: 
                self.argentDepenser+=int(classCanette.prixCotisant)
            else :
                self.argentDepenser+=int(classCanette.prixNonCotisant)
        else :
            print("plus de canette en stock")
    def acheter_diferait(self,classCanette):#pas sur 
        if self.cotisant==0:
            print("se nes pas possible veuillez cotiser")
        elif classCanette.stock>0:
            self.nb_A_payer=int(self.nb_A_payer)
            self.nbc_acheter+=1
            classCanette.stock-=1
            self.nb_A_payer+=int(classCanette.prixCotisant)
            print("ajouter nb A payer")
        else :
            print("plus de canette en stock")


def F_recupData(nomficher):
    tabRes=[]
    fichier=open(nomficher, 'r')
    contenu = fichier.readlines()
    for ligne in contenu:
        tabRes.append(ligne.strip().split(";"))
    fichier.close()
    return tabRes

# # entrée
# value = StringVar() 
# value.set("texte par défaut")
# entree = Entry(fenetre, textvariable=string, width=30)
# entree.pack()

def F_add():
    global tabEtudiant,eLMCARTE,fenetreCarte
    print(eLMCARTE[1])
    
    # tabEtudiant.append(Etudiant(eLMCARTE[0],int(str(eLMCARTE[1])),int(eLMCARTE[2]),int(eLMCARTE[3]),int(eLMCARTE[4]),eLMCARTE[5]))
    F_writeEtudiant(tabEtudiant)
    fenetreCarte.destroy()

def F_ajouterCarte(carid):
    global eLMCARTE,fenetreCarte
    fenetreCarte = Tk()
    eLMCARTE=[]
    Label(fenetreCarte, text="Prenom",width=25).pack(side=TOP)
    eLMCARTE.append(StringVar())
    Entry(fenetreCarte, textvariable=eLMCARTE[-1], width=30).pack(side=TOP)
    
    Label(fenetreCarte, text="Cotisant",width=25).pack(side=TOP)
    eLMCARTE.append(IntVar())
    Entry(fenetreCarte, textvariable=eLMCARTE[-1], width=30).pack(side=TOP)

    Label(fenetreCarte, text="Nb_a_payer",width=25).pack(side=TOP)
    eLMCARTE.append(IntVar())
    Entry(fenetreCarte, textvariable=eLMCARTE[-1], width=30).pack(side=TOP)

    eLMCARTE.append(0)

    Label(fenetreCarte, text="nbc_acheter",width=25).pack(side=TOP)
    eLMCARTE.append(IntVar())
    Entry(fenetreCarte, textvariable=eLMCARTE[-1], width=30).pack(side=TOP)

    eLMCARTE.append(str(carid))

    Button(fenetreCarte, text="Valider", width=30,command=F_add).pack(side=TOP)
    
    print(eLMCARTE)
    fenetreCarte.mainloop()


def LectureNFC():#renvoie id 
    global varGlobal1,varGlobal2
    # varGlobal1=1
    # varGlobal2=len(tabEtudiant)
    # F_ajouterCarte("teste")
    # varGlobal1=0
    clf = nfc.ContactlessFrontend('usb')
    if (clf.open('usb:001:003')==True):
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        tag=str(tag)
        print("tag:",tag)
        i=0
        for elm in tabEtudiant:
            if (tag==elm.cardNFC):
                
                clf.close()
                varGlobal2=i
                return i
            i+=1
        clf.close()
        # si par reconnue on propose ajouter 
        print("Carte non reconnue")
        varGlobal1=1
        varGlobal2=0
        # F_ajouterCarte(tag)
    else :
        print("proble RNFC")
    return 0

def F_Connextion():
    global varGlobal1
    messagebox.showinfo("Titre1",'cliquer sur OK + Presenter Carte NFC ')#rajouter img de l'endroit ou est NFC
    LectureNFC()
    if (varGlobal1):
        varGlobal1=0
        # return len(tabEtudiant)-1
    return varGlobal2

def F_recupEtudiant():
    res=[]
    tab=F_recupData("data/etudiant.txt")
    for elm in tab:
        res.append(Etudiant(elm[0],int(elm[1]),int(elm[2]),int(elm[3]),int(elm[4]),elm[5]))
    return res

def F_recupCanette():
    res=[]
    tab=F_recupData("data/canette.txt")
    for elm in tab:
        res.append(Canette(elm[0],int(elm[1]),int(elm[2]),int(elm[3]),elm[4]))
    return res

def F_reset(entier):
    global indexEtudiantConnexter,tabPanier,clien,mylist,enleverA_payer,textPaimenAZEt,textPaimenConnextion
    indexEtudiantConnexter=0
    tabPanier=[]
    clien=tabEtudiant[0]
    if entier:
        textPaimenAZEt.set("Prix:0.0")
        textPaimenConnextion.set(str(tabEtudiant[indexEtudiantConnexter].prenom))
    if enleverA_payer:
        enleverA_payer=0


def F_SommeArtice():
    res=0
    if tabEtudiant[indexEtudiantConnexter].cotisant>=1 :
        for elm in tabPanier:
            res+=elm.prixCotisant
    else :
        for elm in tabPanier:
            res+=elm.prixNonCotisant
    return res/10

def F_writeEtudiant(tabEtudiant):
    print("ou etudianti")
    fichier=open("data/etudiant.txt","w")
    for elm in tabEtudiant:
        fichier.write("%s;%s;%s;%s;%s;%s\n"%(elm.prenom,elm.cotisant,elm.nb_A_payer,elm.argentDepenser,elm.nbc_acheter,elm.cardNFC))
    fichier.close()

def F_writeCanette(tabCanette):
    print("ooui canette")
    fichier=open("data/canette.txt","w")
    for elm in tabCanette:
        fichier.write("%s;%s;%s;%s;%s\n"%(elm.nom,elm.prixCotisant,elm.prixNonCotisant,elm.stock,elm.chemainImg))
    fichier.close()

def F_affichage():
    pass

#bug quand removue garde toujours l'argent

def F_remove_item():
    selected_checkboxs = mylist.curselection()
    for selected_checkbox in selected_checkboxs[::-1]:
        tabPanier.pop(selected_checkbox)
        mylist.delete(selected_checkbox)
    textPaimenAZEt.set("Prix:%s"%(F_SommeArtice()))
    
def F_choixMenuFinal(i):
    global enleverA_payer
    if i==0:#il paye
        print("custome",tabEtudiant[indexEtudiantConnexter].nb_A_payer)
        tabPanier.append(Canette("custome",tabEtudiant[indexEtudiantConnexter].nb_A_payer,tabEtudiant[indexEtudiantConnexter].nb_A_payer,1,"NUL"))
        #enlever nb canette
        tabEtudiant[indexEtudiantConnexter].nbc_acheter-=1#car on vas en ajouter
        mylist.insert(END,"%s %seuro"%(tabPanier[-1].nom,tabPanier[-1].prixNonCotisant/10))
        enleverA_payer=1
        print("verif panier",tabPanier[-1].nom,tabPanier[-1].prixNonCotisant/10)
    fenetremenu.destroy()

def F_choixMenu(i):
    global indexEtudiantConnexter,fenetremenu
    fenetremenu = Tk()
    if i==1:#voir compte
        #si pas connexter on connexte
        if indexEtudiantConnexter==0:
            indexEtudiantConnexter=F_Connextion()
        

        textPaiment="Prix : %s"%(tabEtudiant[indexEtudiantConnexter].nb_A_payer/10)
        Label(fenetremenu, text=textPaiment,width=25).pack(side=TOP)

        tabBoutonText=["Payer Maintenant","Payer Plustard"]
        nbBoutonPaiment=len(tabBoutonText)
        tabBoutonPrix=[]
        for i in range(nbBoutonPaiment):
            print(i)
            tabBoutonPrix.append(Button(fenetremenu, text=tabBoutonText[i], width=10,command=lambda i=i: F_choixMenuFinal(i)))
            tabBoutonPrix[i].pack(side=LEFT)#rajouter padx (faut far nouv frame)
        # remouveMyliste(mylist)#on elève affichage 
        fenetremenu.mainloop()
    #boissont 

    #compte 

    #admin
    if i==2 : 
        
        print(i)

def F_listInsert():
    if tabEtudiant[indexEtudiantConnexter].cotisant>=1 :
        for elm in tabPanier:
            mylist.insert(END,"%s %s euro"%(elm.nom,elm.prixCotisant/10))
    else :
        for elm in tabPanier:
            mylist.insert(END,"%s %s euro"%(elm.nom,elm.prixNonCotisant/10))
                

#bug si on clique sur croix
def F_choixPaimentFinal(i):
    global fenetrePaiment,indexEtudiantConnexter
    if i==0:
        # messagebox.showinfo("alerte", "Veuillez connexion")
        # print("-------")
        # print("avant",indexEtudiantConnexter)
        etduVal=F_Connextion()
        # print("valider par",etduVal)
        # print("devient",indexEtudiantConnexter)

        if tabEtudiant[etduVal].cotisant>1:
            print("bon")
            for elm in tabPanier:
                tabEtudiant[indexEtudiantConnexter].nb_A_payer=0
                tabEtudiant[indexEtudiantConnexter].acheter_instantaner(elm)
            # print("prix ajouter",F_SommeArtice())
            # print("nb cannette",len(tabPanier))
            F_writeEtudiant(tabEtudiant)
            F_writeCanette(tabCanette)
            F_reset(1)
        else :
            print("doit être membre bg")
            i=3
    if i==1:
        # messagebox.showinfo("alerte", "Pas terminer")
        etduVal=F_Connextion()
        if tabEtudiant[etduVal].cotisant>1:
            print("bon")
            for elm in tabPanier:
                tabEtudiant[indexEtudiantConnexter].acheter_instantaner(elm)
            # print("prix ajouter",F_SommeArtice())
            # print("nb cannette",len(tabPanier))
            F_writeEtudiant(tabEtudiant)
            F_writeCanette(tabCanette)
            F_reset(1)
        else :
            print("doit être membre bg")
            i=3
    if i==2:
        if indexEtudiantConnexter==0:
            indexEtudiantConnexter=F_Connextion()
        
        if tabEtudiant[indexEtudiantConnexter].cotisant>=1:
            print("Bon")#ajouter fichier ici pour faire tract
            for elm in tabPanier:
                tabEtudiant[indexEtudiantConnexter].acheter_diferait(elm)
            F_writeEtudiant(tabEtudiant)
            F_writeCanette(tabCanette)
            F_reset(1)
    if i==3:
        F_listInsert()
    fenetrePaiment.destroy()
    
def F_choixPaiment(i):
    global fenetrePaiment,mylist,indexEtudiantConnexter,textPaimenConnextion
    som=F_SommeArtice()
    # print("some",som)
    if i==0 and som > 0:
        fenetrePaiment = Tk()
        texte=""
        for elm in tabPanier:
            texte+=elm.nom+"; "

        textPaiment="Elm:%s\nPrix%s"%(texte,som)
        Label(fenetrePaiment, text=textPaiment,width=25).pack(side=TOP)

        tabBoutonText=["Carte","Liquide","Compte","Quitter"]
        nbBoutonPaiment=len(tabBoutonText)
        tabBoutonPrix=[]
        for i in range(nbBoutonPaiment):
            print(i)
            tabBoutonPrix.append(Button(fenetrePaiment, text=tabBoutonText[i], width=10,command=lambda i=i: F_choixPaimentFinal(i)))
            tabBoutonPrix[i].pack(side=LEFT)#rajouter padx (faut far nouv frame)
        remouveMyliste(mylist)#on elève affichage 
        fenetrePaiment.mainloop()
    elif i==1:
        indexEtudiantConnexter=F_Connextion()
        # print("Bonjour" ,tabEtudiant[indexEtudiantConnexter].prenom)
        textPaimenConnextion.set(str(tabEtudiant[indexEtudiantConnexter].prenom))
        remouveMyliste(mylist)
        F_listInsert()
        textPaimenAZEt.set("Prix:%s"%(F_SommeArtice()))

    else : 
        remouveMyliste(mylist)
        F_reset(1)


def F_AchoseBoisson(i):
    if tabCanette[i].stock>0:
        tabPanier.append(tabCanette[i])
        if tabEtudiant[indexEtudiantConnexter].cotisant>=1:
            print("cotisant")
            mylist.insert(END,"%s %s euro"%(tabPanier[-1].nom,tabPanier[-1].prixCotisant/10))
        else :
            mylist.insert(END,"%s %s euro"%(tabPanier[-1].nom,tabPanier[-1].prixNonCotisant/10))
        textPaimenAZEt.set("Prix:%s"%(F_SommeArtice()))
    else : 
        print("plus de canette dispo")

def remouveMyliste(mylist):
    mylist.delete(0,END)


global enleverA_payer,textPaimenAZEt,varGlobal1
#si on execute
if __name__=="__main__":
    varGlobal1=0
    #!partie init donner
    """donner
    etudiant.txt #on il y aurra tout les inderant insi que id rfid lier
    prix.txt #cannette et prix et img(chemin)
    """
    tabEtudiant=F_recupEtudiant()

    tabCanette=F_recupCanette()

    enleverA_payer=0
    F_reset(0)
    
    #!partie affichage graphique 
    fenetre = Tk()
    #taille fenetre
    taillefenX=1300
    taillefenY=800
    fenetre.title("Canette")
    fenetre.geometry("%sx%s"%(taillefenX,taillefenY))
    #conpartiment pour affichage
    
    TK_frameLeft=Frame(fenetre, relief=FLAT, bd=0,width=taillefenX/2)
    TK_frameRight=Frame(fenetre, relief=FLAT, bd=0,width=taillefenX/2)

    TK_RecapArticle = Frame(TK_frameLeft, relief=FLAT, bd=2,height=taillefenX/2,padx=0,pady=0)
    TK_ListItem = Frame(TK_RecapArticle, relief=FLAT, bd=2,height=taillefenX/2)
    
    TK_bardMenu = Frame(TK_frameRight, relief=FLAT, bd=2)
    TK_choisirBoisson = Frame(TK_frameRight, relief=FLAT, bd=2)
    TK_Paiment = Frame(TK_frameLeft, relief=FLAT, bd=2)

    #les truc utilise
    #REcap article 
    Label(TK_RecapArticle, text="Recap Article",width=25).pack(side=TOP,expand=True,fill=BOTH)
    scroll_bar = Scrollbar(TK_ListItem)
    mylist = Listbox(TK_ListItem,yscrollcommand = scroll_bar.set)    
    for i in range(len(tabPanier)):
        mylist.insert(END,"%s %seuro"%(tabPanier[i].nom,tabPanier[i].prixNonCotisant))

    scroll_bar.config( command = mylist.yview )
    Button(TK_RecapArticle, text="delete", command=F_remove_item,width=25).pack(side=BOTTOM, fill=BOTH,expand=True)
    
    #bar menu
    nbBoutonMenu=3
    tabBoutonText=["Boisson","Voir Compte","Admin"]
    tabBoutonMenu=[]
    for i in range(nbBoutonMenu):
        tabBoutonMenu.append(Button(TK_bardMenu, text=tabBoutonText[i], width=10,command=lambda i=i: F_choixMenu(i)))
        tabBoutonMenu[i].pack(side=LEFT)#rajouter padx (faut far nouv frame)

    #choisir boisson
    Label(TK_choisirBoisson, text="Choix Boisson",width=25).pack(side=TOP,fill=X)
    #canvas pour afficher img qu'on ren clickable
    canvas = Canvas(TK_choisirBoisson, width=600, height=600)
    canvas.pack()
    tabimg_file=[]
    tabimg=[]
    for i in range(len(tabCanette)):
        tabimg_file.append( Image.open("img/%s"%(tabCanette[i].chemainImg)))
        tabimg_file[-1] = tabimg_file[-1].resize((100, 100))
        tabimg.append(ImageTk.PhotoImage(tabimg_file[-1]))
        Button(canvas, image=tabimg[-1],command=lambda i=i:F_AchoseBoisson(i)).pack(side=LEFT)
    

    #paiment
    #bouton paiment
    textPaimenAZEt = StringVar()
    textPaimenAZEt.set("Prix:%s"%(F_SommeArtice()))
    textPaimenConnextion = StringVar()
    textPaimenConnextion.set(str(tabEtudiant[indexEtudiantConnexter].prenom))
    Label(TK_Paiment, text="Paiment",width=25).pack(side=TOP,fill=X)
    Label(TK_Paiment, textvariable=textPaimenAZEt,width=25).pack(side=TOP,fill=X)
    Label(TK_Paiment, text="Connextion",width=25).pack(side=TOP,fill=X)
    Label(TK_Paiment, textvariable=textPaimenConnextion,width=25).pack(side=TOP,fill=X)
    nbBoutonPaiment=3
    tabBoutonText=["Payer","Connextion","Reset"]
    tabBoutonPrix=[]
    for i in range(nbBoutonPaiment):
        tabBoutonPrix.append(Button(TK_Paiment, text=tabBoutonText[i], width=10,command=lambda i=i: F_choixPaiment(i)))
        tabBoutonPrix[i].pack(side=LEFT)#rajouter padx (faut far nouv frame)

    #affichage Frame #https://www.pythontutorial.net/tkinter/tkinter-pack/
    TK_frameLeft.pack(side=LEFT,expand=TRUE,fill=BOTH)
    TK_frameRight.pack(side=RIGHT, expand=TRUE,fill=BOTH)

    scroll_bar.pack( side = RIGHT,fill = Y )
    mylist.pack( side = LEFT,fill=BOTH)
    TK_ListItem.pack(fill=BOTH,side=TOP)#ici pour scroll
    TK_RecapArticle.pack(fill=BOTH,side=TOP)
    
    # Label(TK_bardMenu, text="menu World",width=10,heigh=10).pack()
    TK_bardMenu.pack(fill=X,side=TOP)

    TK_choisirBoisson.pack(fill=BOTH,side=BOTTOM,expand=True)

    TK_Paiment.pack(fill=BOTH)


    #!partie client

    # print(tabCanette[0].stock)
    # tabEtudiant[0].acheter_diferait(tabCanette[0])
    # print(tabCanette[0].stock)  
    # tabEtudiant[1].acheter_diferait(tabCanette[0])
    # print(tabCanette[0].stock)

    # print(LectureNFC().prenom)
    fenetre.mainloop()

    #quand fermet 
    #on back up tout et on recrée nouveau ficher
    os.system("cp -r data OLD%sdata"%(1))#rajouter nb en fonction version

    #en suite on modife
    F_writeEtudiant(tabEtudiant)
    F_writeCanette(tabCanette)
    

