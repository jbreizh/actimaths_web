#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

############## Import global
from lxml import etree
from os import listdir
from os.path import join, dirname, isdir
from time import strftime ,localtime

############## Variables
environnement = "actimaths"
max_exercice = 20

############## lis le fichier listant les exercices au format xml
def lire_liste_exercice(file):
    tree = etree.parse(file)
    root = tree.getroot()
    liste = []
    for onglet in root.iter("onglet"):
        nom_onglet = onglet.get("nom")
        liste_categorie = []
        for categorie in onglet.iter("categorie"):
            nom_categorie = categorie.get("nom")
            liste_exercice = []
            for exercice in categorie.iter("exercice"):
                nom_exercice = exercice.get("nom")
                commande_exercice = exercice.get("commande")
                liste_parametre = []
                for parametre in exercice.iter("parametre"):
                    nom_parametre = parametre.get("nom")
                    min_parametre = parametre.get("min")
                    max_parametre = parametre.get("max")
                    defaut_parametre = parametre.get("defaut")
                    liste_parametre.append([nom_parametre, min_parametre, max_parametre, defaut_parametre])
                liste_exercice.append([nom_exercice, liste_parametre, commande_exercice])
            liste_categorie.append([nom_categorie, liste_exercice])
        liste.append([nom_onglet, liste_categorie])
    return liste

############## liste tous les modeles possibles
def lire_modele(type):
    modele = ""
    for fichier in listdir(join(dirname(__file__),"exercices_%s" % environnement, "modeles",type)):
        if isdir(join(dirname(__file__),"exercices_%s" % environnement, "modeles",type, fichier)):
            modele += "<option>%s</option>" % fichier
    return modele

############## liste tous les niveaux
def lire_niveau(liste_exercice):
    niveau = ""
    for onglet in range(len(liste_exercice)):
        niveau += "<option>%s</option>" % liste_exercice[onglet][0]
    return niveau

############## Creation de la liste d'exercice a partir du formulaire
def creation_formulaire(erreur = ""):
    ## creation de la liste d'exercices
    liste_exercice = lire_liste_exercice(join(dirname(__file__),"exercices_%s" % environnement , "onglets", "niveau.xml"))
    ## creation du formuaire
    print "Content-type: text/html;\r\n\r\n"
    ## Head
    html = u"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Actimaths Web</title>
<link rel="stylesheet" href="/data/css/style.css">
<script type="text/javascript" src='http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js'></script>
<script type="text/javascript" src="/data/js/organictabs.jquery.js"></script>
<script type="text/javascript">
function valider(formulaire){
   var sujet_presentation = formulaire.elements['sujet_presentation'].checked;
   var corrige_presentation = formulaire.elements['corrige_presentation'].checked;
   var sujet_page = formulaire.elements['sujet_page'].checked;
   var corrige_page = formulaire.elements['corrige_page'].checked;
   if (!(sujet_presentation || corrige_presentation || sujet_page || corrige_page))
   {
       alert("Choisissez un type de sortie");
       return false;
   }
   var temps_slide = formulaire.elements['temps_slide'].value;
   if (isNaN(parseInt(temps_slide)))
   {
      alert("Le temps par slide doit ête un nombre");
      return false;
   }
   return true;
}
</script>
</head>"""
    ## Body
    html += """<body>
<div id="page-wrap">
<form method="post" action="system.py" id="idForm"  onsubmit="return valider(this)">
<h1>Actimaths Web</h1> \n"""
    ## Affichage du message d'erreur
    if erreur:
        html +=  u"<h2 class=\"erreur\">%s</h2> \n" % erreur
    ## Creation du formulaire d'exercices
    for onglet in range(len(liste_exercice)):
        html += u"<h2>%s</h2> \n""" % liste_exercice[onglet][0]
        html += u"<div id=\"Onglets-%s\" class=\"Onglets\"> \n" % onglet
        # Script de gestion des onglets
        html += "<script type=\"text/javascript\"> \n"
        html += "$(function() { \n"
        html += u"$(\"#Onglets-%s\").organicTabs(); \n" % onglet
        html += "}); \n"
        html += "</script> \n"
        # Declaration des onglets
        html += "<ul class=\"nav\"> \n"
        html += "<li class=\"nav-0\"><a href=\"#Onglets-%s-0\" class=\"current\">&#x27A4;</a></li> \n" % onglet
        for categorie in range(len(liste_exercice[onglet][1])):
            if categorie == len(liste_exercice[onglet][1])-1:
                html += u"<li class=\"nav-%s last\"><a href=\"#Onglets-%s-%s\">%s</a></li> \n" %(categorie+1,onglet,categorie+1,liste_exercice[onglet][1][categorie][0])
            else:
                html += u"<li class=\"nav-%s\"><a href=\"#Onglets-%s-%s\">%s</a></li> \n" %(categorie+1,onglet,categorie+1,liste_exercice[onglet][1][categorie][0])
        html += "</ul> \n"
        html += "<div class=\"list-wrap\"> \n"
        html += "<ul id=\"Onglets-%s-0\"> \n" % onglet
        html += "</ul> \n"
        # Construction du contenu des onglets
        for categorie in range(len(liste_exercice[onglet][1])):
            html += u"<ul id=\"Onglets-%s-%s\"  class=\"hide\"> \n" % (onglet,categorie+1)
            # Construction de la ligne correspondant à un exercice
            for exercice in range(len(liste_exercice[onglet][1][categorie][1])):
                html += "<li>"
                html += u"<input class=\"input exercice\" type=\"number\" value=\"0\" min=\"0\" max=\"%s\" name=\"%s\" />" % (max_exercice, liste_exercice[onglet][1][categorie][1][exercice][2])
                html += u"<a href=\"/data/vignettes/%s.png\" ><img src=\"/data/images/whatsthis.png\" /></a>" % liste_exercice[onglet][1][categorie][1][exercice][2]
                html += u"<label class=\"label exercice\" for=\"%s\"/>%s</label>" %(liste_exercice[onglet][1][categorie][1][exercice][2], liste_exercice[onglet][1][categorie][1][exercice][0])
                # Ajout des parametres à la ligne de l'exercice
                for parametre in range(len(liste_exercice[onglet][1][categorie][1][exercice][1])):
                        html += u"<input class=\"input parametre\" type=\"number\" value=\"%s\" " % liste_exercice[onglet][1][categorie][1][exercice][1][parametre][3]
                        html += u"min=\"%s\" " % liste_exercice[onglet][1][categorie][1][exercice][1][parametre][1]
                        html += u"max=\"%s\" " % liste_exercice[onglet][1][categorie][1][exercice][1][parametre][2]
                        html += u"name=\"%s-%s\" />" % (liste_exercice[onglet][1][categorie][1][exercice][2], parametre)
                html += "</li> \n"
            html += "</ul> \n"
        html += "</div> <!-- END List Wrap --> \n"
        html += "</div> <!-- END Organic Tabs (%s) --> \n"% onglet
    ## Creation du formulaire d'option
    html += u"""
<h2>Options</h2>
<div id="Options" class=\"Onglets\">
<script>
$(function() {
$("#Options").organicTabs();
});
</script>
<ul class="nav">
<li class="nav-0"><a href="#Options-0" class="current">&#x27A4;</a></li>
<li class="nav-1"><a href="#Options-1">Informations</a></li>
<li class="nav-2 last"><a href="#Options-2">Sorties</a></li>
</ul>
<div class="list-wrap">
<ul id="Options-0">
</ul>
<ul id="Options-1" class="hide">
<li><label class=\"label option\" for=\"titre\">Titre de la fiche :</label><input class=\"input option\" type=\"text\" name=\"titre\" value=\"Activite Mentale\"/></li>
<li><label class=\"label option\" for=\"nom_etablissement\">Nom de l'établissement :</label><input class=\"input option\" type=\"text\" name=\"nom_etablissement\" value=\"Etablissement X\"/></li>
<li><label class=\"label option\" for=\"nom_auteur\">Nom de l'auteur :</label><input class=\"input option\" type=\"text\" name=\"nom_auteur\" value=\"Mr X\"/></li>
<li><label class=\"label option\" for=\"temps_slide\">Temps par slide :</label><input class=\"input option\" type=\"number\" name=\"temps_slide\" value=\"10\" min=\"0\" max=\"100\"/></li>
<li><label class=\"label option\" for=\"date_activite\">Date de l'activité :</label><input class=\"input option\" type=\"text\" name=\"date_activite\" value=\"%s\"/></li>
<li><label class=\"label option\" for=\"niveau\">Niveau :</label><select class=\"select option\" name=\"niveau\">%s</select></li>
</ul>
<ul id="Options-2" class="hide">
<li><label class=\"label option\" for=\"sujet_presentation\">Sujet vidéoprojetable :</label><input class=\"input option\" type=\"checkbox\" name=\"sujet_presentation\" checked/></li>
<li><label class=\"label option\" for=\"corrige_presentation\">Corrigé vidéoprojetable :</label><input class=\"input option\" type=\"checkbox\" name=\"corrige_presentation\" checked/></li>
<li><label class=\"label option\" for=\"modele_presentation\">Modèle vidéoprojetable :</label><select class=\"select option\" name=\"modele_presentation\">%s</select></li>
<li><hr /></li>
<li><label class=\"label option\" for=\"sujet_page\">Sujet papier :</label><input class=\"input option\" type=\"checkbox\" name=\"sujet_page\"/></li>
<li><label class=\"label option\" for=\"corrige_page\">Corrigé papier :</label><input class=\"input option\" type=\"checkbox\" name=\"corrige_page\"/></li>
<li><label class=\"label option\" for=\"modele_page\">Modèle papier :</label><select class=\"select option\" name=\"modele_page\">%s</select></li>
</ul>
</div> <!-- END List Wrap -->
</div> <!-- END Organic Tabs (Options) -->
<p class=\"input\"><input class=\"input creer\" type="submit" value=\"Créer\"/> <input class=\"input annuler\" type="reset" value=\"Annuler\"/></p>
</form> <!-- END Formulaire -->
</div> <!-- END Page Wrap -->
</body>
</html>""" % (strftime('%A %d %B %Y',localtime()), lire_niveau(liste_exercice), lire_modele("presentation"), lire_modele("page"))
    print html.encode('utf-8')

if __name__ == "__main__":
    creation_formulaire()
