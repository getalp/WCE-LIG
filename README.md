# WCE LIG: an open-source toolkit for Word Confidence Estimation
This toolkit, written in python (python3), enables you to estimate the quality of an automatic translation at word level.
It outputs a good (G) or a bad (B) label foreach word in of the translation hypothesis.

For instance:
```
Source: give me some pills
Translation hypothesis: me donner des pilules
WCE: B B G G
Reference: donnes moi des pilules
```

## What the toolkit do?
First, the toolkit pre-process the data, then, it extract some internal and external features.
Finally, it outputs a good (G) or a bad (B) label foreach word in of the translation hypothesis based on those features.
Actually, the internal features belongs to the translation system and the external features uses external toolkits to extract informations (linguistic or probabilistic)

## What are the features extracted?
1 Proper Name		&  9  Left Source Word		& 17  Left Target POS	& 25 WPP Exact & 33 Punctuation \\
2 Unknown Stemming	& 10  Left Source Stem		& 18 Left Target Word		& 26  WPP Any & 34  Stop Word \\
3 Number of Word Occurrences & 11  Right Source POS & 19  Left Target Stem		& 27  Max   & 35  Occur in Google Translate \\
4 Number of Stemming Occurrences & 12  Right Source Word		& 20 Right Target POS & 28  Min & 36 Occur in Bing Translator \\
5 Source POS  		& 13  Right Source Stem		& 21  Right Target Word		& 29  Nodes &37  Polysemy Count -- Target\\
6 Source Word			& 14  Target POS	& 22  Right Target Stem		& 30  Constituent Label  & 38  Backoff Behaviour -- Target\\
7 Source Stem			& 15  Target Word 		& 23  Longest Target $N$-gram Length			& 31  Distance To Root  &&\\
8 Left Source POS		& 16  Target Stem 		& 24  Longest Source $N$-gram Length			& 32  Numeric && \\

 
This toolkit enables you to estimate the quality of an automatic translation.

## How far can we go?
You can achieve State-of-the-Art WCE results in the WMT shared task (http://www.statmt.org/wmt14/quality-estimation-task.html) 
For English-French quality estimation task:

X-Bad = 1640     Y-Bad = 3395    Z-Bad = 4537
X-Good = 15409   Y-Good = 18306          Z-Good = 17164
B        Pr=0.4831       Rc=0.3615       F1=0.4135
G        Pr=0.8417       Rc=0.8978       F1=0.8688

## What is needed?

+ Set the WCE_ROOT environment variable (see Readme file)
+ python3
+ PyYAML-3.11
+ NLTK for python 3
+ tools: see tools directory
+ 7zip to decompress data in the input_data directory

## Repository description

<TABLE BORDER="1"> 
  <CAPTION> Voici le titre du tableau </CAPTION> 
  <TR> 
 <TH> Titre A1 </TH> 
 <TH> Titre A2 </TH> 
 <TH> Titre A3 </TH> 
 <TH> Titre A4 </TH> 
  </TR> 
  <TR> 
 <TH> Titre B1 </TH> 
 <TD> Valeur B2 </TD> 
 <TD> Valeur B3 </TD> 
 <TD> Valeur B4 </TD> 
  </TR> 
</TABLE> 

## Acknoledgement

This toolkit is part of the French National Research Agency project KEHATH (https://kehath.imag.fr/)

