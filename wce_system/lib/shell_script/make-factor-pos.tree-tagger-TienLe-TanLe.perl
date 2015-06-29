#!/usr/bin/perl -w

#####################################################################################################
# Groupe d'Étude pour la Traduction/le Traitement Automatique des Langues et de la Parole (GETALP)
# Homepage: http://getalp.imag.fr
#
# Author: Tien LE (ngoc-tien.le@imag.fr)
# Advisors: Laurent Besacier & Benjamin Lecouteux
# URL: tienhuong.weebly.com
#####################################################################################################

#updated by
#Tien Ngoc LE (ngoc-tien.le@imag.fr)
#Tan Ngoc LE (letan.dhcn@gmail.com)

use strict;

# handle switches
use Getopt::Long "GetOptions";
#TienNLe updated 2014.05.17, 2014.12.12
my ($IN,$OUT,$TREE_TAGGER,$WORDTAGDETAIL,$WORDTAGLEMMA,$WORDBASIC,$WORDLEMMA,$BASIC,$STEM,$LANGUAGE);

#TienNLe added 2014.05.17, 2014.12.12
if (!&GetOptions('tree-tagger=s' => \$TREE_TAGGER,
				 'wordtagdetail' => \$WORDTAGDETAIL,
				 'wordtaglemma' => \$WORDTAGLEMMA,
				 'wordbasic' => \$WORDBASIC,
				 'wordlemma' => \$WORDLEMMA,
                 'basic' => \$BASIC,
                 'stem' => \$STEM,
                 'l=s' => \$LANGUAGE) ||
    !($IN = shift @ARGV) ||
    !($OUT = shift @ARGV) ||
    !defined($TREE_TAGGER) ||
    !defined($LANGUAGE)) {
	print "syntax: make-factor-pos.tree-tagger-TienLe-TanLe.perl -tree-tagger INSTALL_DIR -l LANGUAGE IN_FILE OUT_FILE [-wordtagdetail] [-wordtaglemma] [-wordbasic] [-wordlemma] [-basic] [-stem]\n";
	exit(1);
}

# define the model file for the given language
my $MODEL = undef;
$MODEL = "english-utf8" if $LANGUAGE eq "en"; #Tien LE updated 2014.Dec.19
$MODEL = "french-utf8" if $LANGUAGE eq "fr";
$MODEL = "spanish-utf8" if $LANGUAGE eq "es";
$MODEL = "german" if $LANGUAGE eq "de";
$MODEL = "italian-utf8" if $LANGUAGE eq "it";
$MODEL = "dutch" if $LANGUAGE eq "nl";
$MODEL = "bulgarian-utf8" if $LANGUAGE eq "bg";
$MODEL = "greek" if $LANGUAGE eq "el";
die("Unknown language '$LANGUAGE'") unless defined($MODEL);
$MODEL = $TREE_TAGGER."/lib/".$MODEL.".par";

# define encoding conversion into Latin1 or Greek if required 
my $CONV = "";
#$CONV = "iconv --unicode-subst=X -f utf8 -t iso-8859-1|" 
$CONV = "perl -ne 'use Encode; print encode(\"iso-8859-1\", decode(\"utf8\", \$_));' |" 
	unless $MODEL =~ /utf8/ || $LANGUAGE eq "bg";
$CONV = "perl -ne 'use Encode; print encode(\"iso-8859-7\", decode(\"utf8\", \$_));' |" 
	if $LANGUAGE eq "el";

# pipe in data into tagger, process its output
my $first = 1;
open(TAGGER,"cat $IN | $CONV".
            "perl -ne 'foreach(split){print \$_.\"\n\";}print \"eND_oF_SeNTeNCe\n\";'|".
            "$TREE_TAGGER/bin/tree-tagger -token -lemma -sgml $MODEL|");
open(OUT,">$OUT");

#TienNLe added 2014.05.17
#Spliter between the word and [lemma/basicTag/detailTag]
#my $charSplit="//";
#my $charSplit = "|||";
#my $stem = "";
#my $tag = "";
#my $result = ""

while(<TAGGER>) {
	my $charSplit = "|||";
	my ($word,$tag,$stem) = split;
	if ($word eq "eND_oF_SeNTeNCe") {
		print OUT "\n";
		$first = 1;
	}
	else {
		print OUT " " unless $first;
		if ($STEM) {
			#$stem = $word if $stem eq "<unknown>";
			$stem =~ s/\|.+//;
			print OUT $stem;
		}
		else {
			if($BASIC)
			{
				#TienNLe added comment 2014.05.17
				#Remove detail tag-name 
				$tag =~ s/\:.+//;
				print OUT $tag;
			}
			else
			{
				if($WORDLEMMA)
				{
					#TienNLe added codes 2014.05.17
					#Contain with owner-format: word/lemma 
					#$stem = $word if $stem eq "<unknown>";
					$stem =~ s/\|.+//;
				
					$tag = $word.$charSplit.$stem;
					print OUT $tag;
				}
				else
				{ 
					if($WORDTAGDETAIL)
					{
						##WORDTAGDETAIL = true
						#TienNLe added codes 2014.05.17
						#Contain with owner-format: word/POS_Tag_name_detail 
						#Note: POS_Tag_name_detail: is detail
						$tag = $word.$charSplit.$tag;
						print OUT $tag;
					}
					else 
					{
						if($WORDBASIC){
							#wordbasic -> $WORDBASIC
							#TienNLe added codes 2014.05.17
							#Note: POS_Tag_name: NOT detail
							#Contain with owner-format: word/POS_Tag_name
					
							#convert tag to BASIC tagName
							$tag =~ s/\:.+//; 
					
							#concat to word with my format: word/POS_Tag_name
							$tag = $word.$charSplit.$tag;
							print OUT $tag;
						} 
						else
						{
							if($WORDTAGLEMMA)
							{
								#wordbasic -> $WORDTAGLEMMA
								#TienNLe added codes 2014.12.12
								#Note: POS_Tag_name: NOT detail
								#Contain with owner-format: word/POS_Tag_name
								
								#TienNLe added codes 2014.12.12
								#Contain with owner-format: word/lemma 
								#$stem = $word if $stem eq "<unknown>";
								$stem =~ s/\|.+//;
							
								#$tag = $word.$charSplit.$stem;
					
								#convert tag to BASIC tagName
								$tag =~ s/\:.+//; 
					
								#concat to word with my format: word/POS_Tag_name/lemma
								$tag = $word.$charSplit.$tag.$charSplit.$stem;
								#$result = $word.$charSplit.$tag.$charSplit.$stem;
								print OUT $tag;
							}
							else
							{
								#No input parameters
								print OUT $tag;
							}
						}
					}
				}
			}
		}
		$first = 0;
	}
}
close(TAGGER);
