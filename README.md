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
Here is the list of all the features which are used in the toolkit.


<TABLE BORDER="1"> 
<TR><TD>1 Proper Name                           </TD><TD> 17  Left Target POS                   </TD><TD> 25 WPP Exact                          </TD></TR>
<TR><TD>2 Unknown Stemming                      </TD><TD> 18 Left Target Word                   </TD><TD> 26  WPP Any                           </TD></TR>
<TR><TD>3 Number of Word Occurrences            </TD><TD> 19  Left Target Stem                  </TD><TD> 27  Max                               </TD></TR>
<TR><TD>4 Number of Stemming Occurrences        </TD><TD> 20 Right Target POS                   </TD><TD> 28  Min                               </TD></TR>
<TR><TD>5 Source POS                            </TD><TD> 21  Right Target Word                 </TD><TD> 29  Nodes                             </TD></TR>
<TR><TD>6 Source Word                           </TD><TD> 22  Right Target Stem                 </TD><TD> 30  Constituent Label                 </TD></TR>
<TR><TD>7 Source Stem                           </TD><TD> 15  Target Word                       </TD><TD> 31  Distance To Root                  </TD></TR>
<TR><TD>8 Left Source POS                       </TD><TD> 16  Target Stem                       </TD><TD> 32  Numeric                           </TD></TR>
<TR><TD>  9  Left Source Word                   </TD><TD> 17  Left Target POS                   </TD><TD> 33 Punctuation                        </TD></TR>
<TR><TD> 10  Left Source Stem                   </TD><TD> 18 Left Target Word                   </TD><TD> 34  Stop Word                         </TD></TR>
<TR><TD> 11  Right Source POS                   </TD><TD> 19  Left Target Stem                  </TD><TD> 35  Occur in Google Translate         </TD></TR>
<TR><TD> 12  Right Source Word                  </TD><TD> 20 Right Target POS                   </TD><TD> 36 Occur in Bing Translator           </TD></TR>
<TR><TD> 13  Right Source Stem                  </TD><TD> 21  Right Target Word                 </TD><TD> 37  Polysemy Count -- Target          </TD></TR>
<TR><TD> 14  Target POS                         </TD><TD> 22  Right Target Stem                 </TD><TD> 38  Backoff Behaviour -- Target       </TD></TR>
<TR><TD> 15  Target Word                        </TD><TD> 23  Longest Target $N$-gram Length    </TD><TD>                                       </TD></TR>
<TR><TD> 16  Target Stem                        </TD><TD> 24  Longest Source $N$-gram Length    </TD><TD>                                       </TD></TR>
</TABLE> 
 
 
Detailed description can be founded if the paper directory.
## How far can we go?
You can achieve State-of-the-Art WCE results in the WMT shared task (http://www.statmt.org/wmt14/quality-estimation-task.html) 
For English-French quality estimation task:

<TABLE BORDER="0"> 
<TR><TD> B              </TD><TD>  Pr=0.4831            </TD><TD> Rc=0.3615  </TD><TD> F1=0.4135 </TD></TR>
<TR><TD> G              </TD><TD>  Pr=0.8417            </TD><TD> Rc=0.8978  </TD><TD> F1=0.8688 </TD></TR>
</TABLE> 

Metrics used are Precision (Pr), Recall (Rc) and F-Measure F1.
## What is needed?

+ Set the WCE_ROOT environment variable (see Readme file)
+ python3
+ PyYAML-3.11
+ NLTK for python 3
+ tools: see tools directory
+ 7zip to decompress data in the input_data directory (see README.md in the directories "tools" and "input_data")

## Repository description

+ wce_system: contains the core of the system 
+ input_data: contains the data used to train your WCE system
+ tools: contains all the tools needed to use fully the toolkit
+ docs: contains the documentation and the scientific papers related to this toolkit

## Acknowledgement

This toolkit is part of the project KEHATH (https://kehath.imag.fr/) funded by the French National Research Agency.

