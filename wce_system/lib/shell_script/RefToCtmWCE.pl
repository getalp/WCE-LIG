#!/usr/bin/perl -w

use strict;
use warnings;


if (@ARGV < 1)
{
	print "<fichier contenant les references>\n";
	die "nb args invalide\n";
}

open FIC, $ARGV[0] or die "erreur ouverture fichier $ARGV[0]\n";

my $Contenu;
my $BaseFichier;
my $BaseNameFichier;
my $Compteur;

foreach (<FIC>)
{
# 	$_=~/(.*?) (.*)/;

        $BaseFichier=$ARGV[0];
        $BaseNameFichier=`/usr/bin/basename $BaseFichier`;
        chomp($BaseNameFichier);
	$Contenu=$_;

	$BaseFichier=~s/(.*)\..*/$1/;

	#$Contenu=~s/ /\n/g;

	$Compteur=0;

	open FIC2, ">${BaseFichier}.ctm" or die "erreur ouverture fichier ${BaseFichier}.ctm\n";
	
	#Tien Ngoc LE added 2014.Dec.24 - BEGIN
# 	print FIC2  "$BaseFichier 1 ${Compteur}.0 1.0 $BaseFichier\n";
# 	$Compteur++;
	#Tien Ngoc LE added 2014.Dec.24 - END

	foreach (split / /,$Contenu)
	{
		print FIC2  "$BaseNameFichier 1 ${Compteur}.0 1.0 $_\n";
		$Compteur++;
	}

	close FIC2;
}

close FIC;
