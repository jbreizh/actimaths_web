#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# Actimaths
# Un programme en Python qui permet de créer des presentation de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2013 -- Jean-Baptiste Le Coz (jb.lecoz@gmail.com)
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from cgitb import enable
from os import chdir
from os.path import join, dirname

def main():
    port = input("Quel port doit utiliser actimaths_web (supérieur à 1024) ?")
    print "Actimaths_web démarre sur le port %s ..." %port
    try:
        enable()
        chdir(join(dirname(__file__),'www'))
        serv = HTTPServer( ('', port), CGIHTTPRequestHandler)
        print "... Actimaths_web en attente sur le port %s" %port
        serv.serve_forever()
    except:
        print "Erreur"

if __name__ == "__main__":
	main()
