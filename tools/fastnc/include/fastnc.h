/*
 * =====================================================================================
 * 
 *       Filename:  fastnc.h
 * 
 *    Description:  
 * 
 *        Version:  0.2
 *        Created:  07.12.2007 23:01:19 CET
 *       Revision:  none
 *       Compiler:  g++
 * 
 *         Author:  Benjamin Lecouteux 
 *        Company:  LIA
 * 
 * =====================================================================================
 */

#include <math.h>
#include <vector>
#include <set>
#include <map>
#include <iostream>
#include <string.h>
#include <strings.h>
#include <unistd.h>
#include "readlm.h"

using namespace std;
uint64_t ComptLink=0;


struct ltstr
{
	bool operator()(const char* s1, const char* s2) const
	{
		return strcmp(s1, s2) < 0;
	}
};


#define INFINI 2000000000
//#define PRECISION 0.0001
#define PRECISION 0.01 //BEST
//#define PRECISION 0.1


map<char *, int, ltstr> WordsID;
//#define PRECISION 0.000001
/*

int flt_cmp(float x, float y)
{
	float a, b;
	int ret;
	float eps_a = 0.0000000001;
	float eps_r = 0.0000000001;

	if (x < y)
	{
		a = x;
		b = y;
		ret = -1;
	}
	else if (x > y)
	{
		a = y;
		b = x;
		ret = 1;
	}
	else
		ret = 0;


	if (ret != 0)
	{

		if (b - a < eps_a)
		{
			ret = 0;
		}

		if (ret != 0)
		{

			if ((b - a) / a < eps_r)
				ret = 0;
		}
	}

	return ret;
}
*/





inline bool Egalite(float a, float b)
{
	if (fabs(a-b) < PRECISION) return true;
	return false;
	//return flt_cmp(a,b) == 0;
}

inline bool PlusPetit(float a, float b)
{
	if (!Egalite(a,b)  && a < b) return true;
	else return false;
	//return flt_cmp(a,b) < 0;
}


struct CLONE_HASH
{
	vector<int> *History;
	int UsedContext;	
	int NextWordId;
	float NextLmProb;
	float NextAcProb;
	float AcProbability;
	class NODE *Target;
	//class NODE *Next;
	class NODE *CloneTarget;
	class NODE *From;
};


struct TIMELINK
{
	float Start;
	float End;
	float Duration;
};


class LINK
{
	public:
		uint64_t id;
		static int NbLink;
		static float MLFudge;
		static float Penalty;
		static float PScaling;
		static float AcFudge;
		static float MaxId;

		LINK(class NODE *From, class NODE *Target, float Post, int Word, float LMProb=0, float AcProb=0, bool Fake=false);
		~LINK();
		void merge(LINK *L);
		bool operator == (LINK &L);
		struct NCNODE *NCBack;
		struct NCNODE *NCNext;
		class NODE *Target;
		class NODE *From;
		float Posterior;
		float Weight(bool Scaling=false);
		vector<TIMELINK *> TimeLinks; 

		//bool IsTheSame (LINK *, float LmProb);	
		void NotFake();
		float LmProbability;
		float AcProbability;
		int ContextToUse;
		int WordId;
};

float LINK::Weight(bool Scaling)

{
	if (WordId == WordsID[(char *)"*DELETE*"]) return -1000;
	if (WordId > MaxId && AcProbability == 0) return 0;
	
	if (LmProbability == 0 && AcProbability == 0) return 0;
	
	if (WordId > MaxId && AcProbability) 
	{
		if (Scaling) return (AcProbability * AcFudge)/PScaling;
		return AcProbability * AcFudge;
	}

	/*if (AcProbability == 0)
	  {
	  if (Scaling)
	  return (LmProbability * MLFudge)/PScaling;
	  else
	  return (LmProbability * MLFudge);

	  }*/

	if (Scaling)
		return (LmProbability * MLFudge + Penalty + AcProbability /** AcFudge*/)/PScaling;
	else
		return ((LmProbability * MLFudge) + Penalty + AcProbability /** AcFudge*/);
}

int LINK::NbLink=0;
float LINK::MaxId=86000;
float LINK::MLFudge=10;
float LINK::AcFudge=1.0;
float LINK::Penalty=-12.0;
float LINK::PScaling=10.0;

/*

   struct CLONE_HASH
   {
   int NextWordId;

   vector<int> History;
   float NextLmProb;
   class NODE *CloneTarget;
   };*/


struct TO_SEARCH
{
	NODE *Target;
	bool Histo;
	bool Word;
};



class comp_search
{
	public:
		bool operator()(struct TO_SEARCH* a, struct TO_SEARCH* b) { 	

			return a < b;
		}
};







class CloneCompare_Word
{
	public:
		bool operator()(CLONE_HASH* a, CLONE_HASH* b) { 	

			bool result = false;

			if (a->NextWordId < b->NextWordId) result = true;
			else if (a->NextWordId == b->NextWordId && PlusPetit(a->NextLmProb, b->NextLmProb)) result = true;
			//else if (a->NextWordId == b->NextWordId && Egalite(a->NextLmProb, b->NextLmProb) && PlusPetit(a->NextAcProb, b->NextAcProb)) result = true;

			return result; }
};


class CloneCompare_All
{
	public:
		bool operator()(CLONE_HASH* a, CLONE_HASH* b) { 	

			int Ha[MAX_GRAM*2];
			int Hb[MAX_GRAM*2];

			memset(Ha, 0, sizeof(int)*MAX_GRAM*2);	
			memset(Hb, 0, sizeof(int)*MAX_GRAM*2);	

			for (int i = 0; i < a->History->size(); i++)
				Ha[i] = (*(a->History))[i];

			for (int i = 0; i < b->History->size(); i++)
				Hb[i] = (*(b->History))[i];

			int cmp = memcmp(Ha, Hb, MAX_GRAM*sizeof(int)*2);

			if (cmp < 0) return true;
			if (cmp == 0 && a->Target < b->Target) return true;
			return false;	
		}
};





class CloneCompare_History2
{
	public:
		bool operator()(CLONE_HASH* a, CLONE_HASH* b) { 	

			int Ha[MAX_GRAM*2];
			int Hb[MAX_GRAM*2];

			memset(Ha, 0, sizeof(int)*MAX_GRAM*2);	
			memset(Hb, 0, sizeof(int)*MAX_GRAM*2);	

			for (int i = 0; i < a->History->size(); i++)
				Ha[i] = (*(a->History))[i];

			for (int i = 0; i < b->History->size(); i++)
				Hb[i] = (*(b->History))[i];

			int cmp = memcmp(Ha, Hb, MAX_GRAM*sizeof(int)*2);

			if (cmp < 0) return true;
			if (cmp == 0 && a->Target < b->Target) return true;
			return false;	
		}
};




class CloneCompare_History
{
	public:
		bool operator()(CLONE_HASH* a, CLONE_HASH* b) { 	

			int Ha[MAX_GRAM*2];
			int Hb[MAX_GRAM*2];

			memset(Ha, 0, sizeof(int)*MAX_GRAM*2);	
			memset(Hb, 0, sizeof(int)*MAX_GRAM*2);	

			for (int i = 0; i < a->History->size(); i++)
				Ha[i] = (*(a->History))[i];

			for (int i = 0; i < b->History->size(); i++)
				Hb[i] = (*(b->History))[i];

			//if (memcmp(Ha, Hb, MAX_GRAM*sizeof(int)*2) < 0) return true;
			//if (memcmp(Ha, Hb, MAX_GRAM*sizeof(int)*2) == 0 && a->UsedContext < b->UsedContext) return true;
			//return false;
			return (memcmp(Ha, Hb, MAX_GRAM*sizeof(int)*2) < 0);	
		}
};

class CONNECT
{
	public:
		CONNECT(NODE *n1, NODE *n2, int word=0, float ac=0)
		{
			if (n1 > n2) 	a = n1, b = n2;
			else		a = n2, b = n1;	

			this->word=word;
			this->ac = ac;
		}
		int word;
		float ac;
		NODE *a;
		NODE *b;
};




class CompareConnects
{
	public:
		bool operator()(class CONNECT* a, class CONNECT* b) { 	

			NODE *Na[2];
			NODE *Nb[2];
			Na[0] = a->a, Na[1] = a->b;
			Nb[0] = b->a, Nb[1] = b->b;
			int cmp;
			//return  memcmp (Na, Nb, sizeof(NODE *)*2) < 0;
			if (memcmp (Na, Nb, sizeof(NODE *)*2) == 0) return a->word < b->word;
			else return memcmp (Na, Nb, sizeof(NODE *)*2) < 0;
		}
};





class LinkCompare
{
	public:
		bool operator()(const class  LINK* a, class   LINK* b) { 	

			//bool result = false;

			return a->id < b->id;
			//if (a->WordId < b->WordId) result = true;
			//if (a->WordId == b->WordId && PlusPetit(a->LmProbability, b->LmProbability) /*a->LmProbability < b->LmProbability*/) result = true;

			//if (OriginalFind == true)
			//{
			//	if (a->WordId == b->WordId && Egalite(a->LmProbability, b->LmProbability) && PlusPetit(a->AcProbability, b->AcProbability)) result = true;
			//	if (a->WordId == b->WordId && Egalite(a->LmProbability, b->LmProbability) && Egalite(a->AcProbability, b->AcProbability)  &&  a->Target < b->Target) result = true;
			//	if (a->WordId == b->WordId && Egalite(a->LmProbability, b->LmProbability) && Egalite(a->AcProbability, b->AcProbability)  &&  a->Target ==  b->Target && a < b) result = true;
			//if (a->WordId == b->WordId && a->Target < b->Target) result = true;
			//if (a->WordId == b->WordId && a->Target == b->Target && a < b) result = true;
			//}
			//else
			//{
			//	if (a->WordId == b->WordId && a->LmProbability == b->LmProbability && a->AcProbability < b->AcProbability) result = true;
			//	if (a->WordId == b->WordId && a->LmProbability == b->LmProbability && a->AcProbability == b->AcProbability  &&  a->Target < b->Target) result = true;
			//	if (a->WordId == b->WordId && a->LmProbability == b->LmProbability && a->AcProbability == b->AcProbability  &&  a->Target == b->Target && a < b)  result = true;

			//}

			//return result; 
		}
};

bool operator<(const class Ngram &n1, const class Ngram &n2)
{
	return true;
}

class NODE
{
	public:
		NODE(float T, float P=1, int N=0);
		~NODE();
		void merge(NODE *N, bool back=true, bool Next=true);
		void merge2(NODE *N, LINK *);

		float Viterbi;
		int MyCluster;
		int ContextToUse;
		int Number;
		int WordId;
		float Time;
		float Posterior;
		float Forward;
		float Backward;
		bool HasNull;
		NODE *CloneDup(bool CloneLinks, bool Before = true, bool After = true);

		NODE *Clone(bool CloneLinks);
		vector <NODE *> Clones;
		set<struct LINK *, LinkCompare> BackLinks;
		set<struct LINK *, LinkCompare > NextLinks;
		NODE *SearchCloneInContext(LINK *Before, LINK *After, ReadLM *LM, float LmProb, int Order, int ContextSize, set<CLONE_HASH *, CloneCompare_Word> &CloneHashWord, set<CLONE_HASH *, CloneCompare_History> &CloneHashHistory, CLONE_HASH *&CloneToAdd, vector<int> *Seq, vector<int> *Seq2);
		//		NODE *SearchCloneInContext(LINK *Before, LINK *After, ReadLM *LM, float LmProb, int ContextSize, set<CLONE_HASH *, CloneCompare_Word> &CloneHashWord, set<CLONE_HASH *, CloneCompare_History> &CloneHashHistory, CLONE_HASH *&CloneToAdd);
};


NODE::~NODE()
{
	BackLinks.clear();
	NextLinks.clear();
	Clones.clear();
};


NODE *NODE::CloneDup(bool CloneLinks, bool Before, bool After)
{
	NODE *Clone=new NODE(Time);

	Clone->MyCluster=MyCluster;
	Clone->Number=Number;
	Clone->Time=Time;
	Clone->WordId=WordId;

	if (CloneLinks == true)
	{
		set<struct LINK *, LinkCompare>::iterator it;

		if (Before)
			for (it = BackLinks.begin(); it != BackLinks.end(); it++) new LINK((*it)->From, Clone, (*it)->Posterior, (*it)->WordId ,  (*it)->LmProbability,  (*it)->AcProbability);

		if (After)
			for (it = NextLinks.begin(); it != NextLinks.end(); it++) new LINK(Clone, (*it)->Target, (*it)->Posterior, (*it)->WordId ,  (*it)->LmProbability,  (*it)->AcProbability);
	}

	return Clone;
}

NODE *NODE::Clone(bool CloneLinks)
{
	NODE *Clone=new NODE(Time);

	Clone->MyCluster=MyCluster;
	Clone->Number=Number;
	Clone->Time=Time;

	if (CloneLinks == true)
	{
		set<struct LINK *, LinkCompare>::iterator it;

		for (it = BackLinks.begin(); it != BackLinks.end(); it++) new LINK((*it)->From, Clone, (*it)->Posterior, (*it)->WordId ,  (*it)->LmProbability,  (*it)->AcProbability);
		for (it = NextLinks.begin(); it != NextLinks.end(); it++) new LINK(Clone, (*it)->Target, (*it)->Posterior, (*it)->WordId ,  (*it)->LmProbability,  (*it)->AcProbability);
	}

	Clones.push_back(Clone);

	return Clone;
}



class Ngram
{
	private:
		vector<int> Gram;
		NODE *Target;

	public:
		void PushTarget(NODE *T)
		{
			Target = T;
		}

		void push(int n)
		{
			Gram.push_back(n);
		}

		NODE *GetNode()const
		{
			return Target;
		}

		bool operator < (const Ngram &n1)
		{
			return true;
		}

		friend bool operator<(const Ngram &n1, const Ngram &n2);


};
/*


void NODE::merge2(NODE *N, LINK *LinkToMerge)
{
	set<struct LINK *, LinkCompare>::iterator it;

	for (it = N->NextLinks.begin(); it != N->NextLinks.end(); it++)
		(*it)->From = this;
	for (it = N->BackLinks.begin(); it != N->BackLinks.end(); it++)
		(*it)->Target = this;
	
	BackLinks.insert(N->BackLinks.begin(), N->BackLinks.end());
	
	NextLinks.insert(N->NextLinks.begin(), N->NextLinks.end());


	}*/


void NODE::merge2(NODE *N, LINK *ToRemove)
{
	set<struct LINK *, LinkCompare>::iterator it;


	for (it = N->NextLinks.begin(); it != N->NextLinks.end(); it++)
		(*it)->From = this;

	for (it = N->BackLinks.begin(); it != N->BackLinks.end(); it++)
		(*it)->Target = this;

	BackLinks.insert(N->BackLinks.begin(), N->BackLinks.end());
	NextLinks.insert(N->NextLinks.begin(), N->NextLinks.end());

	BackLinks.erase(ToRemove);
	NextLinks.erase(ToRemove);
	ToRemove->Target->BackLinks.erase(ToRemove);
	ToRemove->From->NextLinks.erase(ToRemove);

	delete ToRemove;
	delete N;
}



void NODE::merge(NODE *N, bool back, bool next)
{
	set<struct LINK *, LinkCompare>::iterator it;

	if (next)
		for (it = N->NextLinks.begin(); it != N->NextLinks.end(); it++)
			(*it)->From = this;

	if (back)
		for (it = N->BackLinks.begin(); it != N->BackLinks.end(); it++)
			(*it)->Target = this;
	if (back)
		BackLinks.insert(N->BackLinks.begin(), N->BackLinks.end());
	if (next)
		NextLinks.insert(N->NextLinks.begin(), N->NextLinks.end());
}


void LINK::NotFake()
{
	struct TIMELINK *Tlink;
	Tlink = new struct TIMELINK;
	Tlink->Start = From->Time;
	Tlink->End = Target->Time;
	Tlink->Duration = Tlink->End-Tlink->Start;
	if (Tlink->Duration < 0 ) Tlink->Duration = -Tlink->Duration;
	TimeLinks.push_back(Tlink);

	From->NextLinks.insert(this);
	Target->BackLinks.insert(this);

}

LINK::LINK(class NODE *From, class NODE *Target, float Post, int Word, float LmProb, float AcProb, bool Fake)
{
	struct TIMELINK *Tlink;

	LmProbability = LmProb;
	AcProbability = AcProb;
	if (Fake == false) 
	{
		Tlink = new struct TIMELINK;
		Tlink->Start = From->Time;
		Tlink->End = Target->Time;
		Tlink->Duration = Tlink->End-Tlink->Start;
		if (Tlink->Duration < 0 ) Tlink->Duration = -Tlink->Duration;
		TimeLinks.push_back(Tlink);
	}
	id=ComptLink++;
	NbLink++;	
	this->From = From;
	this->Target = Target;
	this->Posterior = Post;
	this->WordId = Word;
	if (Fake == false)
	{
		//cerr <<"from"<<endl;
		From->NextLinks.insert(this);
		//cerr <<"target"<<endl;
		Target->BackLinks.insert(this);
		//cerr <<"ok"<<endl;
	}
}

void LINK::merge(LINK *L)
{
	Posterior+=L->Posterior;

	TimeLinks.insert(TimeLinks.end(), L->TimeLinks.begin(), L->TimeLinks.end());

	set<LINK *, LinkCompare>::iterator it;

	it = L->Target->BackLinks.find(L);
	if (it != L->Target->BackLinks.end())
		L->Target->BackLinks.erase(it);
}
/*
   bool LINK::operator==(LINK &L)
   {
   if (NCBack == L.NCBack && NCNext == L.NCNext && WordId == L.WordId) return true;
   return false;
   }*/

LINK::~LINK()
{
	NbLink--;

	/*set<LINK *, LinkCompare>::iterator it;

	  it = Target->BackLinks.find(this);
	  if (it != Target->BackLinks.end()) Target->BackLinks.erase(it);

	  it = From->NextLinks.find(this);
	  if (it != From->NextLinks.end()) From->NextLinks.erase(it);*/

}


NODE::NODE(float T, float P, int N)
{
	Time = T;
	Number = N;
	HasNull = false;
	WordId = -1;
	Forward=Backward=1;
	Posterior=1;
	//Posterior = P;
	//Extended = false;
}


class NCNODE
{
	public:

		NCNODE()
		{
			Tmin = INFINI;
			Tmax = -INFINI;
			MeshLinks = new vector<LINK *>;
		};

		void SetMin(float min) {Tmin = min;};
		void SetMax(float max) {Tmax = max;};
		float GetMin() {return Tmin;};
		float GetMax() {return Tmax;};
		void push(NODE *node) 
		{
			set<struct LINK *, LinkCompare>::iterator it;
			NCNodes.push_back(node);

			for (it = node->NextLinks.begin(); it != node->NextLinks.end(); it++)
			{
				TargetNodes.insert((*it)->Target);
			}
		};
		int NbNodes() {return NCNodes.size();};
		NODE *Node(int i) {return NCNodes[i];};
		int Find(NODE *Target) 
		{
			return TargetNodes.count(Target);
		};
		vector<class LINK *> *MeshLinks;


	private:
		float Tmin;
		float Tmax;
		vector <class NODE *> NCNodes;
		set<NODE *> TargetNodes;
};


class NodeCompare
{
	public:
		bool operator()(const struct  NODE* x, const struct  NODE* y) { return x->Time > y->Time; }
};



