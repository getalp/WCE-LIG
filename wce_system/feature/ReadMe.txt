ReadMe.txt trong "Feature"
**************************

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

List of Features:
======================
Punctuation
Stop Word
Numeric
Proper Name
unknown lemma ***
Number Of Occurrences word
Number of occurrences stem (frequency of stemmed word) ***
Polysemy Count - Target (ES) #chu y: ket qua se duoc cong don -> nen xoa truoc khi chay lai
Polysemy Count - Target (EN) #chu y: ket qua se duoc cong don

??? Polysemy Count - Source (FR) #chu y: ket qua se duoc cong don
?? Vi chua co alignment giua Target to Source

Longest Target gram length
Backoff Behaviour
Constituent Label #chu y: yeu cau can phai co NLTK support python 3
Distance to Root #chu y: yeu cau can phai co NLTK support python 3
Longest Source gram length (hoi rac roi)
18 features: Target; Right_Target; Left_Target; Source; Right_Source; Left_Source (Word; POS; Stemming)
WPP any
Max
Min
Nodes
WPP Exact
Occur in Google Translator
Occur in Bing Translator

label_word ***

*** Null Link (KHONG DUNG Feature nay nua)

*********************
****old version******
Target Word
Source Word
Target POS
Source POS
Right Target Context
Left Target Context
Right Source Context
Left Source Context
*********************