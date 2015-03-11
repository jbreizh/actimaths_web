#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

############## Import global
from os import listdir
from os.path import join, dirname
from cgi import FieldStorage
from StringIO import StringIO
from tempfile import mkdtemp
from zipfile import ZipFile, ZIP_DEFLATED
from shutil import rmtree

############## Import local
from actimaths_web2 import lire_liste_exercice, creation_formulaire

############## Variables
environnement = "actimaths"
max_exercice = 20
dossier_creation = "/tmp/"

############## lis le formulaire et créé la liste des exercices
def lire_formulaire(liste_exercice, form):
    try:
        ## Creation de parametre a partir du formulaire
        parametres = {'sujet_presentation':   form.getvalue("sujet_presentation"),
                      'corrige_presentation': form.getvalue("corrige_presentation"),
                      'sujet_page':           form.getvalue("sujet_page"),
                      'corrige_page':         form.getvalue("corrige_page"),
                      'titre':                form.getvalue("titre"),
                      'nom_etablissement':    form.getvalue("nom_etablissement"),
                      'nom_auteur':           form.getvalue("nom_auteur"),
                      'temps_slide':          form.getvalue("temps_slide"),
                      'date_activite':        form.getvalue("date_activite"),
                      'niveau':               form.getvalue("niveau"),
                      'nom_fichier':          "exercice",
                      'environnement':        environnement,
                      'affichage':            "niveau",
                      'modele_presentation':  form.getvalue("modele_presentation"),
                      'modele_page':          form.getvalue("modele_page"),
                      'chemin_csv':           "",
                      'afficher_pdf':         False}
        ## Creation de la liste d'exercice a partir du formulaire
        parametres['liste_exercice'] = []
        for onglet in range(len(liste_exercice)):
            for categorie in range(len(liste_exercice[onglet][1])):
                for exercice in range(len(liste_exercice[onglet][1][categorie][1])):
                    nombre_exercice = int(form.getvalue("%s" % liste_exercice[onglet][1][categorie][1][exercice][2],"0"))
                    commande = liste_exercice[onglet][1][categorie][1][exercice][2]
                    valeur_parametre = []
                    for parametre in range(len(liste_exercice[onglet][1][categorie][1][exercice][1])):
                        valeur_parametre.append(int(form.getvalue("%s-%s" % (liste_exercice[onglet][1][categorie][1][exercice][2], parametre),liste_exercice[onglet][1][categorie][1][exercice][1][parametre][3])))
                    for i in range(nombre_exercice):
                        parametres['liste_exercice'].append((commande, valeur_parametre))
        return (True, parametres)
    except:
        return  (False, u"Erreur de lecture du formulaire.")

############## Creation de la liste d'exercice a partir du formulaire
def creation_exercice(parametres):
    # on teste si l'utilisateur à coché au moins une sortie
    if (parametres['sujet_presentation'] or parametres['corrige_presentation'] or parametres['sujet_page'] or parametres['corrige_page']):
        # on teste si l'utilisateur a choisit des exercices
        if parametres['liste_exercice']:
            # on teste si l'utilisateur n'a pas choisit trop d'exercices
            if len(parametres['liste_exercice']) <= max_exercice:
                # Creation d'un dossier temporaire dans tmp et creation des exercices
                parametres['chemin_fichier'] = mkdtemp( dir = dossier_creation)
                # Au cas ou la creation des exercices echoue
                try:
                    # Import de la fonction creation de l'environnement choisit et creation des exercices
                    exec("from exercices_%s.creation import creation" % environnement)
                    creation(parametres)
                    # Compression de tous les fichiers crees en zip
                    buffer_zip = StringIO()
                    archive = ZipFile(buffer_zip, 'w', ZIP_DEFLATED)
                    for fichier in listdir(parametres['chemin_fichier']):
                        archive.write(fichier, fichier)
                    archive.close()
                    buffer_zip.seek(0)
                    response = buffer_zip.getvalue()
                    buffer_zip.close()
                    return (True, response)
                except:
                    return (False, u"Erreur interne.")
                finally:
                    # Supression du dossier temporaire
                    rmtree(parametres['chemin_fichier'])
            else:
                return (False, u"Vous ne pouvez pas choisir plus de %s exercices simultanément." % max_exercice)
        else:
            return (False, u"Veuillez sélectionner au moins un exercice.")
    else:
        return (False, u"Veuillez sélectionner au moins une sortie.")

###==============================================================
###                            Main
###==============================================================
def main():
    ## creation du formuaire
    liste_exercice = lire_liste_exercice(join(dirname(__file__),"exercices_%s" % environnement, "onglets", "niveau.xml"))
    form = FieldStorage()
    ## creation des parametres à partir du formulaire
    (creation_parametres, parametres) = lire_formulaire(liste_exercice, form)
    if creation_parametres:
        # creation du fichier zip contenant les exercices
        (creation_reponse, response) = creation_exercice(parametres)
        # envoie du fichier zip contenant les exercices
        if creation_reponse:
            print "Content-type: application/zip;\r\nContent-Disposition: attachment; filename=exercice.zip\r\nContent-Title: exercice.zip\r\n\r\n"
            print response
        # Retour d'une erreur en cas de probleme à la création
        else:
            creation_formulaire(response)
    ## Retour d'une erreur en cas lecture du formulaire
    else:
        creation_formulaire(parametres)

if __name__ == "__main__":
    main()
