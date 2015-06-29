#!/usr/bin/perl -w

# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole Toolkit (eval_agent Toolkit) 
# Homepage: http://getalp.imag.fr
#
# Updated by Tien Ngoc LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com

use strict;

while(<STDIN>) {
  s/\&bar;/\|/g;   # factor separator (legacy)
  s/\& bar ;/\|/g;
  s/\&#124;/\|/g;  # factor separator
  s/\& # 124 ;/\|/g;
  s/\&lt;/\</g;    # xml
  s/\& lt ;/\</g;
  s/\&gt;/\>/g;    # xml
  s/\& gt ;/\>/g;
  s/\&bra;/\[/g;   # syntax non-terminal (legacy)
  s/\& bra ;/\[/g;
  s/\&ket;/\]/g;   # syntax non-terminal (legacy)
  s/\& ket ;/\]/g;
  s/\&quot;/\"/g;  # xml
  s/\& quot ;/\"/g;  # xml
  s/\&apos;/\'/g;  # xml
  s/\& apos ;/\'/g;  # xml
  s/\&#91;/\[/g;   # syntax non-terminal
  s/\& # 91 ;/\[/g;
  s/\&#45;/\-/g;   # Tien LE added 2014-Dec-07 U+002D - hyphen-minus (HTML: &#45;) (still not to be confused with U+2212 − minus sign) ref: http://en.wikipedia.org/wiki/Hyphen
  s/\& # 45 ;/\-/g;   
  s/\&#93;/\]/g;   # syntax non-terminal
  s/\& # 93 ;/\]/g;
  s/\&amp;/\&/g;   # escape escape
  s/\& amp ;/\&/g; # Tien LE added 2014-Dec-07
  s/jusqu \"/jusqu\'/g; 
  s/ d \" / d' /g;   
  
  s/@-@/-/g; # Tien LE added 2014-Dec-14
  
  
  print $_;
}
