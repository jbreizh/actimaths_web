# Pyromaths
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d"exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if notPopen, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


import math
import random
import string
from outils import Arithmetique, Affichage

def mon_int(t):  # retourne un entier texte sous la forme d'un nombre, zéro sinon
    if t == '':
        t = 0
    elif ('1234567890').count(t):
        t = int(t)
    else:
        t = 0
    return t

def valeurs(nbre_min, nbre_max, nbre_decimal_1, nbre_decimal_2):
    while 1:
        nba = Arithmetique.valeur_alea(nbre_min*10**nbre_decimal_1, nbre_max*10**nbre_decimal_1)
        if nba - (nba // 10) * 10:
            break
    while 1:
        nbb = Arithmetique.valeur_alea(nbre_min*10**nbre_decimal_2, nbre_max*10**nbre_decimal_2)
        if nbb - (nbb // 10) * 10:
            break
    nba = nba * 10 ** -nbre_decimal_1
    nbb = nbb * 10 ** -nbre_decimal_2
    deca = [str(nba)[i] for i in range(len(str(nba)))]
    decb = [str(nbb)[i] for i in range(len(str(nbb)))]
    if deca.count('.'):
        posa = deca.index('.')
    else:
        posa = len(deca)
    if decb.count('.'):
        posb = decb.index('.')
    else:
        posb = len(decb)

    lavtvirg = max(posa, posb)
    laprvirg = max(len(deca) - posa, len(decb) - posb)
    return (nba, nbb, deca, decb, lavtvirg, laprvirg)

def lignes(ligne, deca, lavtvirg, laprvirg):
    if deca.count('.'):
        posa = deca.index('.')
    else:
        posa = len(deca)
    if posa < lavtvirg:
        for i in range(lavtvirg - posa):
            ligne.append('')
    for i in range(len(deca)):
        if deca[i] == '.':
            ligne.append(',')
        else:
            ligne.append(str(deca[i]))
    for i in range(laprvirg - (len(deca) - posa)):
        if ligne.count(','):
            ligne.append('0')
        else:
            ligne.append(',')
    return ligne

#---------------methode pour la somme--------------------------------

def retenues_somme(ligne1, ligne2):
    lg = len(ligne1)
    ligne0 = ['' for i in range(lg)]
    for i in range(lg - 1):
        #on déplace la retenue pour qu'elle ne soit pas au-dessus de la virgule
        if ligne1[(lg - i) - 1] == ',' and ligne0[(lg - i) - 1] == '1':
            ligne0[(lg - i) - 1] = ''
            ligne0[(lg - i) - 2] = '1'
        elif mon_int(ligne1[(lg - i) - 1]) + mon_int(ligne2[(lg - i) - 1]) + mon_int(ligne0[(lg - i) - 1]) > 9:
            ligne0[(lg - i) - 2] = '1'
    return ligne0

def tex_somme(exo, cor,nbre_min, nbre_max, nbre_decimal_1, nbre_decimal_2):
    (ligne1, ligne2) = ([''], ['+'])
    (nba, nbb, deca, decb, lavtvirg, laprvirg) = valeurs(nbre_min, nbre_max, nbre_decimal_1, nbre_decimal_2)
    total = nba + nbb
    dectotal = [str(total)[i] for i in range(len(str(total)))]
    if dectotal.count('.'):
        postotal = dectotal.index('.')
    else:
        postotal = len(dectotal)
    if postotal <= lavtvirg:
        ligne3 = ['']
    else:
        ligne3 = []
    ligne1 = lignes(ligne1, deca, lavtvirg, laprvirg)
    ligne2 = lignes(ligne2, decb, lavtvirg, laprvirg)
    ligne3 = lignes(ligne3, dectotal, lavtvirg, laprvirg)
    ligne0 = retenues_somme(ligne1, ligne2)
    if ligne0[0] == '1':
        ligne0[0] = '\\tiny 1'
    exo.append('$$ %s + %s = \\ldots $$' % (Affichage.decimaux(nba), Affichage.decimaux(nbb)))
    cor.append('\\begin{footnotesize}')
    cor.append('\\begin{tabular}[t]{*{%s}{c}}' % (lavtvirg + laprvirg + 1))
    cor.append('%s \\\\' % ' & \\tiny '.join(ligne0))
    cor.append('%s \\\\' % ' & '.join(ligne1))
    cor.append('%s \\\\\n\\hline' % ' & '.join(ligne2))
    cor.append('%s \\\\' % ' & '.join(ligne3))
    cor.append('\\end{tabular}\\par')
    cor.append('\\end{footnotesize}')
    formule = '%s+%s = %s' % (Affichage.decimaux(nba, 1), Affichage.decimaux(nbb, 1), Affichage.decimaux(nba + nbb, 1))
    cor.append((u'\\[ \\boxed{%s} \\] ').expandtabs(2 * 3) % (formule))

#---------------methode pour la difference posé--------------------------------

def retenues_diff(ligne1, ligne2):
    lg = len(ligne1)
    ret = 0
    for i in range(lg - 1):
        if not (ligne1[(lg - i) - 1] == ',' and ret):
            if mon_int(ligne1[(lg - i) - 1]) < mon_int(ligne2[(lg - i) -
                    1]) + ret:
                ligne1[(lg - i) - 1] = '$_1$%s' % ligne1[(lg - i) - 1]
                tmpret = 1
            else:
                tmpret = 0
            if ret:
                ligne2[(lg - i) - 1] = '%s$_1$' % ligne2[(lg - i) - 1]
            ret = tmpret
    return (ligne1, ligne2)

def tex_difference(exo, cor, nbre_min, nbre_max, nbre_decimal_1, nbre_decimal_2):
    (ligne1, ligne2) = ([''], ['-'])
    (nba, nbb, deca, decb, lavtvirg, laprvirg) = valeurs(nbre_min, nbre_max, nbre_decimal_1, nbre_decimal_2)
    if nba < nbb:
        (nba, nbb, deca, decb) = (nbb, nba, decb, deca)
    total = nba - nbb
    dectotal = [str(total)[i] for i in range(len(str(total)))]
    if dectotal.count('.'):
        postotal = dectotal.index('.')
    else:
        postotal = len(dectotal)
    if postotal <= lavtvirg:
        ligne3 = ['']
    else:
        ligne3 = []

    ligne1 = lignes(ligne1, deca, lavtvirg, laprvirg)
    ligne2 = lignes(ligne2, decb, lavtvirg, laprvirg)
    ligne3 = lignes(ligne3, dectotal, lavtvirg, laprvirg)
    (ligne1, ligne2) = retenues_diff(ligne1, ligne2)
    exo.append('$$ %s - %s = \\ldots $$' % (Affichage.decimaux(nba), Affichage.decimaux(nbb)))
    cor.append('\\begin{footnotesize}')
    cor.append('\\begin{tabular}[t]{*{%s}{c}}' % (lavtvirg + laprvirg + 1))
    cor.append('%s \\\\' % ' & '.join(ligne1))
    cor.append('%s \\\\\n\\hline' % ' & '.join(ligne2))
    cor.append('%s \\\\' % ' & '.join(ligne3))
    cor.append('\\end{tabular}\\par')
    cor.append('\\end{footnotesize}')
    formule = '%s-%s = %s' % (Affichage.decimaux(nba, 1), Affichage.decimaux(nbb, 1), Affichage.decimaux(nba - nbb, 1))
    cor.append((u'\\[ \\boxed{%s} \\] ').expandtabs(2 * 3) % (formule))

#--------------Construction des exercices-----------------------

def AdditionHeure(parametre):
    question = "Poser l'addition suivante :"
    exo = [ ]
    cor = [ ]
    tex_somme(exo, cor, parametre[0], parametre[1], random.randint(1,2), random.randint(1,2))
    return exo, cor, question

def SoustractionHeure(parametre):
    question = "Poser la soustraction suivante :"
    exo = [ ]
    cor = [ ]
    tex_difference(exo, cor, parametre[0], parametre[1], random.randint(1,2), random.randint(1,2))
    return exo, cor, question

#---------------methode pour l'horloge--------------------------------

def tex_horloge(tex, heure, minute):
    tex.append("\\begin{center}")
    tex.append("\\psset{unit=0.5cm}")
    tex.append("\\begin{pspicture}(-5,-5)(5,5)")
    tex.append("\\pscircle[fillstyle=solid, fillcolor=white]{5}")
    tex.append("\\pscircle[fillstyle=solid, fillcolor=white]{4.5}")
    tex.append("\\pscircle[fillstyle=solid, fillcolor=white]{0.1}")
    tex.append("\\SpecialCoor")
    tex.append("\\multido{\\i=0+30}{12}{\\psline(4.5;\\i)(5;\\i)}")
    tex.append("\\multido{\\i=0+90}{4}{\\psline(4;\\i)(5;\\i)}")
    tex.append("\\psline[linewidth=0.2](0;0)(2;%s)" % (90 - heure*30 - minute*0.5))
    tex.append("\\psline[linewidth=0.1](0;0)(4;%s)" % (90 - minute*6))
    tex.append("\\NormalCoor")
    tex.append("\\end{pspicture}")
    tex.append("\\end{center}")

#--------------Construction des exercices-----------------------

def LectureHorloge(parametre):
    heure = random.randrange(12)
    minute = random.randrange(0,60,5)
    # initialisation
    question = u"Quelle heure est-il ? :"
    exo = []
    cor = []
    # affichage de l'horloge
    tex_horloge(exo, heure, minute)
    tex_horloge(cor, heure, minute)
    # corrige
    cor.append("\\begin{center}")
    if minute > 9:
        cor.append("Il est $\\boxed{%sh%s}$ ou $\\boxed{%sh%s}$" %(heure, minute, heure+12, minute))
    else:
        cor.append("Il est $\\boxed{%sh0%s}$ ou $\\boxed{%sh0%s}$" %(heure, minute, heure+12, minute))
    cor.append("\\end{center}")
    return (exo, cor, question)

#---------------methode pour les conversions--------------------------------

def tex_tableau(tex, contenu):
    nombreColonne = len(contenu)
    if nombreColonne != 0:
        nombreLigne = len(contenu[0])
        # entete du tableau
        tex.append("\\begin{center}")
        ligne = "\\begin{tabular}{|"
        for i in range(len(contenu)):
            ligne += "c|"
        ligne += "}"
        tex.append(ligne)
        # corps du tableau
        for i in range(nombreLigne):
            tex.append("\\hline")
            ligne = ""
            for j in range(nombreColonne):
                ligne += "%s" % contenu[j][i]
                if j != nombreColonne - 1:
                   ligne += "&"
            ligne += "\\\\"
            tex.append(ligne)
        tex.append("\\hline")
        # fin du tableau
        tex.append("\\end{tabular}")
        tex.append("\\end{center}")

#--------------Construction des exercices-----------------------
def ConversionHeureMinute(parametre):
    # variables
    heure =  random.randrange(parametre[0],parametre[1])
    minute = heure * 60
    choix = random.randrange(2)
    if choix:
        contenuTableauEnonce = [["Heure","Minute"],[1,60],[heure,"\\ldots"]]
    else:
        contenuTableauEnonce = [["Heure","Minute"],[1,60],["\\ldots",minute]]
    contenuTableauCorrige = [["Heure","Minute"],[1,60],[heure,minute]]
    # initialisation
    question = u"Fais la conversion :"
    exo = []
    cor = []
    # affichage du tableau
    tex_tableau(exo, contenuTableauEnonce)
    tex_tableau(cor, contenuTableauCorrige)
    # enonce et corrige
    if choix:
        exo.append("$$ %s h = \\ldots min $$" % heure)
        cor.append("$$ %s h = %s \\times 60 min $$" % (heure, heure))
        cor.append("$$ %s h = \\boxed{%s min} $$" % (heure, minute))
    else:
        exo.append("$$ %s min = \\ldots h $$" % minute)
        cor.append("$$ %s min = %s \\div 60 h $$" % (minute, minute))
        cor.append("$$ %s min = \\boxed{%s h} $$" % (minute, heure))
    return (exo, cor, question)

def ConversionMinuteSeconde(parametre):
    # variables
    minute =  random.randrange(parametre[0],parametre[1])
    seconde = minute * 60
    choix = random.randrange(2)
    if choix:
        contenuTableauEnonce = [["Minute","Seconde"],[1,60],[minute,"\\ldots"]]
    else:
        contenuTableauEnonce = [["Minute","Seconde"],[1,60],["\\ldots",seconde]]
    contenuTableauCorrige = [["Minute","Seconde"],[1,60],[minute,seconde]]
    # initialisation
    question = u"Fais la conversion :"
    exo = []
    cor = []
    # affichage du tableau
    tex_tableau(exo, contenuTableauEnonce)
    tex_tableau(cor, contenuTableauCorrige)
    # enonce et corrige
    if choix:
        exo.append("$$ %s min = \\ldots s $$" % minute)
        cor.append("$$ %s min = %s \\times 60 s $$" % (minute, minute))
        cor.append("$$ %s min = \\boxed{%s s} $$" % (minute, seconde))
    else:
        exo.append("$$ %s s = \\ldots min $$" % seconde)
        cor.append("$$ %s s = %s \\div 60 min $$" % (seconde, seconde))
        cor.append("$$ %s s = \\boxed{%s min} $$" % (seconde, minute))
    return (exo, cor, question)

