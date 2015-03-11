#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name = "actimaths_web",
    version = "1.01",
    description = u"Actimaths est un fork de Pyromaths qui permet de créer des fiches d'activités mentales avec leurs corrigés au format LaTeX et PDF.",
    license = "GPL",
    author = "Jean-Baptiste Le Coz",
    author_email = "jb.lecoz@gmail.com",
    url = "http://mathecailloux.ile.nc",
    packages=['actimaths_web'],
    include_package_data=True,
    data_files=[(r'share/applications', [r'data/actimaths_web.desktop']),
                (r'share/actimaths_web', [r'data/actimaths_web.png'])],
    scripts = ["actimaths_web_start"],
    platforms = ['unix'],
    long_description = u"Actimaths est un fork de Pyromaths qui permet de créer des fiches d'activités mentales avec leurs corrigés au format LaTeX et PDF.",
    )
