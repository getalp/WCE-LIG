/*
 * =====================================================================================
 * 
 *       Filename:  alignContainer.h
 * 
 *    Description:  generic DTW and SwithWaterman implementations 
 * 
 *        Version:  1.2
 *        Created:  05/03/07 10:41:03 CEST
 *       Revision:  none
 *       Compiler:  g++
 * 
 *         Author:  LECOUTEUX Benjamin 
 *        Company:  LIA
 * 
 * =====================================================================================
 */


#ifndef INFINI
#define INFINI 1000000
#endif

#include <deque>
#include <vector>
#include <iostream>
#include <algorithm>
#include <fstream>

using namespace std;

struct SOMMET
{
	float Max;
	int MaxRef;
	int MaxHyp;
};




template <class Tr, class Th, class P> class AlignDTW
{
	protected:
		P Sub;
		P Ins;
		P Del;

		int NbCommunsPrecedent;

		P **MatriceDTW;
		P (*CalculerDistance)(Tr Ref, Th Hyp);
		bool (*PrintRefOrHyp)(Tr Ref, Th Hyp, ofstream *Out);
		static P DistanceDefaut(Tr Ref, Th Hyp);
		static bool PrintDefaultRefOrHyp(Tr Ref, Th Hyp, ofstream *Out=NULL);
		P MaxDTW(P a, P b, P c);

		unsigned int TailleMaxHyp;


		vector<Tr> *Reference;
		vector<int> SubInsDel;
		vector<int> RefVec;
		vector<int> HypVec;

		int WindowCut;
		bool FastCut;
		bool PrintVerbose;
		int *BacktraceRef;
		int *BacktraceHyp;

		ofstream *Out;
	public:
		int *Maxis/*[2048]*/;
		int *MaxTailleRef/*[2048]*/;
		int *MinTailleRef/*[2048]*/;

		bool IsAligned(int HypNum);
		int GetAlign(int HypNum);
		
		void SetOut(ofstream *COut)
		{	
			Out = COut;
		};

		void SetPrintVerbose(bool v){PrintVerbose = v;};

		P GetMax(vector<Th> &Hyp, int OriRef=0, int OriHyp=0);
		void PrintBestAlign(vector<Th> &Hyp, int *ins=NULL, int *sub=NULL, int *del=NULL, int *ok=NULL);

		AlignDTW(unsigned int TailleMaxRef, vector<Tr> &Ref, P (*DistFunction)(Tr a, Th b)=NULL,bool (*PrintRefOrHyp)(Tr Ref, Th Hyp, ofstream *Out)=NULL ,P Sub=4, P Ins=8, P Del=5);
		void InitDTW(P FillBorder=-INFINI, P Fill=0, P Init=0, bool FastCut = false, int WindowCut = 30);
		P CalculerCheminDTW(vector<Th> &Hyp, int OriI = 0, int OriJ = 0);
		void BackTrack(vector<Th> &Hyp, int OriRef=0, int OriHyp=0);
		~AlignDTW();
};




template <class Tr, class Th, class P> class SmithWatermanDTW:public AlignDTW<Tr,Th,P>
{
	private:


		struct SVG_SWDTW
		{
			P MaxI;
			P MaxJ;
			int IdMaxI;
			int IdMaxJ;
		};

		struct SVG_SWDTW **SvgMatrice;



		P MaxOfAll;
		P *MaxI;
		P *MaxJ;

		int *IdMaxI;
		int *IdMaxJ;

		P MaxDTW(P a, P b, P c, P d);


		deque<SOMMET *> Maximums;

		//deque<P> Maximums;
		//deque<int> MaxRef;
		//deque<int> MaxHyp;

		int NbMaximums;

	public:

		SmithWatermanDTW(int TailleMaxHyp, vector<Tr> &Ref, int NbMax, P (*DistFunction)(Tr a, Th b)=NULL, bool (*PrintRefOrHyp)(Tr Ref, Th Hyp)=NULL , P Sub=1, P Ins=1, P Del=1);
		void InitDTW(P FillBorder=0.0, P Fill=0.0, P Init=0.0, bool FastCut = false, int WindowCut = 30);
		~SmithWatermanDTW();
		P CalculerCheminDTW(vector<Th> &Hyp, int OriI = 0, int OriJ = 0);
		void BackTrack(vector<Th> &Hyp, int Best = 0);

};


template <class Tr, class Th, class P> P SmithWatermanDTW<Tr, Th, P>::MaxDTW(P a, P b, P c, P d)
{
	if (a >= b && a >= c && a >= d) return a;
	if (b >= a && b >= c && b >= d) return b;
	if (c >= a && c >= b && c >= d) return c;
	return d;
}



template <class Tr, class Th, class P> AlignDTW<Tr,Th,P>::AlignDTW(unsigned int TailleMaxHyp, vector<Tr> &Ref , P (*DistFunction)(Tr a, Th b),bool (*PrintRefOrHyp)(Tr Ref, Th Hyp, ofstream *Out) , P Sub, P Ins, P Del)
{
	unsigned int i, Max;


	Out = static_cast<ofstream*>(&cout);

	Reference = &Ref;

	WindowCut = 50;
	MatriceDTW = new P*[TailleMaxHyp];

	
	for (i = 0; i < TailleMaxHyp; i++)
		MatriceDTW[i] = new P[(*Reference).size()];	


	Maxis = new int[(*Reference).size()];
	MaxTailleRef = new int[ (*Reference).size()  ];
	MinTailleRef = new int[ (*Reference).size()  ];


	BacktraceRef = new int[(*Reference).size()];
	BacktraceHyp = new int[TailleMaxHyp];

	if ((*Reference).size() > TailleMaxHyp) Max = (*Reference).size();
	else Max = TailleMaxHyp;


	//BacktraceAlg = new int[Max];


	FastCut = false;

	this->TailleMaxHyp = TailleMaxHyp;
	this->Sub = Sub;
	this->Ins = Ins;
	this->Del = Del;

	if (DistFunction) CalculerDistance = DistFunction;
	else CalculerDistance = DistanceDefaut;

	if (PrintRefOrHyp) this->PrintRefOrHyp = PrintRefOrHyp;
	else this->PrintRefOrHyp = PrintDefaultRefOrHyp;

}


template <class Tr, class Th, class P> AlignDTW<Tr,Th,P>::~AlignDTW()
{
	int i;

	//delete [] BacktraceRef;
	//delete [] BacktraceHyp;
	//delete [] BacktraceAlg;

	for (i = 0; i < TailleMaxHyp; i++)
		delete [] MatriceDTW[i];

	delete [] MatriceDTW;
}

template <class Tr, class Th, class P> P AlignDTW<Tr,Th,P>::MaxDTW(P a, P b, P c)
{
	if (a >= b && a >= c) return a;
	if (b >= a && b >= c) return b;
	return c;
}


template <class Tr, class Th, class P> bool AlignDTW<Tr,Th,P>::PrintDefaultRefOrHyp(Tr Ref, Th Hyp, ofstream *Out)
{
	if (Out == NULL) Out = static_cast<ofstream*>(&cout);

	if (Ref) *Out << Ref<<"\t";
	else *Out <<"-\t";

	if (Hyp) *Out << Hyp<<"\t";
	else *Out <<"-\t";

	return true;
}

template <class Tr, class Th, class P> P AlignDTW<Tr,Th,P>::DistanceDefaut(Tr a, Th b)
{
	if (a == (Tr)b) return 5;
	else return -20;
}



template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::InitDTW(P FillBorder, P Fill, P Init, bool FastCut, int WindowCut)
{
	unsigned int i, j;

	this->WindowCut = WindowCut;

	this->FastCut = FastCut;

	for (i = 0; i < (*Reference).size(); i++)
		MatriceDTW[0][i] = FillBorder;

	for (i = 0; i < TailleMaxHyp; i++)
		MatriceDTW[i][0] = FillBorder;

	for (i = 1; i < TailleMaxHyp; i++)
		for (j = 1; j < (*Reference).size(); j++)
			MatriceDTW[i][j] = Fill;

	MatriceDTW[0][0] = Init;
}


template <class Tr, class Th, class P> void SmithWatermanDTW<Tr,Th, P>::BackTrack( vector<Th> &Hyp, int Best)
{
	//int BestHyp = MaxHyp.front();
	//int BestRef = MaxRef.front();
	int BestHyp, BestRef, i;

	deque<SOMMET*>::iterator itMax;
	//deque<SOMMET *>::iterator itMax;
	//deque<SOMMET *>::iterator itMax;
	//deque<int>::iterator itHyp;

	cerr <<"nombre d'entrees : "<<Maximums.size()<<endl;

	for (itMax = Maximums.begin(), i = 0; itMax != Maximums.end() && i < Maximums.size() && i < Best ;itMax++, i++);

	cout <<"max : "<<(*itMax)->Max;

	if (itMax != Maximums.end())
	{
		BestHyp = (*itMax)->MaxHyp;
		BestRef = (*itMax)->MaxRef;

		cout <<"alignement sur : "<<BestHyp<<", "<<BestRef<<endl;

		AlignDTW<Tr,Th,P>::BackTrack(Hyp, BestRef, BestHyp);
	}
	//else cerr <<"depassement du nombre de solutions"<<endl;

}


template <class Tr, class Th, class P> int AlignDTW<Tr,Th,P>::GetAlign(int HypNum)
{
	//cout <<"isaligned : BacktraceHyp["<<HypNum<<"] : "<<BacktraceHyp[HypNum]<<endl;

	if (BacktraceHyp[HypNum] >= 0) return BacktraceHyp[HypNum];
	return -1;
}




template <class Tr, class Th, class P> bool AlignDTW<Tr,Th,P>::IsAligned(int HypNum)
{
	//cout <<"isaligned : BacktraceHyp["<<HypNum<<"] : "<<BacktraceHyp[HypNum]<<endl;

	if (HypNum >= 0 &&  BacktraceHyp[HypNum] >= 0) return true;
	return false;
}


template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::PrintBestAlign(vector<Th> &Hyp, int *ins, int *sub, int *del, int *ok)
{
	int tmp1, tmp2, tmp3;

	if (ok)  (*ok)=0;
	if (ins) (*ins)=0;
	if (del) (*del)=0;
	if (sub) (*sub)=0;


	if (Out == NULL) Out = static_cast<ofstream*>(&cout);
	//cout <<endl<<endl;

	//cout <<"--->"<<endl;
	bool ValidPrint;

	if (PrintVerbose)
	{
		*Out <<"alignment : "<<endl<<endl;
		*Out <<"state\tRef\tHyp"<<endl;
	}

	while (AlignDTW<Tr,Th,P>::SubInsDel.size())
	{
		tmp1 = AlignDTW<Tr,Th,P>::SubInsDel.back();
		AlignDTW<Tr,Th,P>::SubInsDel.pop_back();

		if (PrintVerbose)
		{
			if (tmp1 == 0)	
			{
				*Out <<"ok\t";
				if (ok) (*ok)++;
			}
			else if (tmp1 == 1) 
			{
				*Out <<"ins\t";
				if (ins) (*ins)++;
			}
			else if (tmp1 == 2) 
			{
				*Out <<"del\t";
				if (del) (*del)++;
			}
			else 
			{
				*Out <<"sub\t";
				if (sub) (*sub)++;
			}
		}

		tmp2 = AlignDTW<Tr,Th,P>::RefVec.back();
		AlignDTW<Tr,Th,P>::RefVec.pop_back();

		tmp3 = AlignDTW<Tr,Th,P>::HypVec.back();
		AlignDTW<Tr,Th,P>::HypVec.pop_back();



		if (tmp2 >= 0 && tmp3 >=0) ValidPrint = PrintRefOrHyp((*Reference)[tmp2], Hyp[tmp3], Out);
		else if (tmp2 >= 0) ValidPrint = PrintRefOrHyp((*Reference)[tmp2], NULL, Out);
		else if (tmp3 >= 0) ValidPrint = PrintRefOrHyp(NULL, Hyp[tmp3], Out);
		else ValidPrint = PrintRefOrHyp(NULL, NULL, Out);

		if (PrintVerbose) *Out << endl;
		else if (ValidPrint) *Out <<endl;
	}
}

template <class Tr, class Th, class P> P AlignDTW<Tr,Th,P>::GetMax(vector<Th> &Hyp, int OriRef, int OriHyp)
{
	int i,j;

	if (OriHyp) i = OriHyp;
	else	i = Hyp.size()-1;

	if (OriRef) j = OriRef;
	else j = (*Reference).size()-1;


	P Max = -INFINI;


	if (FastCut == true)
	{
		j = Maxis[i];
		//cout <<" max["<<i<<"] choisi --> "<<j<<" : "<<(*Reference)[j]->cMot<<endl;
		Max = MatriceDTW[i][j];
	}
	else
	{
		for (int k = 0; k < (int) (*Reference).size(); k++)
			if (MatriceDTW[i][k] > Max)
			{
				j = k;
				Max = MatriceDTW[i][k];
			}
	}

	return Max;
}

template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::BackTrack(vector<Th> &Hyp, int OriRef, int OriHyp)
{
	P Score;
	P Diag;
	P Left;
	P Up;

	int i,j;

	for (i = 0; i < (int)  (*Reference).size(); i++) BacktraceRef[i] = -1;
	for (i = 0; i < (int) Hyp.size(); i++) BacktraceHyp[i] = -1;


	if (OriHyp) i = OriHyp;
	else	i = Hyp.size()-1;

	if (OriRef) j = OriRef;
	else j = (*Reference).size()-1;


	P Max = -INFINI;

	//cout <<"cuicui :)"<<endl;

	if (FastCut == true)
	{
		j = Maxis[i];
		//cout <<" max["<<i<<"] choisi --> "<<j<<" : "<<(*Reference)[j]->cMot<<endl;
		Max = MatriceDTW[i][j];
	}
	else
	{
		for (int k = 0; k < (int) (*Reference).size(); k++)
			if (MatriceDTW[i][k] > Max)
			{
				j = k;
				Max = MatriceDTW[i][k];
			}
	}

	RefVec.clear();
	HypVec.clear();
	SubInsDel.clear();

	int svgi=-1, svgj=-1;

	while (i > 0 && j > 0)
	{
		Score = MatriceDTW[i][j];
		Diag = MatriceDTW[i-1][j-1];
		Left = MatriceDTW[i-1][j];
		Up = MatriceDTW[i][j-1];

		//Diag = Score;

		//if (Up == 0 && Diag == 0 && Left == 0) cout <<"alignement over"<<endl;

		if (Score > Up && Score > Left)
		{
			svgi=i;
			svgj=j;
			RefVec.push_back(j);
			HypVec.push_back(i);

			if (CalculerDistance((*Reference)[j], Hyp[i]) <= 0) 
			{
				SubInsDel.push_back(3);
				BacktraceRef[j] = BacktraceHyp[i] = -3;
			}
			else
			{
				SubInsDel.push_back(0);
				BacktraceRef[j] = i;
				BacktraceHyp[i] = j;
			}

			i--, j--;
		}
		else if (Up > Score && Up > Left)
		{
			SubInsDel.push_back(2);
			RefVec.push_back(j);
			HypVec.push_back(-1);
			BacktraceRef[j] = -2;
			BacktraceHyp[i] = -1;
			j--;
		}
		else 
		{
			SubInsDel.push_back(1);
			RefVec.push_back(-1);
			HypVec.push_back(i);
			BacktraceRef[j] = -1;
			BacktraceHyp[i] = -2;
			//cout <<"i--"<<endl;
			i--;
		}
	}


	while (i > 0)
	{
		Score = MatriceDTW[i][0];
		//Diag = MatriceDTW[i-1][j-1];
		Left = MatriceDTW[i-1][j];
		//Up = MatriceDTW[i][j-1];

		//Diag = Score;

		//if (Up == 0 && Diag == 0 && Left == 0) cout <<"alignement over"<<endl;

		if (Score >= Left)
		{
			RefVec.push_back(j);
			HypVec.push_back(i);

			if (CalculerDistance((*Reference)[j], Hyp[i]) <= 0) 
			{
				SubInsDel.push_back(3);
				BacktraceRef[j] = BacktraceHyp[i] = -3;
			}
			else
			{
				SubInsDel.push_back(0);
				BacktraceRef[j] = i;
				BacktraceHyp[i] = j;
			}

			i--;
		}
		else 
		{
			SubInsDel.push_back(1);
			RefVec.push_back(-1);
			HypVec.push_back(i);
			BacktraceRef[j] = -2;
			BacktraceHyp[i] = -1;
			i--;
		}
	}

	//cout <<"i : "<<i<<", j : "<<j<<endl;

	if (i >= 0 && j >= 0)
	{
		if (CalculerDistance((*Reference)[j], Hyp[i]) > 0)
		{
			SubInsDel.push_back(0);
			BacktraceRef[j] = i;
			BacktraceHyp[i] = j;
			RefVec.push_back(j);
			HypVec.push_back(i);

		}
		else
		{
			//cerr <<"le fautif !"<<endl;
			BacktraceRef[j] = -2;
			BacktraceHyp[i] = -1;


			// modif pour corriger bug d'insertion en debut (on met une substitution
			
			//SubInsDel.push_back(1);
			//RefVec.push_back(-1);
			//HypVec.push_back(i);
			
			SubInsDel.push_back(3);
			RefVec.push_back(j);
			HypVec.push_back(i);
		}
	}
}


template <class Tr, class Th, class P> SmithWatermanDTW<Tr,Th,P>::SmithWatermanDTW(int TailleMaxHyp, vector<Tr> &Ref, int NbMax,  P (*DistFunction)(Tr a, Th b), bool (*PrintRefOrHyp)(Tr a, Th b), P Sub, P Ins, P Del):AlignDTW<Tr,Th,P>(TailleMaxHyp, Ref, DistFunction, PrintRefOrHyp ,Sub, Ins, Del)
{
	int i;

	NbMaximums = NbMax;

	MaxI = new P[Ref.size()];
	MaxJ = new P[TailleMaxHyp];

	IdMaxI = new int[Ref.size()];
	IdMaxJ = new int[TailleMaxHyp];

	SvgMatrice = new struct SVG_SWDTW*[TailleMaxHyp];

	for (i = 0; i < TailleMaxHyp; i++)
		SvgMatrice[i] = new struct SVG_SWDTW[Ref.size()];
}


template <class Tr, class Th, class P> SmithWatermanDTW<Tr,Th,P>::~SmithWatermanDTW()
{
	delete [] MaxI;
	delete [] MaxJ;

	delete [] IdMaxI;
	delete [] IdMaxJ;
}


template <class Tr, class Th, class P> void SmithWatermanDTW<Tr,Th,P>::InitDTW(P FillBorder, P Fill, P Init, bool FastCut, int WindowCut)
{
	int i;

	AlignDTW<Tr,Th,P>::InitDTW(FillBorder, Fill, Init, FastCut, WindowCut);

	for (i = 0; i < (*AlignDTW<Tr,Th,P>::Reference).size(); i++)
	{
		MaxI[i] = 0.0;
		IdMaxI[i] = 0;
	}


	for (i = 0; i < AlignDTW<Tr,Th,P>::TailleMaxHyp; i++)
	{
		MaxJ[i] = 0.0;
		IdMaxJ[i] = 0;
	}
}


bool SortByMax(SOMMET *a, SOMMET *b);
/*{
  if (a->Max > b->Max) return true;
  return false;
  }*/

template <class Tr, class Th, class P> P SmithWatermanDTW<Tr,Th,P>::CalculerCheminDTW(vector<Th> &Hyp, int OriI, int OriJ)
{
	int i, j;
	P Cout;


	if (OriI > 0 || OriJ > 0)
	{
		P TheMax = 0.0;
		int X, Y;


		//cout <<"maxJ : ";
		for (i = 0; i < OriI; i++)
		{
			MaxJ[i] = SvgMatrice[i][OriJ].MaxJ;
			IdMaxJ[i] = SvgMatrice[i][OriJ].IdMaxJ;

			//cout <<MaxJ[i]<<", ";

			if (MaxJ[i] > TheMax) TheMax = MaxJ[i], X = OriI, Y = i; 
		}

		//cout <<endl;


		//cout <<"maxI : ";
		for (j = 0; j < OriJ; j++)
		{
			MaxI[j] = SvgMatrice[OriI][j].MaxI;
			IdMaxI[j] = SvgMatrice[OriI][j].IdMaxI;

			//cout <<MaxI[j]<<", ";

			if (MaxI[j] > TheMax) TheMax = MaxI[j], X = i, Y = OriJ;
		}

		//cout <<endl;

		for (i = OriI; i < Hyp.size(); i++) MaxJ[i] = 0;
		for (j = OriJ; j < (*AlignDTW<Tr,Th,P>::Reference).size(); j++) MaxI[j] = 0;


		struct SOMMET *SommetTmp = new struct SOMMET;


		for (i = 0; i < Maximums.size(); i++)
			delete Maximums[i];

		Maximums.clear();

		SommetTmp->Max = TheMax;
		SommetTmp->MaxRef = Y;
		SommetTmp->MaxHyp = X;

		Maximums.push_front(SommetTmp);
		//Maximums.push_front(TheMax);
		//MaxRef.clear();
		//MaxHyp.clear();
		//MaxRef.push_front(Y);
		//MaxHyp.push_front(X);
	}

	float Precedent = 0.0;


	for (i = 0; i < Hyp.size(); i++)
	{
		for (j = 0; j < (*AlignDTW<Tr,Th,P>::Reference).size(); j++)
		{
			if (i >= OriI || j >= OriJ)
			{
				Cout = CalculerDistance((*AlignDTW<Tr,Th,P>::Reference)[j], Hyp[i]);

				if (i > 0 && j > 0)
				{
					AlignDTW<Tr,Th,P>::MatriceDTW[i][j] = MaxDTW(MaxI[j] - AlignDTW<Tr,Th,P>::Ins, MaxJ[i] - AlignDTW<Tr,Th,P>::Del, AlignDTW<Tr,Th,P>::MatriceDTW[i-1][j-1] + AlignDTW<Tr,Th,P>::Sub * Cout, 0.0);
				}
				else AlignDTW<Tr,Th,P>::MatriceDTW[i][j] = MaxDTW(MaxI[j] - AlignDTW<Tr,Th,P>::Ins, MaxJ[i] - AlignDTW<Tr,Th,P>::Del, AlignDTW<Tr,Th,P>::Sub * Cout, 0.0);


				if (AlignDTW<Tr,Th,P>::MatriceDTW[i][j] > MaxI[j])
				{
					MaxI[j] = AlignDTW<Tr,Th,P>::MatriceDTW[i][j];
					IdMaxI[j] = i;
				}

				if (AlignDTW<Tr,Th,P>::MatriceDTW[i][j] > MaxJ[i])
				{
					MaxJ[i] = AlignDTW<Tr,Th,P>::MatriceDTW[i][j];
					IdMaxJ[i] = j;
				}

				SvgMatrice[i][j].MaxJ = MaxJ[i];
				SvgMatrice[i][j].IdMaxJ = IdMaxJ[i];
				SvgMatrice[i][j].MaxI = MaxI[j];
				SvgMatrice[i][j].IdMaxI = IdMaxI[j];



				//cout <<i<<", "<<j<<", "<<AlignDTW<T,P>::MatriceDTW[i][j]<<endl;

				struct SOMMET *SommetTmp;

				if (Maximums.size() > 0)
				{
					if (AlignDTW<Tr,Th,P>::MatriceDTW[i][j] >= Maximums.front()->Max)
					{
						if (abs(Maximums.front()->MaxHyp-i) <= 1 && abs(Maximums.front()->MaxRef-j) <= 1)
						{
							SommetTmp = Maximums.front();
							//Maximums.pop_front();
							//MaxHyp.pop_front();
							//MaxRef.pop_front();
						}
						else
						{
							SommetTmp = new struct SOMMET;
							Maximums.push_front(SommetTmp);
						}

						SommetTmp->Max = AlignDTW<Tr,Th,P>::MatriceDTW[i][j];
						SommetTmp->MaxHyp = i;
						SommetTmp->MaxRef = j;

						//Maximums.push_front(AlignDTW<Tr,Th,P>::MatriceDTW[i][j]);
						//MaxHyp.push_front(i);
						//MaxRef.push_front(j);

						if (Maximums.size() > NbMaximums) 
						{
							delete Maximums.back();
							Maximums.pop_back();
						}
						//if (MaxHyp.size() > NbMaximums) MaxHyp.pop_back();
						//if (MaxRef.size() > NbMaximums) MaxRef.pop_back();
					}
				}
				else
				{	
					SommetTmp = new struct SOMMET;
					Maximums.push_front(SommetTmp);
					SommetTmp->Max = AlignDTW<Tr,Th,P>::MatriceDTW[i][j];
					SommetTmp->MaxHyp = i;
					SommetTmp->MaxRef = j;


					//Maximums.push_front(AlignDTW<Tr,Th,P>::MatriceDTW[i][j]);
					//MaxHyp.push_front(i);
					//MaxRef.push_front(j);
				}

				Precedent = AlignDTW<Tr,Th,P>::MatriceDTW[i][j];
			}
		}
	}		



	sort(Maximums.begin(), Maximums.end(), SortByMax);


	/*
	   cout <<" "<<"\t";

	   for (j = 0; j < Hyp.size(); j++)
	   cout <<Hyp[j]<<"\t";

	   cout <<" (j)"<<endl;

	   for (i = 0; i < Ref.size(); i++)
	   {
	   cout <<Ref[i]<<"\t";

	   for (j = 0; j < Hyp.size(); j++)
	   cout<<AlignDTW<Tr,Th,P>::MatriceDTW[j][i]<<"\t";
	   cout <<endl;
	   }
	   cout <<"(i)"<<endl;
	   */
	return AlignDTW<Tr,Th,P>::MatriceDTW[Hyp.size()-1][(*AlignDTW<Tr,Th,P>::Reference).size()-1];

}


template <class Tr, class Th, class P> P AlignDTW<Tr,Th, P>::CalculerCheminDTW(vector<Th> &Hyp, int OriJ, int OriI)
{
	unsigned int i, j;
	P Cout;

	if (OriI < 0) OriI = 0;
	if (OriJ < 0) OriJ = 0;

	MatriceDTW[0][0] = CalculerDistance((*Reference)[0], Hyp[0]);
	Maxis[0] = 0;
	//P Delt = Del;

	//cout <<"ref size : "<<(*Reference).size()<<endl;

	P Max;
	P Mul;
	P CoutFinal;
	unsigned int RefSize = (*Reference).size();


	for (i = OriI; i < Hyp.size(); i++)
	{
		Max = -INFINI;

		if (FastCut == true && i > 0)
		{
			OriJ = Maxis[i-1]-WindowCut;
			if (OriJ < 0) OriJ = 0;
			RefSize =  Maxis[i-1]+WindowCut;
		}
		else if (FastCut == true && i == 0)
		{
			OriJ=0;
			RefSize = WindowCut;
		}

		if (RefSize > (*Reference).size()) 
			RefSize = (*Reference).size();



		//if (i > 0)
		//	cout <<"refsize : "<<RefSize<<" maxis["<<i<<"] : "<<Maxis[i-1]<<endl;


		MaxTailleRef[i] = RefSize; 
		MinTailleRef[i] = OriJ;

		for (j = (unsigned int)OriJ; j < RefSize; j++)
		{
			Cout = CalculerDistance((*Reference)[j], Hyp[i]);

			//if (Cout <= 0) Mul = 1;
			//else Mul = 0;

			if (Cout <= 0) CoutFinal = Sub;
			else CoutFinal = -Cout;


			if (i > 0)
			{
				if ((int)j > OriJ)
				{
					if ((int)j < MaxTailleRef[i-1] && (int)j > MinTailleRef[i-1])
					{
						MatriceDTW[i][j] = MaxDTW(MatriceDTW[i-1][j] - Ins, MatriceDTW[i][j-1] - Del, MatriceDTW[i-1][j-1] - CoutFinal);
					}
					else MatriceDTW[i][j] = MaxDTW(-INFINI, MatriceDTW[i][j-1] - Del /**Mul*/, -INFINI);
				}
				else 
				{
					if ((int)j >= MinTailleRef[i-1])
						MatriceDTW[i][j] = MaxDTW(MatriceDTW[i-1][j] - Ins /**Mul*/, -INFINI, -INFINI);
					else MatriceDTW[i][j] = -INFINI;
				}

			}
			else if ((int) j > OriJ) MatriceDTW[i][j] = MaxDTW(-INFINI, MatriceDTW[i][j-1] - Del/**Mul*/, -INFINI);
			else MatriceDTW[i][j] = Cout;

			//if (MatriceDTW[i][j] < -INFINI) MatriceDTW[i][j] = -INFINI;

			/*
			   if (i > OriI && j > OriJ && j < MaxTailleRef[i-1]) MatriceDTW[i][j] = Cout + MaxDTW(MatriceDTW[i-1][j] - Ins, MatriceDTW[i][j-1] - Del, MatriceDTW[i-1][j-1] - Sub*Mul);
			   else if (i > OriI && j > OriJ) 
			   {
			   if(j < MaxTailleRef[i-1]) MatriceDTW[i][j] = Cout + MaxDTW(MatriceDTW[i-1][j] - Ins*Mul, -INFINI, -INFINI);
			   else MatriceDTW[i][j] = Cout + MaxDTW(-INFINI, MatriceDTW[i][j-1] - Del*Mul, -INFINI);
			   }
			   else if (j > OriJ) MatriceDTW[i][j] = Cout + MaxDTW(-INFINI, MatriceDTW[i][j-1] - Del*Mul, -INFINI);
			   else MatriceDTW[i][j] = Cout;
			   */
			//if (MatriceDTW[i][j] < -900000) MatriceDTW[i][j] = -INFINI;

			if (MatriceDTW[i][j] > Max) 
			{
				Max = MatriceDTW[i][j];
				Maxis[i] = j;
			}

		}
	}
	//cout <<"here25"<<endl;	
	return MatriceDTW[Hyp.size()-1][(*Reference).size()-1];
}

