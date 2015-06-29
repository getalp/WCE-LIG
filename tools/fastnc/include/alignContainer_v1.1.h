/*
 * =====================================================================================
 * 
 *       Filename:  alignContainer.h
 * 
 *    Description:  generic DTW and SwithWaterman implementations 
 * 
 *        Version:  1.1
 *        Created:  05/03/07 10:41:03 CEST
 *       Revision:  none
 *       Compiler:  g++
 * 
 *         Author:  LECOUTEUX Benjamin 
 *        Company:  LIA
 * 
 * =====================================================================================
 */



#include <deque>
#include <vector>
#include <iostream>

using namespace std;

template <class Tr, class Th, class P> class AlignDTW
{
	protected:
		P Sub;
		P Ins;
		P Del;
	
		int NbCommunsPrecedent;
		
		P **MatriceDTW;
		P (*CalculerDistance)(Tr Ref, Th Hyp);
		void (*PrintRefOrHyp)(Tr Ref, Th Hyp);
		static P DistanceDefaut(Tr Ref, Th Hyp);
		static void PrintDefaultRefOrHyp(Tr Ref, Th Hyp);
		P MaxDTW(P a, P b, P c);

		int TailleMaxRef;
		int TailleMaxHyp;
	
		vector<int> SubInsDel;
		vector<int> RefVec;
		vector<int> HypVec;


		int *BacktraceRef;
		int *BacktraceHyp;
		
	public:
		Tr *IsAligned(int HypNum, vector<Tr> &Ref);
	

		void PrintBestAlign(vector<Tr> &Ref, vector<Th> &Hyp);
		
		AlignDTW(int TailleMaxRef, int TailleMaxHyp, P (*DistFunction)(Tr a, Th b)=NULL,void (*PrintRefOrHyp)(Tr Ref, Th Hyp)=NULL ,P Sub=1, P Ins=1, P Del=1);
		void InitDTW(P FillBorder=0.0, P Fill=0.0, P Init=0.0);
		P CalculerCheminDTW(vector<Tr> &Ref, vector<Th> &Hyp, int OriI = 0, int OriJ = 0);
		void BackTrack(vector<Tr> &Ref, vector<Th> &Hyp, int OriRef=0, int OriHyp=0);
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
		deque<P> Maximums;
		deque<int> MaxRef;
		deque<int> MaxHyp;
	
		int NbMaximums;

	public:
		
		SmithWatermanDTW(int TailleMaxRef, int TailleMaxHyp, int NbMax, P (*DistFunction)(Tr a, Th b)=NULL, void (*PrintRefOrHyp)(Tr Ref, Th Hyp)=NULL , P Sub=1, P Ins=1, P Del=1);
		void InitDTW(P FillBorder=0.0, P Fill=0.0, P Init=0.0);
		~SmithWatermanDTW();
		P CalculerCheminDTW(vector<Tr> &Ref, vector<Th> &Hyp, int OriI = 0, int OriJ = 0);
		void BackTrack(vector<Tr> &Ref, vector<Th> &Hyp);

};


template <class Tr, class Th, class P> P SmithWatermanDTW<Tr, Th, P>::MaxDTW(P a, P b, P c, P d)
{
	if (a >= b && a >= c && a >= d) return a;
	if (b >= a && b >= c && b >= d) return b;
	if (c >= a && c >= b && c >= d) return c;
	return d;
}



template <class Tr, class Th, class P> AlignDTW<Tr,Th,P>::AlignDTW(int TailleMaxRef, int TailleMaxHyp, P (*DistFunction)(Tr a, Th b),void (*PrintRefOrHyp)(Tr Ref, Th Hyp) , P Sub, P Ins, P Del)
{
	int i, Max;

	MatriceDTW = new P*[TailleMaxHyp];
	
	for (i = 0; i < TailleMaxHyp; i++)
		MatriceDTW[i] = new P[TailleMaxRef];	
	
	BacktraceRef = new int[TailleMaxRef];
	BacktraceHyp = new int[TailleMaxHyp];
	
	if (TailleMaxRef > TailleMaxHyp) Max = TailleMaxRef;
	else Max = TailleMaxHyp;

	//BacktraceAlg = new int[Max];

	this->TailleMaxRef = TailleMaxRef;
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

	delete [] BacktraceRef;
	delete [] BacktraceHyp;
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


template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::PrintDefaultRefOrHyp(Tr Ref, Th Hyp)
{
	if (Ref) cout << Ref<<"\t";
	else cout <<"-\t";

	if (Hyp) cout << Hyp<<"\t";
	else cout <<"-\t";
}

template <class Tr, class Th, class P> P AlignDTW<Tr,Th,P>::DistanceDefaut(Tr a, Th b)
{
	if (a == (Tr)b) return 0;
	else return 1;
}



template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::InitDTW(P FillBorder, P Fill, P Init)
{
	int i, j;

	for (i = 0; i < TailleMaxRef; i++)
		MatriceDTW[0][i] = FillBorder;

	for (i = 0; i < TailleMaxHyp; i++)
		MatriceDTW[i][0] = FillBorder;

	for (i = 1; i < TailleMaxHyp; i++)
		for (j = 1; j < TailleMaxRef; j++)
			MatriceDTW[i][j] = Fill;

	MatriceDTW[0][0] = Init;
}


template <class Tr, class Th, class P> void SmithWatermanDTW<Tr,Th, P>::BackTrack(vector<Tr> &Ref, vector<Th> &Hyp)
{
	int BestHyp = MaxHyp.front();
	int BestRef = MaxRef.front();

	AlignDTW<Tr,Th,P>::BackTrack(Ref, Hyp, BestRef, BestHyp);
}


template <class Tr, class Th, class P> Tr *AlignDTW<Tr,Th,P>::IsAligned(int HypNum, vector<Tr> &Ref)
{
	Tr *Return;

	if (BacktraceHyp[HypNum] >= 0)
		return &Ref[BacktraceHyp[HypNum]];
	return NULL;
}


template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::PrintBestAlign(vector<Tr> &Ref, vector<Th> &Hyp)
{
	int tmp1, tmp2, tmp3;

	//cout <<endl<<endl;

	//cout <<"--->"<<endl;


	cout <<"alignment : "<<endl<<endl;
	cout <<"state\tRef\tHyp"<<endl;

	while (AlignDTW<Tr,Th,P>::SubInsDel.size())
	{
		tmp1 = AlignDTW<Tr,Th,P>::SubInsDel.back();
		AlignDTW<Tr,Th,P>::SubInsDel.pop_back();
		if (tmp1 == 0)	cout <<"ok\t";
		else if (tmp1 == 1) cout <<"ins\t";
		else if (tmp1 == 2) cout <<"del\t";
		else cout <<"sub\t";

		tmp2 = AlignDTW<Tr,Th,P>::RefVec.back();
		AlignDTW<Tr,Th,P>::RefVec.pop_back();
		
		tmp3 = AlignDTW<Tr,Th,P>::HypVec.back();
		AlignDTW<Tr,Th,P>::HypVec.pop_back();

		if (tmp2 >= 0 && tmp3 >=0) PrintRefOrHyp(Ref[tmp2], Hyp[tmp3]);
		else if (tmp2 >= 0) PrintRefOrHyp(Ref[tmp2], NULL);
		else if (tmp3 >= 0) PrintRefOrHyp(NULL, Hyp[tmp3]);
		else PrintRefOrHyp(NULL, NULL);
		cout <<endl;
	}
	/*
	while (AlignDTW<Tr,Th,P>::RefVec.size())
	{
		tmp = AlignDTW<Tr,Th,P>::RefVec.back();
		AlignDTW<Tr,Th,P>::RefVec.pop_back();
		//if (tmp >= 0)	cout <<Ref[tmp]<<"\t";
		if (tmp >= 0) PrintRefOrHyp(Ref[tmp], NULL), cout <<"\t";
		else cout <<"-\t";
	}
	cout << endl;

	while (AlignDTW<Tr,Th,P>::HypVec.size())
	{
		tmp = AlignDTW<Tr,Th,P>::HypVec.back();
		AlignDTW<Tr,Th,P>::HypVec.pop_back();
		//if (tmp >= 0)	cout <<Hyp[tmp]<<"\t";
		if (tmp >= 0) PrintRefOrHyp(NULL, Hyp[tmp]), cout <<"\t";
		else cout <<"-\t";
	}
	cout << endl;
	*/
}

template <class Tr, class Th, class P> void AlignDTW<Tr,Th,P>::BackTrack(vector<Tr> &Ref, vector<Th> &Hyp, int OriRef, int OriHyp)
{
	P Score;
	P Diag;
	P Left;
	P Up;

	int i,j;

	if (OriHyp) i = OriHyp;
	else	i = Hyp.size()-1;

	if (OriRef) j = OriRef;
	else j = Ref.size()-1;

	RefVec.clear();
	HypVec.clear();
	SubInsDel.clear();

	//cout <<"alignement :"<<i<<", "<<j<<endl;

	while (i > 0 && j > 0)
	{
		Score = MatriceDTW[i][j];
		Diag = MatriceDTW[i-1][j-1];
		Left = MatriceDTW[i-1][j];
		Up = MatriceDTW[i][j-1];

		Diag = Score;

		//if (Diag == Left == Up == 0.0) break; 

		if (Diag >= Up && Diag >= Left)
		{
			RefVec.push_back(j);
			HypVec.push_back(i);

			//cout <<Ref[j]<<"\t"<<Hyp[i];
			
			if (CalculerDistance(Ref[j], Hyp[i]) < 0) 
			{
				SubInsDel.push_back(3);
				//cout <<"\tsub";
			
				BacktraceRef[j] = BacktraceHyp[i] = -3;
			}
			else
			{
				SubInsDel.push_back(0);
				BacktraceRef[j] = i;
				BacktraceHyp[i] = j;
			}

			//cout <<endl;
			
			i--, j--;
		}
		else if (Up >= Diag && Up >= Left)
		{
			SubInsDel.push_back(2);
			RefVec.push_back(j);
			HypVec.push_back(-1);

			//cout <<Ref[j]<<"\t-\t"<<"del"<<endl;
			BacktraceRef[j] = -2;
			BacktraceHyp[i] = -1;
			j--;
		}
		else 
		{
			SubInsDel.push_back(1);
			RefVec.push_back(-1);
			HypVec.push_back(i);

			//cout <<"-"<<"\t"<<Hyp[i]<<"\tins"<<endl;
			BacktraceRef[j] = -1;
			BacktraceHyp[i] = -2;
			i--;
		}
	}
/*	
	while (i > 0)
	{
		Score = MatriceDTW[i][j];
		Left = MatriceDTW[i-1][j];

		Diag = Score;

		//if (Diag == Left == Up == 0.0) break; 

		if (Diag >= Left)
		{
			RefVec.push_back(j);
			HypVec.push_back(i);

			//cout <<Ref[j]<<"\t"<<Hyp[i];

			if (CalculerDistance(Ref[j], Hyp[i]) < 0) 
			{
				SubInsDel.push_back(3);
				//cout <<"\tsub";

				BacktraceRef[j] = BacktraceHyp[i] = -3;
			}
			else
			{
				SubInsDel.push_back(0);
				BacktraceRef[j] = i;
				BacktraceHyp[i] = j;
			}

			//cout <<endl;

			i--;
		}
		else 
		{
			SubInsDel.push_back(1);
			RefVec.push_back(-1);
			HypVec.push_back(i);

			//cout <<"-"<<"\t"<<Hyp[i]<<"\tins"<<endl;
			BacktraceRef[j] = -1;
			BacktraceHyp[i] = -2;
			i--;
		}
	}
	*/
	/*
	while (j > 0)
	{
		Score = MatriceDTW[i][j];
		Up = MatriceDTW[i][j-1];

		Diag = Score;

		//if (Diag == Left == Up == 0.0) break; 

		if (Diag >= Up)
		{
			RefVec.push_back(j);
			HypVec.push_back(i);

			//cout <<Ref[j]<<"\t"<<Hyp[i];
			
			if (CalculerDistance(Ref[j], Hyp[i]) < 0) 
			{
				SubInsDel.push_back(3);
				//cout <<"\tsub";
			
				BacktraceRef[j] = BacktraceHyp[i] = -3;
			}
			else
			{
				SubInsDel.push_back(0);
				BacktraceRef[j] = i;
				BacktraceHyp[i] = j;
			}

			//cout <<endl;
			
			j--;
		}
		else if (Up >= Diag)
		{
			SubInsDel.push_back(2);
			RefVec.push_back(j);
			HypVec.push_back(-1);

			//cout <<Ref[j]<<"\t-\t"<<"del"<<endl;
			BacktraceRef[j] = -2;
			BacktraceHyp[i] = -1;
			j--;
		}
	}*/


	//if (i == 0 && j == 0)
	{
		if (CalculerDistance(Ref[j], Hyp[i]) > 0)
		{
			SubInsDel.push_back(0);
			BacktraceRef[j] = i;
			BacktraceHyp[i] = j;
		}
		else
		{
			SubInsDel.push_back(3);
			BacktraceRef[j] = BacktraceHyp[i] = -3;
		}
		RefVec.push_back(j);
		HypVec.push_back(i);


		//cout <<Ref[j]<<"\t"<<Hyp[i]<<endl;
	}


}


template <class Tr, class Th, class P> SmithWatermanDTW<Tr,Th,P>::SmithWatermanDTW(int TailleMaxRef, int TailleMaxHyp, int NbMax,  P (*DistFunction)(Tr a, Th b), void (*PrintRefOrHyp)(Tr a, Th b), P Sub, P Ins, P Del):AlignDTW<Tr,Th,P>(TailleMaxRef, TailleMaxHyp, DistFunction, PrintRefOrHyp ,Sub, Ins, Del)
{
	int i;

	NbMaximums = NbMax;

	MaxI = new P[TailleMaxRef];
	MaxJ = new P[TailleMaxHyp];

	IdMaxI = new int[TailleMaxRef];
	IdMaxJ = new int[TailleMaxHyp];

	SvgMatrice = new struct SVG_SWDTW*[TailleMaxHyp];

	for (i = 0; i < TailleMaxHyp; i++)
		SvgMatrice[i] = new struct SVG_SWDTW[TailleMaxRef];
}


template <class Tr, class Th, class P> SmithWatermanDTW<Tr,Th,P>::~SmithWatermanDTW()
{
	delete [] MaxI;
	delete [] MaxJ;

	delete [] IdMaxI;
	delete [] IdMaxJ;
}


template <class Tr, class Th, class P> void SmithWatermanDTW<Tr,Th,P>::InitDTW(P FillBorder, P Fill, P Init)
{
	int i;

	AlignDTW<Tr,Th,P>::InitDTW(FillBorder, Fill, Init);

	for (i = 0; i < AlignDTW<Tr,Th,P>::TailleMaxRef; i++)
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


template <class Tr, class Th, class P> P SmithWatermanDTW<Tr,Th,P>::CalculerCheminDTW(vector<Tr> &Ref, vector<Th> &Hyp, int OriI, int OriJ)
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
		for (j = OriJ; j < Ref.size(); j++) MaxI[j] = 0;

		Maximums.clear();
		Maximums.push_front(TheMax);
		MaxRef.clear();
		MaxHyp.clear();
		MaxRef.push_front(Y);
		MaxHyp.push_front(X);
	}


	for (i = 0; i < Hyp.size(); i++)
	{
		for (j = 0; j < Ref.size(); j++)
		{
			if (i >= OriI || j >= OriJ)
			{
				Cout = CalculerDistance(Ref[j], Hyp[i]);

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

				if (Maximums.size() > 0)
				{
					if (AlignDTW<Tr,Th,P>::MatriceDTW[i][j] >= Maximums.front())
					{
						Maximums.push_front(AlignDTW<Tr,Th,P>::MatriceDTW[i][j]);
						MaxHyp.push_front(i);
						MaxRef.push_front(j);

						if (Maximums.size() > NbMaximums) Maximums.pop_back();
						if (MaxHyp.size() > NbMaximums) MaxHyp.pop_back();
						if (MaxRef.size() > NbMaximums) MaxRef.pop_back();
					}
				}
				else
				{	
					Maximums.push_front(AlignDTW<Tr,Th,P>::MatriceDTW[i][j]);
					MaxHyp.push_front(i);
					MaxRef.push_front(j);
				}
			}
		}
	}		

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
	return AlignDTW<Tr,Th,P>::MatriceDTW[Hyp.size()-1][Ref.size()-1];

}


template <class Tr, class Th, class P> P AlignDTW<Tr,Th, P>::CalculerCheminDTW(vector<Tr> &Ref, vector<Th> &Hyp, int OriI, int OriJ)
{
	int i, j;
	P Cout;
	//P Delt = Del;

	for (i = OriI; i < Hyp.size(); i++)
	{
		for (j = OriJ; j < Ref.size(); j++)
		{
			Cout = CalculerDistance(Ref[j], Hyp[i]);

			/*
			   if (i > 0 && j > 0) MatriceDTW[i][j] = Cout + MaxDTW(MatriceDTW[i-1][j], MatriceDTW[i][j-1]-Cout, MatriceDTW[i-1][j-1]);
			   else if (i > 0) MatriceDTW[i][j] = Cout + MaxDTW(MatriceDTW[i-1][j], -100, -100);
			   else if (j > 0) MatriceDTW[i][j] = Cout + MaxDTW(-100, MatriceDTW[i][j-1], -100);
			   */

			if (i > 0 && j > 0) MatriceDTW[i][j] = Cout + MaxDTW(MatriceDTW[i-1][j] -  Ins, MatriceDTW[i][j-1] - Del, MatriceDTW[i-1][j-1] + Sub * Cout);
			else if (i > 0) MatriceDTW[i][j] = MaxDTW(MatriceDTW[i-1][j] - Ins, 0, 0);
			else if (j > 0) MatriceDTW[i][j] = MaxDTW(0, MatriceDTW[i][j-1] - Del, 0);
		}
	}				
	return MatriceDTW[Hyp.size()-1][Ref.size()-1];
}

