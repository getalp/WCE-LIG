/*
 * =====================================================================================
 *
 *       Filename:  main.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  06/05/07 13:40:26 CEST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:   (), 
 *        Company:  
 *
 * =====================================================================================
 */


#include "alignContainer.h"
#include <strings.h>
#include <string.h>
#include <fstream>

float Comp(const char *a, const char *b)
{
	char Mot[2048];
	char Mot2[2048];

	int taille = strlen(a);
	int Curseur=0;
	char cur=a[0];

	while (Curseur <= taille && cur != ':')
	{

		Mot[Curseur++] = cur;

		Mot[Curseur] = '\0';
		cur = a[Curseur];
	}

	Curseur=0;
	cur=b[0];

	taille = strlen(b);

	while (Curseur <= taille && cur != ':')
	{

		Mot2[Curseur++] = cur;

		Mot2[Curseur] = '\0';
		cur = b[Curseur];
	}


	//cout <<a<<" comp.. "<<b<<endl;
	if (strcasecmp(Mot, Mot2) == 0) return 12;
	
	else return -2;
}

int main(int argc, char **argv)
{
	//char *Ref[27]={"DANS", "la", "mesure", "OÙ", "ON"    ,  "CONSERVERAIT", "le", "JOUEUR", "À", "BORDEAUX", "C", "EST", "SÛR" , "QU", "IL"       ,  "Y"  , "A"       , "UNE", "DETTE", "plus", "que", "morale", "avec", "LE", "REAL", "de", "MADRID"};

	const char *Ref_[]={"le:2", "grand:7","lapin", "blanc","court","dans","la","prairie:3","jaune","la", "son","ami","le", "canard", "hautain","1","2","3","4","o","o","o","o","o","o","o","o","o","o"};
	const char *Hyp_[]={"1","2","3","4","le:3","super","grand:8","lapin","noir","court","dans","le","petite","jolie","prairie:4","la","le","canard","5","6","7","1"};

	vector<const char *> Ref;
	vector<const char *> Hyp;
	
	ifstream fic1;
	fic1.open(argv[1]);
	ifstream fic2;
	fic2.open(argv[2]);

	int nb = 0;

	while(fic1.eof() == false) 
	{
		char *test = new char[100];
		fic1.getline(test, 100);
		Ref.push_back(test);
		nb++;
		cout <<"fic1 : chargement du mot : "<<test<<endl;
	}

	cerr <<nb<<" mots charges dans la reference 1"<<endl;

	nb=0;
	while(fic2.eof() == false) 
	{
		char *test = new char[100];
		fic2.getline(test, 100);
		Hyp.push_back(test);
		nb++;
		cout <<"fic2 : chargement du mot : "<<test<<endl;
	}


	cerr <<nb<<" mots charges dans la reference 2"<<endl;




/*	for (int i = 0; i < 22; i++) 
	{
		Hyp.push_back(Hyp_[i]);
	}*/

	 //char *Hyp[21]={"la", "mesure", "EN", "CONCERT", "VOIT",         "le","JOUR", "EN",  "POSSESSION", "ILS", "VIENNENT", "D",  "ÊTRE",  "plus", "que" ,"morale", "avec", "L", "AVAL", "de", "PARIS"};

//	class SmithWatermanDTW<const char *, const char *, float> MaDTW(Hyp.size(), Ref, 10, Comp,NULL , 5, 5, 5);
	
	//class  AlignDTW<const char *, const char *, float> MaDTW(Hyp.size(), Ref, Comp, NULL, 4, 4.5, 6); //best
	class  AlignDTW<const char *, const char *, float> MaDTW(Hyp.size(), Ref, Comp, NULL, 4, 8, 5); //best
	//class  AlignDTW<const char *, const char *, float> MaDTW(Hyp.size(), Ref, Comp, NULL, 10, 4, 2); //best
	

	cout <<"init : "<<Hyp.size() <<" et "<<Ref.size()<<endl;
	MaDTW.InitDTW(-INFINI, 0, 0, true, 100);
	cout <<"calcul dtw"<<endl;
	MaDTW.CalculerCheminDTW(Hyp, 0, 0);
	
	//for (int i = 0; i < 3; i++)
	//{

	cout <<"backtrack"<<endl;
	MaDTW.BackTrack(Hyp);

	cout <<"print align"<<endl;
	MaDTW.PrintBestAlign(Hyp);
	//cout<<endl<<endl;

	//cout <<"alignements : "<<endl;

	//for (int i = 0; i < Hyp.size(); i++)
	//	cout <<"mot "<<Hyp[i]<<" : "<<MaDTW.IsAligned(i)<<endl;

	//}
	//MaDTW.CalculerCheminDTW(Ref, Hyp, 8, 2);
	//MaDTW.BackTrack(Ref, Hyp);
}

