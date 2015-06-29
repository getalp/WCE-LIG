#!/bin/bash

## Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit) 
## Homepage: http://getalp.imag.fr
##
## Author: Tien LE (ngoc-tien.le@imag.fr)
## Advisors: Laurent Besacier & Benjamin Lecouteux
## URL: tienhuong.weebly.com

java -classpath bin:lib/*:config org.getalp.SenseCounter $1 $2 $3
