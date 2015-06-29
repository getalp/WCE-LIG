#!/usr/bin/perl -w

# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit) 
# Homepage: http://getalp.imag.fr
#
# Authors: Tien Ngoc LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com

use strict;

while(<STDIN>) {
  s/ Mr. / Mr /g;
  #s/ Mr . / Mr /g;
  s/ mr. / mr /g;
  #s/ mr . / mr /g;
  
  s/Mr. /Mr /g;
  #s/Mr . /Mr /g;
  s/mr. /mr /g;
  #s/mr . /mr /g;
  
  s/ M. / M /g;
  s/ m. / m /g;
  #s/ M . / M /g;
  #s/ m . / m /g;
  s/M. /M /g;
  s/m. /m /g;
  #s/M . /M /g;
  #s/m . /m /g;
  #confuse 
  #ex: ... name . --> ... nam
  
  s/ W. / W /g;
  s/ w. / w /g;
  #s/ W . / W /g;
  #s/ w . / w /g;
  s/W. /W /g;
  s/w. /w /g;
  #s/W . /W /g;
  #s/w . /w /g;
    
  s/ Dr. / Dr /g;
  s/ dr. / dr /g;
  #s/ Dr . / Dr /g;
  #s/ dr . / dr /g;
  s/Dr. /Dr /g;
  s/dr. /dr /g;
  #s/Dr . /Dr /g;
  #s/dr . /dr /g;
      
  print $_;
}
