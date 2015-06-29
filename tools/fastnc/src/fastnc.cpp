/*
 * =====================================================================================
 * 
 *       Filename:  fastnc.cpp
 * 
 *    Description:  
 * 
 *        Version:  0.2
 *        Created:  07.12.2007 23:01:19 CET
 *       Revision:  none
 *       Compiler:  g++
 * 
 *         Author:  LECOUTEUX Benjamin 
 *        Company:  LIA
 * 
 * =====================================================================================
 */


#define DEFAULT_ORDER 3


bool IGNORE_CASE;

#include "fastnc.h"
#include "alignContainer.h"
#include "buildlm.h"
#include "readlm.h"




#include <iomanip>
#include <stdarg.h>
#include <queue>
#include <iostream>

#include <sys/mman.h>
#include <iostream>
#include <fstream>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <map>
#include <algorithm>
#include <math.h>
#include <set>

#include <unistd.h>


extern char *optarg;
extern int optind, opterr, optopt;

#include <getopt.h>


int debS, endS;

#define EPSILON_TRANS 500000

char *Utterance;

vector<int> Merged;

struct CONT_CTM
{
	char *Line;
	float Origin;
	float Duration;
	float Start;
	float Viterbi;
	int Word;
	int NodeFrom;
	int NodeTarget;
};


bool V =false;

bool VERBOSE=false;
int Profondeur=3;
//bool DTW_VERBOSE=false;

//float EDIT_DIST[10000][10000];

set<int> *TheNoise=NULL;

static int Ids = 1;
static int IdsUNK = 0;

bool PrintAlignWER(CONT_CTM *Ref, CONT_CTM *Hyp, ofstream *Out);

int AlignCTM(vector<CONT_CTM *> *, vector<NCNODE *> *Mesh, ofstream *Out=NULL);
int AddWord(char *Token, ReadLM *LM);
float FoundInMesh(int Word, float Start, float Duration, vector<NCNODE *> *Mesh);

int AlignCTMWithDTW(vector<CONT_CTM *> *, vector<NCNODE *> *Mesh, bool verbosity ,ofstream *Out=NULL);
char *ForEach(char *Buffer, char *&Cursor, const char *Separator);

void RemoveNULL(NODE *Current, LINK *LinkToRemove);
void RemovePau(NODE *&Current, LINK *LinkToRemove, set<CONNECT *, CompareConnects> *Connections);
void RemoveNULLGeneralCase(NODE *&Current, LINK *LinkToRemove,  set<CONNECT *, CompareConnects> *Connections, vector<NODE *> *g,bool DelNode);
void RemoveUniqNULL (NODE *Current, LINK *LinkToRemove,  set<CONNECT *, CompareConnects> *Connections, vector<NODE *> *NewGraph);

void AddVirtualTimeToGraph(NODE *Current, int Time);

void MyDelete(CONT_CTM *);
vector<NODE *> *RemoveNullAndPause(vector<NODE *> *Graph, ReadLM *LM);

vector<NODE*>* ReduceGraph2(vector<NODE *> *Graph);

void DeleteBackLinks(NODE *node, LINK *LinkToRemove);
void DeleteTopLinks(NODE *node, LINK *LinkToRemove);

vector<CONT_CTM *> *LoadCTM(char *CTMFile, ReadLM *LM);
float CompWER(CONT_CTM *a, CONT_CTM *b);

 bool Print(NCNODE *Ref, CONT_CTM *Hyp, ofstream *Out=NULL);
void ComputeBestPathAlignWER(NODE *Current, AlignDTW<CONT_CTM * , CONT_CTM *, float> *MyDTW, ReadLM *LM, bool Reverse);

float BacktrackBestPath(NODE *Current, ReadLM *LM, float Normalize, ofstream *Out=NULL, vector<CONT_CTM *> *TheCTM = NULL, bool Verbose=false, bool Reverse=false);



vector<NODE *> *ExploseMesh(vector<NODE *> *Mesh);

set<int> *LoadNoise(char *noiseFile, ReadLM *LM);


float edit_distance(const string &s1, const string &s2)
{
	float Dist;
	int Small, Big;



	const size_t len1 = s1.length(), len2 = s2.length();

	if (len1 > len2) Big = len1, Small = len2;
	else		Big = len2, Small = len1;

	vector<vector<unsigned int> > d(len1 + 1, vector<unsigned int>(len2 + 1));

	for(int i = 1; i <= len1; ++i)
		for(int j = 1; j <= len2; ++j)
			d[i][j] = min(d[i - 1][j] + 1, min(d[i][j - 1] + 1, d[i - 1][j - 1] + (s1[i - 1] == s2[j - 1] ? 0 : 1)));


	Dist = (float) d[len1][len2] /**(float)Big/(float)Small*/;


	return Dist;
}

	template <class InputIterator, class T>
void my_unique_Nodes ( InputIterator first, InputIterator last, T  *result )
{
	result->push_back(*first);

	while (++first != last)
	{
		if (!(result->back()->Time == (*first)->Time))
			result->push_back(*first);
		else
		{
			result->back()->merge(*first);
			delete *first;
		}
	}
}


	template <class InputIterator, class T>
void my_unique_Links_From ( InputIterator first, InputIterator last, T  *result )
{
	result->push_back(*first);

	while (++first != last)
	{
		if (!(result->back()->WordId == (*first)->WordId && result->back()->From == (*first)->From))
			result->push_back(*first);
		else
			result->back()->merge(*first);
	}
}



	template <class InputIterator, class T>
void my_unique_Links_Target_expand ( InputIterator first, InputIterator last, T  *result )
{
	result->insert(*first);
	LINK * Temp = (*first);

	while (++first != last)
	{
		if (!( Temp->Target == (*first)->Target  && Temp->WordId == (*first)->WordId && Temp->LmProbability == (*first)->LmProbability && Temp->AcProbability == (*first)->AcProbability))
		{
			result->insert(*first);
			Temp = (*first);
		}
		else
		{
			//Temp->merge((*first));

			delete (*first);
		}
	}
}



	template <class InputIterator, class T>
void my_unique_Links_Target ( InputIterator first, InputIterator last, T  *result )
{
	result->insert(*first);
	LINK * Temp = (*first);

	while (++first != last)
	{
		if (!(Temp->WordId == (*first)->WordId && Temp->Target == (*first)->Target))
		{
			result->insert(*first);
			Temp = (*first);
		}
		else
		{
			Temp->merge((*first));
			delete (*first);
		}
	}
}



	template <class InputIterator, class T>
void my_unique_copy ( InputIterator first, InputIterator last, T  *result )
{
	result->push_back(*first);

	while (++first != last)
	{
		if (!(result->back()->WordId == (*first)->WordId))
			result->push_back(*first);
		else
			result->back()->merge(*first);
	}
}


bool verbose = false;

vector<NODE *> *LoadGraph(char *Data, ReadLM *ML=NULL);
vector<NODE *> *LoadMesh(char *Data, ReadLM *ML=NULL);


vector<int> **CommonWords;
map<int, float> **CommonSumsSimilarity;

map<int, char *> IDToWord;


bool SortByTime(NODE *a, NODE *b)
{
	if (a->Time < b->Time) return true;
	return false;
}


bool SortByWordAndFrom(LINK *a, LINK *b)
{
	bool result = false;

	if (a->WordId < b->WordId) result = true;
	if (a->WordId == b->WordId && a->From < b->From) result = true;

	return result;
}


bool SortByAll(LINK *a, LINK *b)
{
	bool result = false;

	if (a->WordId < b->WordId) result = true;
	if (a->WordId == b->WordId && a->LmProbability < b->LmProbability) result = true;
	if (a->WordId == b->WordId && a->LmProbability == b->LmProbability && a->AcProbability < b->AcProbability ) result = true;
	if (a->WordId == b->WordId && a->LmProbability == b->LmProbability && a->AcProbability == b->AcProbability  && a->Target < b->Target) result = true;

	return result;
}





bool SortByWordAndTarget(LINK *a, LINK *b)
{
	bool result = false;

	if (a->WordId < b->WordId) result = true;
	if (a->WordId == b->WordId && a->Target < b->Target) result = true;

	return result;
}


bool SortWords(LINK *a, LINK *b)
{
	if (a->WordId < b->WordId) return true;
	return false;
}

bool SortByPost(LINK *a, LINK *b)
{
	if (a->Posterior > b->Posterior) return true;
	return false;
}




char *ReadHTK(const char *FileName, size_t &size)
{
	char *Addr;
	struct stat sb;
	int fd;
	size_t FileSize;

	off_t pa_offset;



	fd = open(FileName, O_RDONLY);

	if (VERBOSE) cerr <<"open file "<<FileName<<endl;

	if (fd == -1)
	{
		perror("open");
		exit (EXIT_FAILURE);
	}


	if (fstat(fd, &sb) == -1)
	{
		perror("fstat");
		exit(EXIT_FAILURE);
	}

	FileSize = sb.st_size;

	pa_offset = 0 & ~(sysconf(_SC_PAGE_SIZE) - 1);

	if (VERBOSE) cerr <<"map file in memory..."<<endl;
	Addr = (char *)mmap(NULL, FileSize, PROT_READ, MAP_PRIVATE, fd, pa_offset);

	if (Addr == MAP_FAILED)
	{
		perror("mmap");
		exit (EXIT_FAILURE);
	}
	size = FileSize;

	return Addr;
}


float InverseDistance (int a, int b)
{
	float Dist;


	string sa = IDToWord[a];
	string sb = IDToWord[b];

	Dist = /*EDIT_DIST[b][a] = EDIT_DIST[a][b] =*/ edit_distance(sa, sb);

	return 1.0/(1+Dist);
}

vector<int> *FoundCommonWords(NCNODE *Start, NCNODE *End)
{
	int i;

	NODE *CurrentNode;
	LINK *CurrentLink;

	bool Connected;
	vector<int> *CWords;

	set<struct LINK *>::iterator it;

	int x, y;

	x = Start->Node(0)->MyCluster;

	if (CommonWords[x]) return CommonWords[x];
	else CWords = CommonWords[x] = new vector<int>;

	for (i = 0; i < End->NbNodes(); i++)
	{
		CurrentNode = End->Node(i);

		Connected = false;

		for (it = CurrentNode->BackLinks.begin(); it != CurrentNode->BackLinks.end(); it++)
		{
			CurrentLink = (*it);

			if (CurrentLink->From->MyCluster == Start->Node(0)->MyCluster) Connected = true;

			if (Connected == true)
			{
				CWords->push_back( CurrentLink->WordId );
				Connected = false;
			}
		}
	}
	return CWords;
}


float Overlap(NCNODE *Start, NCNODE *End, struct LINK *Link)
{
	float Overlap;
	float NormalizedOverlap;

	float T0, T1;
	float S0, S1;

	S0 = Link->From->Time;
	S1 = Link->Target->Time;

	T0 = Start->GetMin();
	T1 = End->GetMax();

	if (S0 >= T0 && S1 <= T1) Overlap = fabs(S0-S1);
	else if (S0 < T0 && S1 >= T0 && S1 <= T1) Overlap = fabs(T0-S1);
	else if (S0 >= T0 && S0 <= T1 && S1 > T1) Overlap = fabs(T1-S0);
	else if (S0 < T0 && S1 > T1) Overlap = fabs(T0-T1);
	else Overlap = 0.0;

	NormalizedOverlap = Overlap/(fabs(T0-T1)+fabs(S0-S1));
	return NormalizedOverlap;
}



float Similarity(NCNODE *Start, NCNODE *End,struct LINK *Link)
{
	int i;
	float FinalSimilarity;
	float LinkCardinal;
	vector<int> *CWords;
	float SumsSimilarity=0;

	bool Compute = false;

	//LinkCardinal = Start->GetMax() - End->GetMin();

	//if (verbose) cout <<"1, "<<endl;

	CWords = FoundCommonWords(Start, End);

	int N = Start->Node(0)->MyCluster;

	if (CommonSumsSimilarity[N] != NULL)
	{
		if (CommonSumsSimilarity[N]->count(Link->WordId))
		{
			SumsSimilarity = (*(CommonSumsSimilarity[N]))[Link->WordId];
		}
		else Compute = true;
	}
	else
	{
		Compute = true;
		CommonSumsSimilarity[N] = new map<int, float>;
	}

	//if (verbose) cout <<"2, "<<CWords<<endl;

	if (Compute == true)
	{
		for (i = 0; i < CWords->size(); i++) SumsSimilarity+=InverseDistance((*CWords)[i], Link->WordId);
		(*(CommonSumsSimilarity[N]))[Link->WordId] = SumsSimilarity;
	}
	LinkCardinal  = CWords->size();

	float Over = Overlap(Start, End, Link);

	FinalSimilarity = (1.0/fabs(LinkCardinal) * SumsSimilarity) * Over;

	if (Over == 0) FinalSimilarity=0;

	return FinalSimilarity;
}



int FoundGoodNode(int Start, int End, vector<NCNODE *> *FinalNC, struct LINK *Link)
{
	int i;
	int Max = Start;
	float Sim, SimMax=0;

	for (i = Start; i <= End; i++)
	{
		Sim = Similarity((*FinalNC)[i-1], (*FinalNC)[i], Link);
		if (Sim > SimMax)
		{
			SimMax = Sim;
			Max = i;
		}
	}
	return Max;
}


int RemoveDuplicateLinks(vector<NCNODE *> *FinalNC)
{
	vector<LINK *> *SortedLinks;
	int i;
	int NbLinks = 0;

	for (i = 0; i < (*FinalNC).size(); i++)
	{

		if ((*FinalNC)[i]->MeshLinks->size())
		{
			SortedLinks = new vector<LINK *>;

			//cout <<"node : "<<i<<endl;


			std::sort((*FinalNC)[i]->MeshLinks->begin(), (*FinalNC)[i]->MeshLinks->end(), SortWords);
			//cout <<"node1 : "<<i<<endl;

			my_unique_copy((*FinalNC)[i]->MeshLinks->begin(), (*FinalNC)[i]->MeshLinks->end(), SortedLinks);
			//cout <<"node2 : "<<i<<endl;

			delete (*FinalNC)[i]->MeshLinks;
			//cout <<"node3 : "<<i<<endl;
			(*FinalNC)[i]->MeshLinks = SortedLinks;
			//cout <<"node4 : "<<i<<endl;
			NbLinks += SortedLinks->size();
		}
	}
	return NbLinks;
}



void MakeEpsilonTransition(vector<NCNODE *> *FinalNC, int Start, int End, int Except)
{
	int i;

	LINK *Temp;

	for (i = Start; i < End; i++)
	{
		if (i != Except)
		{
			Temp = new LINK((*FinalNC)[i]->Node(0), (*FinalNC)[i+1]->Node(0), 0, EPSILON_TRANS);
			Temp->NCBack = (*FinalNC)[i];
			Temp->NCNext = (*FinalNC)[i+1];

			(*FinalNC)[i]->MeshLinks->push_back(Temp);
		}
	}
}



void NormalizeMesh(vector<NCNODE *> *FinalNC)
{
	float sum = 0;
	float Complement;
	int k;
	LINK *Temp;
	vector<LINK *>::iterator it;

	for (k = 0; k < FinalNC->size()-1; k++)
	{
		sum = 0.0;

		for (it = (*FinalNC)[k]->MeshLinks->begin(); it != (*FinalNC)[k]->MeshLinks->end(); it++)
		{
			//if ((*it)->WordId == EPSILON_TRANS) cout <<"EPS ";
			sum += (*it)->Posterior;
		}
		if (VERBOSE) cerr <<"sum of posteriors node before normalization"<<k<<" ( "<<(*FinalNC)[k]->NbNodes()  <<" nodes ) : "<<sum<<endl;

		if (sum < 1.0)
		{
			Complement = 1.0-sum;

			Temp = new LINK((*FinalNC)[k]->Node(0), (*FinalNC)[k+1]->Node(0), Complement, 0);

			Temp->NCBack = (*FinalNC)[k];
			Temp->NCNext = (*FinalNC)[k+1];

			(*FinalNC)[k]->MeshLinks->push_back(Temp);
		}

		if (sum > 1.0)
		{
			for (it = (*FinalNC)[k]->MeshLinks->begin(); it != (*FinalNC)[k]->MeshLinks->end(); it++)
			{
				//if ((*it)->WordId == EPSILON_TRANS) cout <<"EPS ";
				(*it)->Posterior/=sum;
			}
		}
	}
}


int AssignLinksInMesh(vector<NCNODE *> *FinalNC, vector<NODE *> *ListNodes)
{
	int n;
	set<struct LINK *,LinkCompare >::iterator itmap;
	NODE *CurrentNode;
	int CurrentCluster;
	int Count = 0;
	int Placement;

	for (n = 1;n < ListNodes->size(); n++) 
	{
		CurrentNode = (*ListNodes)[n];
		CurrentCluster = CurrentNode->MyCluster;

		for (itmap = CurrentNode->BackLinks.begin(); itmap != CurrentNode->BackLinks.end(); itmap++ )
		{
			Count++;
			if ((*itmap)->From->MyCluster+1 == CurrentCluster)
			{
				(*itmap)->NCBack = (*FinalNC)[CurrentCluster-1];
				(*itmap)->NCNext = (*FinalNC)[CurrentCluster];;
			}
			else
			{
				Placement = FoundGoodNode((*itmap)->From->MyCluster+1, CurrentCluster, FinalNC, (*itmap));
				(*itmap)->NCBack = (*FinalNC)[Placement-1];
				(*itmap)->NCNext = (*FinalNC)[Placement];
				//MakeEpsilonTransition(FinalNC, (*itmap)->From->MyCluster, CurrentCluster, Placement-1);

			}
		}
	}

	if (VERBOSE) cerr <<"assign each link to a cluster..."<<endl;
	for (n = 0;n < ListNodes->size(); n++) 
	{
		CurrentNode = (*ListNodes)[n];

		for (itmap = CurrentNode->NextLinks.begin(); itmap != CurrentNode->NextLinks.end(); itmap++ )
			(*itmap)->NCBack->MeshLinks->push_back((*itmap));
	}
	if (VERBOSE) cerr <<"OK : "<<endl;

	return Count;
}

int AssignNodeToCluster(vector<NCNODE *> *FinalNC, vector<NODE *> *ListNodes)
{
	NODE *CurrentNode;
	NODE *FirstNode;
	NODE *BackNode;

	bool AddCluster = false;
	int CurrentCluster = 0, n;
	NCNODE *SelectedCluster;

	FirstNode = (*ListNodes)[0];

	SelectedCluster = new NCNODE;

	FirstNode->MyCluster = 0;

	if (VERBOSE) cerr <<"Assign n0 to N0 ... ";
	SelectedCluster->push( FirstNode );
	if (VERBOSE) cerr <<"OK"<<endl;

	if (SelectedCluster->GetMin() < FirstNode->Time)
		SelectedCluster->SetMin(FirstNode->Time);

	if (SelectedCluster->GetMax() > FirstNode->Time)
		SelectedCluster->SetMax(FirstNode->Time);

	FinalNC->push_back( SelectedCluster );

	for (n = 1;n < ListNodes->size(); n++) 
	{
		AddCluster = false;

		if (VERBOSE) cerr <<"node : "<<n<<endl;

		CurrentNode = (*ListNodes)[n];

		if (SelectedCluster->Find(CurrentNode)) AddCluster = true;

		if (AddCluster == true)
		{
			SelectedCluster = new NCNODE;
			FinalNC->push_back( SelectedCluster );

			CurrentCluster++;
		}

		SelectedCluster->push( CurrentNode );

		if (SelectedCluster->GetMin() > CurrentNode->Time)
			SelectedCluster->SetMin(CurrentNode->Time);

		if (SelectedCluster->GetMax() < CurrentNode->Time)
			SelectedCluster->SetMax(CurrentNode->Time);

		CurrentNode->MyCluster = CurrentCluster;
	}
	if (VERBOSE) cerr <<"OK"<<endl;

	return CurrentCluster;
}


vector<int> *SequenceToFind(LINK *Before, LINK *After, int Order, int MaxId)
{
	vector<int> *SequenceToRetrieve = new vector<int>;
	LINK *Tmp;
	int NullNode = 0;
	int i;
	int Next = 1;

	// PRENDRE EN COMPTE LES NULL NODE !!!!

	if (After) SequenceToRetrieve->push_back(After->WordId);
	else Next = 0;

	if (Before)
	{
		Tmp = Before;


		for (i = Next; i < Order+NullNode && Tmp; i++)
		{
			//cout <<"i : "<<i<<endl;
			//cout <<"word : "<<Tmp->WordId<<endl;
			if (Tmp->WordId <= MaxId) SequenceToRetrieve->push_back( Tmp->WordId );
			else NullNode++;

			if (Tmp->From->BackLinks.size()) Tmp = (*Tmp->From->BackLinks.begin());
			else Tmp = NULL;
		}
	}

	return SequenceToRetrieve;
}

void DeleteNodeAndLinks(NODE *node, bool delnode = true)
{
	set<struct LINK *>::iterator it;

	for (it = node->NextLinks.begin(); it != node->NextLinks.end(); it++)
		DeleteBackLinks((*it)->Target, (*it));

	for (it = node->BackLinks.begin(); it != node->BackLinks.end(); it++)
		DeleteTopLinks( (*it)->From, (*it));

	node->BackLinks.clear();
	node->NextLinks.clear();

	if (delnode) delete node;
}



void PropagateNodeWordsToLink(vector<NODE *> *Graph)
{
	int n;
	set<struct LINK *, LinkCompare>::iterator it;

	for (int n=0; n < Graph->size(); n++)
	{
		for (it = (*Graph)[n]->NextLinks.begin(); it != (*Graph)[n]->NextLinks.end(); it++)
		{
			(*it)->WordId = (*it)->Target->WordId;
		}
	}	
}

vector<NODE *> *LinkToNodeGraph(vector<NODE *> *Graph, ReadLM *ML)
{
	vector<NODE *> *ExpandedGraph = new vector<NODE *>;
	map<LINK *, NODE *> Corres;

	std::sort(Graph->begin(), Graph->end(), SortByTime);

	set<struct LINK *>::iterator it;
	set<struct LINK *>::iterator it2;
	NODE *Cloned;

	Graph->insert(Graph->begin(), (*Graph)[0]->CloneDup(false));

	LINK((*Graph)[0], (*Graph)[1], 0, ML->GetMaxId()+1, 0, 0);

	std::sort(Graph->begin(), Graph->end(), SortByTime);
	NODE *End = Graph->back()->CloneDup(false);
	End->Time+=1;
	ExpandedGraph->push_back(End);

	for (int n=0; n < Graph->size(); n++)
	{
		for (it = (*Graph)[n]->BackLinks.begin(); it != (*Graph)[n]->BackLinks.end(); it++)
		{
			if (n < Graph->size()-1) Cloned = (*it)->Target->CloneDup(false);
			else 
			{
				if ((*it)->WordId > ML->GetMaxId())
					Cloned = End;
				else 
				{
					Cloned = (*it)->Target->CloneDup(false);
					new LINK(Cloned, End, 0,  ML->GetMaxId()+1, 0, 0);
				}
			}
			if (Cloned != End)
			{
				Cloned->WordId = (*it)->WordId;
				ExpandedGraph->push_back(Cloned);
			}
			Corres.insert(pair<LINK *, NODE *> ((*it), Cloned));
		}
	}

	map<CONNECT *, LINK *, CompareConnects> Connections;

	for (int n=0; n < Graph->size(); n++)
	{
		for (it = (*Graph)[n]->BackLinks.begin(); it != (*Graph)[n]->BackLinks.end(); it++)
			if ((*Graph)[n]->NextLinks.size())
			{
				for (it2 = (*Graph)[n]->NextLinks.begin(); it2 != (*Graph)[n]->NextLinks.end(); it2++)
				{

					CONNECT *c = new CONNECT(Corres[(*it)], Corres[(*it2)]);

					/*if (Connections.find(c) != Connections.end()) 
					  {
					  NODE *cl = Corres[(*it)]->CloneDup(true, true, true);


					  cerr <<"duplicata "<<n<<endl;
					  cerr <<(*Connections.find(c)).second->AcProbability<<endl;
					  cerr <<(*it2)->AcProbability<<endl;
					  }
					  else*/
					{
						LINK *l = new LINK(Corres[(*it)], Corres[(*it2)], (*it2)->Posterior, (*it2)->WordId, (*it2)->LmProbability, (*it2)->AcProbability);
						Connections.insert(pair<CONNECT *, LINK *> (c,  l));
					}
				}
			}
	}


	cerr <<"expanded size : "<<ExpandedGraph->size()<<endl;

	for (int n=0; n < Graph->size(); n++)
		DeleteNodeAndLinks((*Graph)[n]);


	for (int n=0; n < ExpandedGraph->size(); n++)
		(*ExpandedGraph)[n]->Number=n;


/*
		int NbNodes;
		int n=1;
		do
		{
		NbNodes = ExpandedGraph->size();
		cerr <<"Reducing pass "<<n++<<", nb nodes : "<<NbNodes<<endl;
		ExpandedGraph = ReduceGraph2(ExpandedGraph);
		}
		while(NbNodes != ExpandedGraph->size());
*/				
	return ExpandedGraph;
}





vector<int> *SequenceToFind2(LINK *Before, LINK *After, int Order, int MaxId)
{
	vector<int> *SequenceToRetrieve = new vector<int>;
	LINK *Tmp;
	int NullNode = 0;
	int i;
	int Next = 1;

	// PRENDRE EN COMPTE LES NULL NODE !!!!

	//cerr <<"sequencetofind"<<endl;

	if (After) 
	{
		if (After->WordId <= MaxId) 
		{
			SequenceToRetrieve->push_back(After->WordId);
			//	cerr <<" " <<IDToWord[After->WordId]<<" ";
		}
		else NullNode=1;
	}
	else Next = 0;

	if (Before)
	{
		Tmp = Before;


		for (i = Next; i < Order+NullNode && Tmp; i++)
		{
			//cout <<" "<<IDToWord[Tmp->WordId]<<" ";
			if (Tmp->WordId <= MaxId) SequenceToRetrieve->push_back( Tmp->WordId );
			else NullNode++;

			if (Tmp->From->BackLinks.size()) Tmp = (*Tmp->From->BackLinks.begin());
			else Tmp = NULL;
		}
	}

	return SequenceToRetrieve;
}






vector<NCNODE *> *FastNC(vector<NODE *> *ListNodes)
{
	vector<NCNODE *> *FinalNC;
	int NbLinks = 0;
	float sum;
	int i;


	int Count = 0;
	int NClust;

	FinalNC = new vector<NCNODE *>;

	if (ListNodes->size())
	{
		if (VERBOSE) cerr <<"Allocation of network confusion clusters ... "<<endl;
		NClust = AssignNodeToCluster(FinalNC, ListNodes)+50;
		if (VERBOSE) cerr <<"number of clusters : "<<NClust-50<<endl;

		CommonWords  = new vector<int> *[NClust];

		CommonSumsSimilarity = new map<int, float> *[NClust];

		for (i = 0; i < NClust; i++)
		{
			CommonWords[i] = NULL;
			CommonSumsSimilarity[i] = NULL;
		}

		if (VERBOSE) cerr << "Allocation of links in network confusion ... "<<   (*ListNodes)[0]->BackLinks.size()  <<endl;
		Count = AssignLinksInMesh(FinalNC, ListNodes);
		if (VERBOSE) cerr <<"OK"<<endl;
		vector<LINK *>::iterator it;


		if (VERBOSE) cerr <<"remove duplicate links ( "<<Count<<" )"<<endl;
		NbLinks  = RemoveDuplicateLinks(FinalNC);
		if (VERBOSE) cerr <<"OK : "<<NbLinks<<endl;

		if (VERBOSE) cerr <<"Normalize mesh transitions"<<endl;
		NormalizeMesh(FinalNC);
		if (VERBOSE) cerr <<"OK"<<endl;

		if (VERBOSE) cerr <<"remove duplicate links after normalization"<<endl;
		NbLinks = RemoveDuplicateLinks(FinalNC);
		if (VERBOSE) cerr <<"OK : "<<NbLinks<<endl;


		for (i = 0; i < FinalNC->size()-1; i++)
		{
			sum = 0.0;

			for (it = (*FinalNC)[i]->MeshLinks->begin(); it != (*FinalNC)[i]->MeshLinks->end(); it++)
				sum += (*it)->Posterior;

			if (VERBOSE) cerr <<"sum of posteriors node "<<i<<" ( "<<(*FinalNC)[i]->NbNodes()  <<" nodes ) : "<<sum<<endl;
		}
	}
	else if (VERBOSE) cerr <<"no node loaded !"<<endl;


	return FinalNC;
}




float FindProb_seq3(vector<int> *SequenceToRetrieve, ReadLM *LM, int *OrderFind = NULL, float *BackOff=NULL, int *UsedContext=NULL)
{

	if (LM == NULL) return 0.0;

	int Ngram[LM->GetOrder()];
	int NumberPrevious=0;

	if ((*SequenceToRetrieve)[0] > LM->GetMaxId()) return 0;
	NumberPrevious = SequenceToRetrieve->size() - 1;

	for (int j = 0; j < NumberPrevious+1; j++)
		Ngram[j] = (*SequenceToRetrieve)[NumberPrevious-j];

	int a;

	float p= LM->FindProbability(Ngram, NumberPrevious+1, false, true, OrderFind, BackOff, UsedContext);

	return p;
}





float FindProb_seq(vector<int> *SequenceToRetrieve, ReadLM *LM, int *ContextSize = NULL)
{

	if (LM == NULL) return 0.0;

	int Ngram[LM->GetOrder()];
	int NumberPrevious=0;

	if ((*SequenceToRetrieve)[0] > LM->GetMaxId()) return 0;
	NumberPrevious = SequenceToRetrieve->size() - 1;

	for (int j = 0; j < NumberPrevious+1; j++)
		Ngram[j] = (*SequenceToRetrieve)[NumberPrevious-j];

	int a;

	float p= LM->FindProbability(Ngram, NumberPrevious+1, false, true, NULL);

	return p;
}



float GetMaxContext(LINK *Before, NODE *After, ReadLM *LM, int *OrderFound, int *UsedContext)
{
	set<struct LINK *>::iterator it;
	float BackOff = 0.0;
	float BackOffCtx = 0.0;

	vector<int> *Sequence;
	*UsedContext = 0;
	*OrderFound = 0;
	Sequence = SequenceToFind(Before, NULL, LM->GetOrder()-1, LM->GetMaxId());

	Sequence->insert(Sequence->begin(), 0);


	int Ctx = 0;
	int of;

	if (After)
	{
		for (it = After->NextLinks.begin(); it != After->NextLinks.end(); it++)
		{
			if ((*it)->WordId > LM->GetMaxId()) 
			{
				*UsedContext=Sequence->size()-1;
				*OrderFound=Sequence->size();
				BackOffCtx = 0;
				break;
			}

			(*Sequence)[0] = (*it)->WordId;
			//cerr <<"size seq before : "<<Sequence->size()<<endl;
			FindProb_seq3(Sequence, LM, &of, &BackOff, &Ctx);

			if (*OrderFound < of) *OrderFound = of;
			if (*UsedContext < Ctx) *UsedContext = Ctx, BackOffCtx = BackOff;
		}
	}
	else  *UsedContext = Sequence->size()-1, *OrderFound = Sequence->size();


	delete Sequence;
	return BackOffCtx;
}




void DeleteBackLinks(NODE *node, LINK *LinkToRemove)
{
	set<struct LINK *>::iterator it;
	it = node->BackLinks.find(LinkToRemove);

	if (it != node->BackLinks.end())
		node->BackLinks.erase(it);
}


void DeleteTopLinks(NODE *node, LINK *LinkToRemove)
{
	set<struct LINK *>::iterator it;
	it = node->NextLinks.find(LinkToRemove);


	if (it != node->NextLinks.end())
		node->NextLinks.erase(it);
}





float FindProb_seq2(vector<int> *SequenceToRetrieve, LINK *After,ReadLM *LM, int *ContextSize = NULL)
{

	if (LM == NULL) return 0.0;

	if (After->WordId > LM->GetMaxId()) return 0;

	int Ngram[LM->GetOrder()];
	int NumberPrevious=0;

	//if ((*SequenceToRetrieve)[0] > LM->GetMaxId()) return 0;
	NumberPrevious = SequenceToRetrieve->size() - 1;

	int j;

	for (j = 0; j < NumberPrevious+1; j++)
		Ngram[j] = (*SequenceToRetrieve)[NumberPrevious-j];

	Ngram[j] = After->WordId;

	int a;

	float p= LM->FindProbability(Ngram, NumberPrevious+2, false, true, NULL);

	return p;
}




float FindProb(LINK *Before, LINK *After, ReadLM *LM, int *ContextSize = NULL)
{

	if (LM == NULL) return 0.0;

	int i=0;
	LINK *Tmp;
	int Order = LM->GetOrder();
	vector<int> *SequenceToRetrieve;
	int NumberPrevious=0;
	float Pr;
	int NullNode=0;

	if (After->WordId > LM->GetMaxId()) return 0;

	SequenceToRetrieve = SequenceToFind(Before, After, Order, LM->GetMaxId());

	Pr = FindProb_seq(SequenceToRetrieve, LM, ContextSize);

	delete SequenceToRetrieve;


	return Pr;
}

NODE *NODE::SearchCloneInContext(LINK *Before, LINK *After, ReadLM *LM, float LmProb, int Order, int UsedContext, set<CLONE_HASH *, CloneCompare_Word> &CloneHashWord, set<CLONE_HASH *, CloneCompare_History> &CloneHashHistory, CLONE_HASH *&CloneToAdd, vector<int> *FullSequence, vector<int> *SequenceToRetrieve)
{
	//vector<int> *FullSequence = new vector<int>;
	int NumberPrevious=0;
	LINK *Tmp;
	int i;
	CloneToAdd = NULL;

	set<CLONE_HASH *, CloneCompare_Word>::iterator itW;
	set<CLONE_HASH *, CloneCompare_History>::iterator itH;

	struct CLONE_HASH *SearchClone = NULL;
	struct CLONE_HASH *Result = NULL;

	int MaxId = LM->GetMaxId();


	//FullSequence = SequenceToFind(Before, NULL, Order-1, MaxId);

	SearchClone = new struct CLONE_HASH;
	SearchClone->NextWordId = After->WordId;
	SearchClone->NextAcProb = After->AcProbability;
	SearchClone->NextLmProb = LmProb;
	SearchClone->From = Before->From;	
	SearchClone->History = FullSequence;

	CloneToAdd = SearchClone;

	//if (After->WordId > MaxId) return NULL; 


	pair<set<CLONE_HASH *, CloneCompare_Word>::iterator,set<CLONE_HASH *, CloneCompare_Word>::iterator> pit;



	itH = CloneHashHistory.find(SearchClone);
//	itW = CloneHashWord.find(SearchClone);	

	if (itH ==  CloneHashHistory.end()) 
	{
		itW = CloneHashWord.find(SearchClone);
		if (itW != CloneHashWord.end()) 
		{
			Result = *itW;
			pit = CloneHashWord.equal_range(SearchClone);
		}
	}
	else Result = (*itH);

	if (After->WordId > MaxId && Result != (*itH)) Result = NULL;

	//if (Result != *itH) return NULL;

	set<struct LINK *>::iterator it;

	map<int, float> Cache;

	if (Result && Result != (*itH) )
	{
		pit = CloneHashWord.equal_range(SearchClone);
		set<CLONE_HASH *, CloneCompare_Word>::iterator itb, ite;
		itb = pit.first;
		ite = pit.second;

		FullSequence->insert(FullSequence->begin(), 0);

		for (itW = itb; itW != ite; itW++)
		{
			Result = *itW;

			//memset(Cache, 0, sizeof(float)*(MaxId+1));
			//cerr <<"--->"<<Result->CloneTarget<<endl;
			//cerr <<"next : "<<Result->CloneTarget->NextLinks.size()<<endl;
			for (it = (*itW)->CloneTarget->NextLinks.begin(); it != (*itW)->CloneTarget->NextLinks.end(); it++)
			{
				if ((*it)->WordId > MaxId)
				{
					Result=NULL;
					break;
				}
				else
				{
					//float LmProb;
					/*if (!Cache.count((*it)->WordId))
					{
						(*FullSequence)[0] = (*it)->WordId;
						LmProb = FindProb_seq( FullSequence  , LM, NULL);
						Cache[(*it)->WordId] = LmProb;
					}
					else LmProb = Cache[(*it)->WordId]; 
					*/
					
					(*FullSequence)[0] = (*it)->WordId;
					LmProb = FindProb_seq( FullSequence  , LM, NULL);
					
					if (fabs(LmProb - ((*it)->LmProbability)) > PRECISION)
					{
						Result = NULL;
						break;
					}
				}
			}
			//if (Result) break;
		}
		FullSequence->erase(FullSequence->begin());
	}



	if (Result) return Result->CloneTarget;

	return NULL;
}


void ExpandNodeSRILike(NODE *n, ReadLM *LM, vector<NODE *> *ExpandedGraph)
{
	set<CLONE_HASH *, CloneCompare_All>::iterator ItCtx;
	set<CLONE_HASH *, CloneCompare_All> CloneHashHistory;
	vector <NODE *> Cloned;
	vector<vector <int> *> Context;
	//vector <int> * Context;
	//int ContextSize = LM->GetOrder();
	set<struct LINK *>::iterator Previous;
	set<struct LINK *>::iterator Next;
	float LmProb;

	map<CONNECT *, LINK *,CompareConnects> Connections;

	if (n->BackLinks.size() == 0 || n->NextLinks.size() == 0)
	{
		LINK *Before = NULL;
		LINK *After = NULL;

		NODE *NewNode = n->CloneDup(true);
		NewNode->ContextToUse=1;
		ExpandedGraph->push_back(NewNode);

		if (NewNode->NextLinks.size())
		{
			for (Next = NewNode->NextLinks.begin(); Next != NewNode->NextLinks.end(); Next++)
			{
				LmProb = FindProb(NULL, (*Next), LM);
				(*Next)->LmProbability = LmProb;
				if ((*Next)->WordId > LM->GetMaxId()) NewNode->HasNull = true;
			}

		}
	}
	else
	{
		int seq;
		for (seq=0, Previous = n->BackLinks.begin(); Previous != n->BackLinks.end(); Previous++, seq++)
		{
			for (Next = n->NextLinks.begin(); Next != n->NextLinks.end(); Next++)
			{
				CLONE_HASH *Clone = new CLONE_HASH;


				int UsedContext = LM->GetOrder();
				int OrderFound;

				float Back = 0.0;

				Back = GetMaxContext((*Next), (*Next)->Target, LM, &OrderFound, &UsedContext);

				if (Next == n->NextLinks.begin())
				{
					Context.push_back(SequenceToFind2(*Previous, NULL, (*Previous)->From->ContextToUse, LM->GetMaxId()));
				}
				Clone->History = Context[seq];
				//Clone->Target = (*Next)->Target;

				//LmProb = FindProb_seq2(Context[seq], *Next, LM, NULL);
				
				
				LmProb = FindProb(*Previous, *Next, LM);

				ItCtx = CloneHashHistory.find(Clone);

				if (ItCtx != CloneHashHistory.end())
				{
					CONNECT *c = new CONNECT((*Previous)->From, (*ItCtx)->CloneTarget);
					if (Connections.find(c) == Connections.end())
					{
						LINK *l=new LINK((*Previous)->From, (*ItCtx)->CloneTarget, (*Previous)->Posterior, (*Previous)->WordId, (*Previous)->LmProbability, (*Previous)->AcProbability);
						Connections.insert(pair<CONNECT *, LINK *>(c, l));
					}
					else delete c;


					c = new CONNECT((*ItCtx)->CloneTarget, (*Next)->Target);
					if (Connections.find(c) == Connections.end())
					{				
						LINK *l=new LINK((*ItCtx)->CloneTarget, (*Next)->Target, (*Next)->Posterior, (*Next)->WordId, LmProb, (*Next)->AcProbability);
						Connections.insert(pair<CONNECT *, LINK *>(c, l));
					}
					else delete c;

					delete Clone;
				}
				else
				{
					NODE *NewNode;

					NewNode = n->CloneDup(false);

					LINK *l = new LINK((*Previous)->From, NewNode, (*Previous)->Posterior, (*Previous)->WordId, (*Previous)->LmProbability, (*Previous)->AcProbability);
					new LINK(NewNode, (*Next)->Target, (*Next)->Posterior, (*Next)->WordId, LmProb, (*Next)->AcProbability);

					NewNode->ContextToUse=UsedContext;
					Clone->CloneTarget = NewNode;
					CloneHashHistory.insert(Clone);
										
					for (int i = 1; i <  (*Previous)->From->ContextToUse; i++)
					{

						CLONE_HASH *CloneTemp = new CLONE_HASH;
						
						CloneTemp->History = SequenceToFind2(*Previous, NULL, i, LM->GetMaxId());
						if ( CloneHashHistory.find(CloneTemp) == CloneHashHistory.end()  )
						{
							CloneTemp->CloneTarget = NewNode;
							CloneHashHistory.insert(CloneTemp);
						}
						else delete CloneTemp->History, delete CloneTemp;
					}

					
					ExpandedGraph->push_back(NewNode);
				}
			}
		}
	}
	set<CLONE_HASH *, CloneCompare_All>::iterator it3;

	for ( it3 = CloneHashHistory.begin(); it3 != CloneHashHistory.end(); it3++) 
		delete (*it3);

	vector<vector<int> *>::iterator itv;

	for (itv = Context.begin(); itv != Context.end(); itv++) delete *itv;


}



void ExpandNode(NODE *CurrentNode, ReadLM  *LM, vector<NODE *> *ExpandedGraph, int OrderWithoutLM)
{
	int i,k;
	int Order;

	if (LM) Order = LM->GetOrder();
	else Order = OrderWithoutLM;

	NODE *Cloned;
	set<class Ngram> ExtendedGrams;

	set<CLONE_HASH *, CloneCompare_Word> CloneHashWord;
	set<CLONE_HASH *, CloneCompare_History> CloneHashHistory;
	vector<CLONE_HASH *> ToDelete;

	set<struct LINK *>::iterator it;
	set<struct LINK *>::iterator it2;
	set<struct LINK *>::iterator it5;


	bool SameNode;
	float LmProb=0;
	set<CONNECT *, CompareConnects> Connections;

	vector<vector<int> *> SequenceToRetrieve;
	vector<vector<int> *> FullSequence;
	vector<int> UsedContexts;

	if (CurrentNode->BackLinks.size() == 0 || CurrentNode->NextLinks.size() == 0)
	{
		LINK *Before = NULL;
		LINK *After = NULL;


		Cloned = CurrentNode->Clone(true);
		ExpandedGraph->push_back(Cloned);

		if (Cloned->NextLinks.size())
		{
			for (it = Cloned->NextLinks.begin(); it != Cloned->NextLinks.end(); it++)
			{

				LmProb = FindProb(NULL, (*it), LM);
				(*it)->LmProbability = LmProb;
			}

		}
	}
	else
	{
		int ContextSize;
		//if (V) cerr<<"ici : nexlinks : "<<  CurrentNode->NextLinks.size()<<", back : "<<CurrentNode->BackLinks.size()  <<endl;

		CLONE_HASH *CloneToAdd;

		int iseq;

		for (it2 = CurrentNode->NextLinks.begin(); it2 != CurrentNode->NextLinks.end(); it2++)
		{
			for (iseq = 0, it = CurrentNode->BackLinks.begin(); it != CurrentNode->BackLinks.end(); it++, iseq++)
			{
				if (it2 == CurrentNode->NextLinks.begin())
				{	
					int OrderFound;
					int UsedContext;

					//GetMaxContext((*it2), (*it2)->Target, LM, &OrderFound, &UsedContext);
					//SequenceToRetrieve.push_back(SequenceToFind((*it), NULL, UsedContext, LM->GetMaxId()));
					
					//UsedContexts.push_back(UsedContext);
					
					GetMaxContext((*it), CurrentNode, LM, &OrderFound, &UsedContext);
					//SequenceToRetrieve.push_back(SequenceToFind((*it), NULL, Order-1, LM->GetMaxId()));
					FullSequence.push_back(SequenceToFind((*it), NULL, Order-1, LM->GetMaxId()));
					
				}

				LmProb = FindProb_seq2(FullSequence[iseq], (*it2), LM, NULL);
				//if (V) cout <<"search clone : "<< IDToWord[(*it2)->WordId]<< " -o- ";
				Cloned = CurrentNode->SearchCloneInContext((*it), (*it2), LM, LmProb, Order, 0, CloneHashWord, CloneHashHistory, CloneToAdd, FullSequence[iseq], NULL);

				//cout << " - "<<LmProb<<endl;
				//cout <<" "<< IDToWord[(*it)->WordId]  <<endl;

				if (Cloned) 
				{
					CONNECT *ConnectTmp = new CONNECT((*it)->From, Cloned, (*it)->WordId);
					if (Connections.find(ConnectTmp) == Connections.end())
					{
						new LINK((*it)->From, Cloned, (*it)->Posterior, (*it)->WordId, (*it)->LmProbability, (*it)->AcProbability);
						Connections.insert(ConnectTmp);
					}
					else delete ConnectTmp;

					ConnectTmp = new CONNECT((*it2)->Target, Cloned, (*it2)->WordId);
					if (Connections.find(ConnectTmp) == Connections.end())
					{
						new LINK(Cloned, (*it2)->Target ,(*it2)->Posterior, (*it2)->WordId, LmProb, (*it2)->AcProbability);
						Connections.insert(ConnectTmp);
					}
					else delete ConnectTmp;
				}
				else
				{
					Cloned = CurrentNode->Clone(false);
					new LINK( (*it)->From, Cloned, (*it)->Posterior, (*it)->WordId, (*it)->LmProbability, (*it)->AcProbability);
					Connections.insert(new CONNECT((*it)->From, Cloned, (*it)->WordId));
					new LINK( Cloned, (*it2)->Target, (*it2)->Posterior, (*it2)->WordId, LmProb, (*it2)->AcProbability);
					Connections.insert(new CONNECT((*it2)->Target, Cloned, (*it2)->WordId));

					ExpandedGraph->push_back(Cloned);
				}
				//if (CloneToAdd)
				//{
				CloneToAdd->CloneTarget = Cloned;
				set<CLONE_HASH *, CloneCompare_History>::iterator itH;
				set<CLONE_HASH *, CloneCompare_Word>::iterator itW;

				itH = CloneHashHistory.find(CloneToAdd);
				itW = CloneHashWord.find(CloneToAdd);
				//itW = CloneHashWord.end();

				//CloneHashWord.insert(CloneToAdd);
				//CloneHashHistory.insert(CloneToAdd);

				if (itH == CloneHashHistory.end())
				{
					CloneHashWord.insert(CloneToAdd);
					ToDelete.push_back(CloneToAdd);
					CloneHashHistory.insert(CloneToAdd);
				}
				else if (itW == CloneHashWord.end())
				{
					CloneHashWord.insert(CloneToAdd);
					ToDelete.push_back(CloneToAdd);
					CloneHashHistory.insert(CloneToAdd);
				}
				else 
				{
					//delete CloneToAdd->History;
					delete CloneToAdd;
				}
				//}
			}
		}
	}

	set<CONNECT *, CompareConnects>::iterator C1;
	for (C1 = Connections.begin(); C1 != Connections.end(); C1++) delete (*C1);


	vector<CLONE_HASH *>::iterator it3;

	for ( it3 = ToDelete.begin(); it3 != ToDelete.end(); it3++) 
	{
		delete (*it3);
	}
	
	vector<vector<int> *>::iterator itv;

	for (itv = SequenceToRetrieve.begin(); itv != SequenceToRetrieve.end(); itv++) delete *itv;
	for (itv = FullSequence.begin(); itv != FullSequence.end(); itv++) delete *itv;

}


float AddLogP(float x, float y)
{
	if (x<y) {
		float temp = x; x = y; y = temp;
	}
	if (y == -HUGE_VAL) {
		return x;
	} else {
		float diff = y - x;
		//return x + log10(1.0 + exp(diff * M_LN10));
		return x + log(1.0 + exp(diff));
	}
}


void ComputeForward(NODE *Current)
{
	set<struct LINK *>::iterator it;
	Current->Viterbi=0;
	Current->Forward=0;
	float Prob = -HUGE_VAL;
	float Best = -HUGE_VAL;
	float Temp;
	//cerr <<"nb backlinks : "<<Current->BackLinks.size()<<endl;
	for (it = Current->BackLinks.begin(); it != Current->BackLinks.end(); it++)
	{
		LINK *Path = (*it);
		Temp = Path->From->Viterbi + Path->Weight();
		if (Temp > Best) Current->Viterbi = Temp, Best = Temp; 
		Prob = AddLogP(Prob, Path->Weight(true) + Path->From->Forward);
		Current->Forward = Prob;
	}	
	//cerr <<"forward : "<<Prob<<endl;	
}


void ComputeBackwardAndPosteriors(NODE *Current, float Normalize)
{
	set<struct LINK *>::iterator it;

	float Prob = -HUGE_VAL;
	Current->Backward=0;


	for (it = Current->NextLinks.begin(); it != Current->NextLinks.end(); it++)
	{
		LINK *Path = (*it);
		Prob = AddLogP(Prob, Path->Weight(true) + Path->Target->Backward);
		Current->Backward = Prob;
		(*it)->Posterior = exp (Current->Forward + (*it)->Weight(true) + (*it)->Target->Backward - Normalize);
		if ((*it)->Posterior > 1.0) (*it)->Posterior = 1.0;
	}	

	//cerr <<"posterior : "<<Current->Forward<<", "<<Current->Backward<<", "<<Normalization<<endl; 
	Current->Posterior = exp (Current->Forward + Current->Backward - Normalize);
	if (Current->Posterior > 1.0) Current->Posterior = 1.0;
	//cerr <<" = "<< Current->Posterior<<endl;	
}


// we assume :
// - that nodes are sorted by topology
// - lm probabilities are computed

void ComputePosteriors(vector<NODE *> *Graph)
{
	float Normalization;



	//cerr<<"number of nodes : "<<Graph->size()<<endl;
	//cerr <<"compute forward"<<endl;
	for (int n = 0; n < Graph->size(); n++) 	
	{
		//cout <<"node : "<<n<<endl;
		ComputeForward((*Graph)[n]);	
	}
	Normalization = (*Graph)[Graph->size() - 1]->Forward;


	cerr <<"compute backward, normalize : "<<Normalization<<endl;
	for (int n = Graph->size() - 1; n >= 0; n--) 	
	{	
		//cerr <<"---> n : "<<n<<endl;		
		ComputeBackwardAndPosteriors((*Graph)[n], Normalization);	
	}


}



void AddVirtualTimeToGraph(NODE *Current, int Time)
{
	set<struct LINK *>::iterator it;

	if ((Current->Time == -1 && Time == 0) || Time)
	{
		if (Current->Time < Time || Current->Time == -1)
		{
			Current->Time = Time;

			for (it = Current->NextLinks.begin(); it != Current->NextLinks.end(); it++)
			{
				AddVirtualTimeToGraph((*it)->Target, Time+1);
			}
		}
	}

}


void ComputeBestPath(NODE *Current)
{
	set<struct LINK *>::iterator it;

	Current->Viterbi = 0;
	float Best=-HUGE_VAL;
	float Temp;

	for (it = Current->BackLinks.begin(); it != Current->BackLinks.end(); it++)
	{
		LINK *Path = (*it);
		Temp = Path->From->Viterbi + Path->Weight();
		if (Temp > Best) Current->Viterbi = Temp, Best = Temp; 
	}
}


float BackTrackBestHyp(NODE *Current, vector<LINK *> *CurrentPath, vector<LINK *> *BestPath, vector<CONT_CTM *> *SearchedPath, int CurrentWord, float Score, float &Best, int MaxId)
{
	set<struct LINK *>::iterator it;




	if (CurrentWord == SearchedPath->size())
	{
		if (Score > Best) 
		{
			Best = Score;
			BestPath->clear();
			*BestPath = *CurrentPath;
		}
	}
	else
	{
		//cout <<"hypot : "<<CurrentWord<< ": "<<(*SearchedPath)[CurrentWord]->Word<< " ("<<debS<<", "<<endS<<" ) "<<endl;
		if ((*SearchedPath)[CurrentWord]->Word == debS || (*SearchedPath)[CurrentWord]->Word == endS)
			BackTrackBestHyp(Current, CurrentPath, BestPath, SearchedPath, CurrentWord+1, Score, Best, MaxId);
		else	
		{
			for (it = Current->NextLinks.begin(); it != Current->NextLinks.end(); it++)
			{
				LINK *Path = (*it);
				if (Path->WordId == (*SearchedPath)[CurrentWord]->Word || Path->WordId > MaxId)
				{
					//cout <<"path : "<< Path->WordId<<" and cur : "<<(*SearchedPath)[CurrentWord]->Word<<endl;
					int Avance = 1;
					if (Path->WordId > MaxId) Avance=0;

					if (Path->WordId <= MaxId) CurrentPath->push_back(Path);
					BackTrackBestHyp(Path->Target, CurrentPath, BestPath, SearchedPath, CurrentWord+Avance, Score+Path->Weight(), Best, MaxId);
					if (Path->WordId <= MaxId) CurrentPath->pop_back();
				}
			}
		}
	}
	return Best;
}




void BestMeshPath(vector<NCNODE *> *Mesh, ReadLM *LM, ofstream *Out=NULL)
{
	if (Out == NULL) Out = static_cast<ofstream*>(&cout);

	LINK *BestLink = NULL;
	float PreviousEnd=-1;

	for (int i = 0; i < Mesh->size()-1; i++)
	{
		sort((*Mesh)[i]->MeshLinks->begin(), (*Mesh)[i]->MeshLinks->end(), SortByPost);

		BestLink = (*(*Mesh)[i]->MeshLinks)[0];
	
			
		if ((LM && BestLink->WordId <= LM->GetMaxId() && BestLink->WordId > 0) 
			|| (!LM && BestLink->WordId > 0)	)
		{
			if (PreviousEnd < 0) PreviousEnd = BestLink->From->Time;

			if (PreviousEnd < BestLink->From->Time) PreviousEnd = BestLink->From->Time;

			*Out <<Utterance<<" "<<"1"<<" "<<fixed<<setprecision(2)<<PreviousEnd<<" "<<setprecision(2) <<int((BestLink->Target->Time-PreviousEnd)*100)/100.0<<" "<< IDToWord[BestLink->WordId] <<" "<< setprecision(5)<<BestLink->Posterior <<endl;
			PreviousEnd=BestLink->Target->Time;
		}
	}
}


float MAXVITERBI=0.0;




float ComputeAllPath(NODE *Current, vector<CONT_CTM *> *Reference, ofstream *Out=NULL)
{
	int n;

	set<struct LINK *>::iterator it;

	//	BacktrackBestPath(Current, LM, 0, (ofstream *) -1, CurrentPath);

	for (it = Current->NextLinks.begin(); it != Current->NextLinks.end(); it++)
	{
		ComputeAllPath((*it)->Target, Reference); 
	}
	return -HUGE_VAL;
}



float ComputeViterbiDecodeAlignWER(vector<NODE *> *Graph, vector<CONT_CTM *> *Reference, ofstream *Out=NULL, bool Reverse=false)
{
	int n;

	class AlignDTW<CONT_CTM * , CONT_CTM *, float> *MyDTW = new AlignDTW<CONT_CTM * , CONT_CTM *, float>(1000, *Reference, CompWER, PrintAlignWER, (float) 9, (float) 10,  (float) 10);
	if (Out == NULL) Out = static_cast<ofstream*>(&cout);

	MyDTW->InitDTW();

	if (Reverse == false)	for (n = 0; n < Graph->size(); n++) 		ComputeBestPathAlignWER((*Graph)[n], MyDTW, NULL, Reverse);
	else			for (n = Graph->size() - 1; n >= 0; n--) 	ComputeBestPathAlignWER((*Graph)[n], MyDTW, NULL, Reverse);

	if 	(Reverse == false && n)			return (*Graph)[n-1]->Viterbi;
	else if (Reverse == true && Graph->size())	return (*Graph)[0]->Viterbi;


	delete MyDTW;

	return -HUGE_VAL;
}





void MyDelete(CONT_CTM *i)
{
	delete i;
}




void AddPath(NODE *Current,  vector<CONT_CTM *> *CurrentPath, AlignDTW<CONT_CTM * , CONT_CTM *, float> *MyDTW, float &Best, int NbRecursive=1, bool Reverse = false)
{

	set<struct LINK *>::iterator it;
	set<struct LINK *, LinkCompare> *Links;
	bool Pop=false;
	float Temp;

	if (Reverse == false) 	Links = &Current->NextLinks;
	else			Links = &Current->BackLinks;

	if (NbRecursive && Links->size())
	{
		for (it = Links->begin(); it != Links->end(); it++)
		{
			int AddRec=0;
			LINK *Path = (*it);


			if (Pop == true) 
			{
				delete CurrentPath->back();
				CurrentPath->pop_back();
			}


			CONT_CTM *tmp = new CONT_CTM;
			tmp->Word = Path->WordId;	

			if (!TheNoise || (TheNoise && TheNoise->find(tmp->Word) == TheNoise->end())) 
			{
				CurrentPath->push_back(tmp);
				Pop=true;
			}
			else delete tmp, Pop=false, AddRec=1;

			if (Reverse == false) 	AddPath(Path->Target, CurrentPath, MyDTW, Best,NbRecursive-1+AddRec, Reverse);		
			else			AddPath(Path->From, CurrentPath, MyDTW, Best,NbRecursive-1+AddRec, Reverse);		

		}
	}
	else
	{
		if (CurrentPath->size())
		{
			MyDTW->CalculerCheminDTW(*CurrentPath, 0, 0);
			Temp = MyDTW->GetMax(*CurrentPath, 0, 0);
			if (Temp > Best) Best = Temp; 
		}
		//else Current->Viterbi = 0;
	}

	if (Pop == true) 
	{
		delete CurrentPath->back();
		CurrentPath->pop_back();
	}
}






void ComputeBestPathAlignWER(NODE *Current, AlignDTW<CONT_CTM * , CONT_CTM *, float> *MyDTW, ReadLM *LM, bool Reverse)
{
	float Best;
	vector<CONT_CTM *> *CurrentPath = new vector<CONT_CTM *>;
	Best=-INFINI;

	BacktrackBestPath(Current, LM, 0, (ofstream *) -1, CurrentPath, false, Reverse);

	AddPath(Current, CurrentPath, MyDTW, Best, Profondeur, Reverse);

	Current->Viterbi=Best;

	for_each(CurrentPath->begin(), CurrentPath->end(), MyDelete);

	delete CurrentPath;
}






float ComputeViterbiDecode(vector<NODE *> *Graph)
{
	int n;

	for (n = 0; n < Graph->size(); n++) ComputeBestPath((*Graph)[n]);

	if (n) return (*Graph)[n-1]->Viterbi;
	return -HUGE_VAL;
}


float BacktrackBestPath(NODE *Current, ReadLM *LM, float Normalize, ofstream *Out, vector<CONT_CTM *> *TheCTM, bool Verbose, bool Reverse)
{
	set<struct LINK *>::iterator it;

	float PreviousEnd;
	if (Out == NULL) Out = static_cast<ofstream*>(&cout);


	float Best=-HUGE_VAL;
	float Temp;
	LINK *BestLink = NULL;


	if (Reverse == false)
	{
		for (it = Current->BackLinks.begin(); it != Current->BackLinks.end(); it++)
		{
			NODE *PreviousNode = (*it)->From;

			if (PreviousNode->Viterbi > Best)
			{
				Best = PreviousNode->Viterbi;
				BestLink = (*it);
			} 
		}
	}
	else
	{
		for (it = Current->NextLinks.begin(); it != Current->NextLinks.end(); it++)
		{
			NODE *NextNode = (*it)->Target;

			if (NextNode->Viterbi > Best)
			{
				Best = NextNode->Viterbi;
				BestLink = (*it);
			} 
		}
	}

	bool Origin = false;


	if (Reverse == false)
	{
		if (BestLink && Current->BackLinks.size()) BacktrackBestPath(BestLink->From, LM, Normalize, Out, TheCTM, Verbose, Reverse);	
		else if (BestLink && Current->BackLinks.size() == 0) Origin = true;
	}
	else
	{
		if (BestLink && Current->NextLinks.size()) BacktrackBestPath(BestLink->Target, LM, Normalize, Out, TheCTM, Verbose, Reverse);	
		else if (BestLink && Current->NextLinks.size() == 0) Origin = true;
	}


	if (BestLink && BestLink->WordId > 0 && ((LM && BestLink->WordId < LM->GetMaxId()) || LM ==NULL) )
	{
		float posterior = exp (BestLink->From->Forward + BestLink->Weight(true) + BestLink->Target->Backward - Normalize);

		if (posterior > 1) posterior = 1;	

		if (TheCTM)
		{

			CONT_CTM *tmp = new CONT_CTM;
			tmp->Viterbi = BestLink->From->Viterbi;	
			tmp->Word = BestLink->WordId;	
			tmp->NodeFrom = BestLink->From->Number;
			tmp->NodeTarget = BestLink->Target->Number;

			if (!TheNoise || (TheNoise && TheNoise->find(tmp->Word) == TheNoise->end())) TheCTM->push_back(tmp);
			else delete tmp;
		}

		PreviousEnd = ceilf(BestLink->From->Time*100)/100;
		float t = (ceilf(BestLink->Target->Time*100) - ceilf(PreviousEnd*100) )/100.0;

		if (Out && Out != (ofstream *) -1) *Out <<Utterance<<" "<<"1"<<" "<<fixed<<setprecision(2)<<PreviousEnd<<" "<<setprecision(2)<<t<<" "<<IDToWord[BestLink->WordId]<<" "<<setprecision(5)<<posterior;

		if (Out && Out != (ofstream *) -1)
		{
			if (Verbose) *Out <<" ["<<BestLink->From->Number<<", "<<BestLink->Target->Number<<"] score : "<<BestLink->Target->Viterbi<<endl;
			else *Out<<endl;
		}
	}
	return PreviousEnd;
}


vector<NODE *> *ExpandGraph(vector<NODE *> *Graph, ReadLM *ML, bool SRILIKE=false)
{
	vector<NODE *> *ExpandedGraph = new vector<NODE *>;

	std::sort(Graph->begin(), Graph->end(), SortByTime);

	VERBOSE=true;
	for (int n=0; n < Graph->size(); n++)
	{
		if (VERBOSE) cerr <<"node "<<n<<" / "<< Graph->size()<<endl;
		if (VERBOSE) cerr <<"nb nodes in expanded : "<<ExpandedGraph->size()<<endl;
		if (VERBOSE) cerr << "nb links : bef : "<<(*Graph)[n]->BackLinks.size()<<", af: "<< (*Graph)[n]->NextLinks.size()<<endl;
		if (!SRILIKE) ExpandNode((*Graph)[n], ML, ExpandedGraph, MAX_GRAM);
		else ExpandNodeSRILike((*Graph)[n], ML, ExpandedGraph);

		DeleteNodeAndLinks((*Graph)[n]);
	}
	return ExpandedGraph;
}


vector<NODE *> *ReduceGraph(vector<NODE *> *Graph)
{
	vector<NODE *> *Copy;
	set<LINK *, LinkCompare> *NewNextLink;

	Copy = new vector<NODE *>;

	//std::sort(Graph->begin(), Graph->end(), SortByTime);

	my_unique_Nodes ( Graph->begin(), Graph->end(), Copy );


	if (VERBOSE) cout <<"number of nodes after reduce : "<<Copy->size()<<endl;

	for (int i = 0; i < Copy->size(); i++)
	{
		NewNextLink = new set<LINK *,LinkCompare >;

		//sort((*Copy)[i]->NextLinks.begin(), (*Copy)[i]->NextLinks.end(), SortByWordAndTarget);

		if ((*Copy)[i]->NextLinks.size())
		{
			my_unique_Links_Target ( (*Copy)[i]->NextLinks.begin(), (*Copy)[i]->NextLinks.end(), NewNextLink  );
			(*Copy)[i]->NextLinks = (*NewNextLink);
		}

		delete NewNextLink;
	}

	if (VERBOSE) cout <<"reduce finished !"<<endl;

	return Copy;
}





void WriteLattice(vector<NODE *> *Graph, char *FileName)
{
	int NbLinks=0;
	int NbNodes=0;

	vector<NODE *>::iterator it;

	std::sort(Graph->begin(), Graph->end(), SortByTime);

	for (it = Graph->begin(); it != Graph->end(); it++)
	{
		NbLinks += (*it)->NextLinks.size();
		(*it)->Number = NbNodes++;
	}

	ofstream FileExt (FileName, ios::out | ios::binary);

	FileExt <<"NODES="<<Graph->size()<<" LINKS="<<NbLinks<<endl;
	FileExt <<"# Nodes"<<endl;

	float Normalize = Graph->back()->Forward;

	for (it = Graph->begin(); it != Graph->end(); it++)
		FileExt<<"I="<<(*it)->Number<<"\t"<<"t="<<(*it)->Time<<"\t"<<"p="<<(*it)->Posterior<<endl;

	FileExt <<"# Links"<<endl;


	set<struct LINK *, LinkCompare>::iterator it2;

	int NbStates=0;

	for (it = Graph->begin(); it != Graph->end(); it++)
		for (it2 = (*it)->NextLinks.begin(); it2 != (*it)->NextLinks.end(); it2++)
		{
			//cerr <<"size : "<<(*it)->NextLinks.size()<<endl;
			//cerr<<"J="<<NbStates++<<"\tS="<<(*it2)->From->Number<<"\tE="<<(*it2)->Target->Number<<"\tW="<<IDToWord[(*it2)->WordId]<<"\ta="<<(*it2)->AcProbability<<"\tl="<<(*it2)->LmProbability<<"\tp="<< (*it2)->Posterior  <<endl;

			FileExt<<"J="<<NbStates++<<"\tS="<<(*it2)->From->Number<<"\tE="<<(*it2)->Target->Number<<"\tW="<<IDToWord[(*it2)->WordId]<<"\ta="<<(*it2)->AcProbability<<"\tl="<<(*it2)->LmProbability<<"\tp="<< (*it2)->Posterior  <<endl;
		}
	FileExt.close();
}


/*
 *
 * Utiliser getopt pour parser les arguments !!
 *
 *
 *
 *
 */
vector<NCNODE *> *ComputeMesh(vector<NODE *> *Graph)
{
	char *Temp=NULL;

	vector<NCNODE *> *Mesh;
	vector<NODE *> *Reduced;
	/*
	   for (int i = 0; i < 10000; i++)
	   for (int j = 0; j < 10000; j++)
	   EDIT_DIST[i][j] = -1;
	   */

	Temp = strdup("*DELETE*");

	WordsID[Temp] = 0;
	IDToWord[0] = Temp;

	if (VERBOSE) cout <<"sort nodes by time ..."<<endl;
	std::sort(Graph->begin(), Graph->end(), SortByTime);
	if (VERBOSE) cout <<"OK"<<endl;

	if (VERBOSE) cout <<"reduce the input graph"<<endl;
	Reduced = ReduceGraph(Graph);
	if (VERBOSE) cout <<"OK"<<endl;
	if (VERBOSE) cout <<"nb nodes in graph : "<<Graph->size()<<endl;
	if (VERBOSE) cout <<"nb links in graph : "<<LINK::NbLink<<endl;
	if (VERBOSE) cout <<"nb different words in graph : "<<WordsID.size()<<endl;


	Mesh = FastNC(Reduced);

	return Mesh;
}


struct ARGS_LM
{
	char *ArpaFile;
	char *Lexicon;

	char *BaseOutput;
	bool SkipUnk;
	int ReduceFactor;
};

void BuildLM(ARGS_LM *Args)
{
	int ReduceMem = Args->ReduceFactor;

	if (ReduceMem < 1) ReduceMem = 1;
	if (ReduceMem > 10) ReduceMem = 10;

	cerr <<"reduce the memory by "<< ReduceMem<<endl;


	class BuildLM LireArpa(Args->ArpaFile, Args->BaseOutput, ReduceMem);

	cerr <<"load arpalex"<<endl;

	if (LireArpa.ReadLMLex(Args->Lexicon) == false)
	{
		cerr <<"unable to load "<<Args->Lexicon<<endl;
		return;
	}

	if (Args->SkipUnk)
	{
		LireArpa.SetSkipUNK(true);
		cerr <<"skip the <UNK> word"<<endl;
	}
	else
	{
		LireArpa.SetSkipUNK(false);
		cerr <<"don't skip the <UNK> word"<<endl;
	}

	LireArpa.ConvertArpa();
}


void Help()
{
	cout <<"INPUT options"<<endl<<endl;
	cout <<"--read-lattice <foo.htk> : load the foo lattice"<<endl;
	cout <<"--read-mesh <foo.htk> : load the foo mesh lattice"<<endl;
	cout <<"--read-lm <basename_lm> : used language model"<<endl;
	cout <<"--read-ctm <foo.ctm> : load the foo ctm (corresponding to foo lattice...)"<<endl;
	cout <<endl<<"FUNCTIONALITIES"<<endl<<endl;
	cout <<"--ignore-case : ignore case during word comparison"<<endl;
	cout <<"--depth-dtw <number> : set the lookahead for viterbi with dtw (value > 3 is not a good idea)"<<endl;
	cout <<"--wnodetolink : move word to links (if they are on nodes)"<<endl;
	cout <<"--extend : extend the lattice by using the Language Model"<<endl;
	cout <<"--extend2 : extend the lattice by using the Language Model like sri toolkit (BUG : take a lot of RAM)"<<endl;
	cout <<"--remove-null : remove null nodes in lattice (BUG : do not use)"<<endl;
	cout <<"--link-to-node : move words to nodes (increase often the size of the graph)"<<endl;
	cout <<"--align-ctm-graph-dtw : align ctm file in corresponding lattice, allowing substitutions, insertions, deletions"<<endl;
	cout <<"--align-ctm-graph : align ctm (the path exist in the graph) file in corresponding lattice"<<endl;
	cout <<"--align-ctm-dtw <file.ctm> : align ctm file by using the corresponding lattice mesh (using dtw)"<<endl;
	cout <<"--align-ctm-time <file.ctm> : align ctm file by using the corresponding lattice mesh (using time infos)"<<endl;
	cout <<"--compute-posteriors : compute lattice posteriors using forward-backward algorithm"<<endl;
	cout <<"--compute-viterbi : search the best path in the lattice (printed in stdout by default)"<<endl;
	cout <<"--compute-mesh : compute a lattice sausage"<<endl;
	cout <<"--best-mesh : consensus decoding"<<endl;
	cout <<"--noise <file of ignored vocab> : vocabulary is not considered for alignments"<<endl;
	cout <<"--amscale, --acscale, --penalty, --pscaling : allow to force fudge for LM, AC and penalty; pscaling change the posterior distribution"<<endl;
	cout <<endl<<"OUTPUT options"<<endl;
	cout <<"--write-mesh <foo.mesh> : write the resulting mesh file"<<endl;
	cout <<"--write-lattice <foo.htk> : write the resulting lattice file"<<endl;
	cout <<"--write-aligned-ctm <foo.ctm> : write the resulting aligned ctm"<<endl;
	cout <<"--write-viterbi <foo.ctm> : write the viterbi result"<<endl;
	cout <<"--write-bestmesh <foo.ctm> : write the best mesh result"<<endl;
	cout <<endl<<"MISC"<<endl;
	//cout <<"--verbose : active verbose mode on stderr"<<endl;
	//cout <<"--debug : active a very high verbose mode (only for developer)"<<endl;	
	cout <<"--help print a boring message"<<endl;
	cout <<"note : you can add -verbose to --align-ctm-time, --align-ctm-dtw, --compute-posteriors options"<<endl;
	cout <<"If you want to use language model, you must compile an arpa model by using the buildlm tool"<<endl;
	cout <<"If you find (again) a bug, please contact benjamin.lecouteux@gmail.com"<<endl;
	cout <<endl<<"EXAMPLES"<<endl;
	cout <<"Align a ctm with a graph where words are on nodes : "<<endl;
	cout <<"./fastnc --read-lattice graph.slf --wnodetolink --read-ctm ref.ctm --align-ctm-graph-dtw --noise noise.txt"<<endl<<endl;
	cout <<"Expand a graph, generate posteriors, decode the graph, make CN, decode CN : "<<endl;
	cout <<"./fastnc --read-lm ML/ML_4g --read-lattice graph.slf --extend --compute-posteriors --compute-viterbi --write-viterbi result.res --write-lattice expanded.htk --lmscale 18 --compute-mesh --write-mesh sausage.wlat --best-mesh --write-bestmesh result2.resmesh"<<endl;

}




int ArgAnalyze(int argc, char *argv[])
{
	bool READ_LM=false;
	bool READ_CTM=false;
	bool READ_NOISE=false;
	bool READ_HTK=false;
	bool READ_MESH=false;

	bool WRITE_MESH=false;
	bool WRITE_HTK=false;
	bool WRITE_ALIGNED_CTM=false;	
	bool WRITE_CTM=false;	
	bool WRITE_VITERBI=false;	

	bool VERBOSE_CTM=false;

	bool EXTEND=false;
	bool EXTEND2=false;
	bool COMPUTE_POSTERIORS=false;
	bool COMPUTE_MESH=false;

	bool ALIGN_CTM_DTW=false;
	bool ALIGN_CTM_GRAPH=false;
	bool ALIGN_CTM_GRAPH_DTW=false;
	bool ALIGN_CTM_TIME=false;
	bool ALIGN_CTM_DTW_VERBOSE=false;
	bool ALIGN_CTM_TIME_VERBOSE=false;
	bool COMPUTE_VITERBI=false;
	bool REMOVE_NULL=false;

	bool DTW_VERBOSE=false;
	bool AC_FUDGE=false;
	bool ML_FUDGE=false;
	bool PENALTY=false;
	bool PSCALING=false;

	bool NODE_TO_LINK=false;
	bool LINK_TO_NODE=false;

	IGNORE_CASE=false;

	int c;
	int digit_optind = 0;

	int CurrentOption;
	char *Fic;
	size_t FileSize;
	ReadLM *LM = NULL;
	char *FileInHTK=NULL;
	char *FileOutHTK=NULL;

	char *FileOutMesh=NULL;
	char *FileInMesh=NULL;

	char *FileNoise=NULL;
	char *FileInCTM=NULL;
	char *FileOutCTMDTW=NULL;
	char *FileOutCTMTime=NULL;

	char *FileLM=NULL;
	ofstream *ViterbiCTM=NULL;

	float AcFudge, MLFudge, PScaling, Penalty;




	while (1) {
		int this_option_optind = optind ? optind : 1;
		int option_index = 0;

		static struct option long_options[] = {
			{"extend", 0, 0, 0},
			{"extend2", 0, 0, 0},
			{"align-ctm-dtw", 0, 0, 0},
			{"align-ctm-time", 0, 0, 0},
			{"align-ctm-graph", 0, 0, 0},
			{"align-ctm-graph-dtw", 0, 0, 0},
			{"align-ctm-dtw-verbose", 0, 0, 0},
			{"align-ctm-time-verbose", 0, 0, 0},
			{"compute-posteriors-verbose", 0, 0, 0},
			{"compute-posteriors", 0, 0, 0},
			{"compute-viterbi", 0, 0, 0},
			{"compute-mesh", 0, 0, 0},
			{"wnodetolink", 0, 0, 0},
			{"noise", 1, 0, 0},
			{"read-lattice", 1, 0, 0},
			{"read-lm",1, 0, 0},
			{"read-mesh", 1, 0, 0},	
			{"read-ctm", 1, 0, 0},
			{"depth-dtw", 1, 0, 0},
			{"write-mesh", 1, 0, 0},
			{"write-lattice", 1, 0, 0},
			{"write-aligned-ctm", 1, 0, 0},
			{"write-viterbi", 1, 0, 0},
			{"link-to-node", 0, 0, 0},
			{"remove-null", 0, 0, 0},
			{"link-to-node", 0, 0, 0},
			{"penalty", 1, 0, 0},
			{"lmscale", 1, 0, 0},
			{"acscale", 1, 0, 0},
			{"pscaling",1,0,0},
			{"help", 0, 0, 0},
			{"verbose", 0, 0, 0},
			{"debug", 0, 0, 0},
			{"ignore-case", 0, 0, 0},
			{0, 0, 0, 0},
		}; 


		c = getopt_long(argc, argv, /*"abc:d:012"*/"", long_options, &option_index);
		if (c == -1)
			break;

		char *CurrentOption;

		switch (c) {
			case 0:
				CurrentOption = (char *)  long_options[option_index].name;

				if (!strcmp(CurrentOption, "ignore-case"))
				{
					cerr <<"ignore-case for comparaison : "<<optarg<<endl;
					IGNORE_CASE=true;
				}
				if (!strcmp(CurrentOption, "acscale"))
				{
					cerr <<"acscale : "<<optarg<<endl;
					AcFudge = atof(optarg);
					AC_FUDGE=true;
				}
				if (!strcmp(CurrentOption, "lmscale"))
				{
					cerr <<"lmscale : "<<optarg<<endl;
					MLFudge = atof(optarg);
					ML_FUDGE=true;
				}
				if (!strcmp(CurrentOption, "link-to-node"))
				{
					cerr <<"link-to-node : "<<endl;
					LINK_TO_NODE=true;
				}
				if (!strcmp(CurrentOption, "penalty"))
				{
					cerr <<"lmscale : "<<optarg<<endl;
					Penalty = atof(optarg);
					PENALTY=true;
				}
				if (!strcmp(CurrentOption, "pscaling"))
				{
					cerr <<"posterior scale : "<<optarg<<endl;
					PScaling = atof(optarg);
					PSCALING=true;
				}
				if (!strcmp(CurrentOption, "depth-dtw"))
				{
					cerr <<"depth for dtw : "<<optarg<<endl;
					Profondeur = atof(optarg);
				}
				if (!strcmp(CurrentOption, "extend"))
				{
					cerr <<"extend lattice"<<endl;
					EXTEND = true;
				}

				if (!strcmp(CurrentOption, "extend2"))
				{
					cerr <<"extend lattice based on histories"<<endl;
					EXTEND2 = true;
				}
				else if (!strcmp(CurrentOption, "align-ctm-graph"))
				{
					cerr <<"Align ctm with graph"<<endl;
					ALIGN_CTM_GRAPH = true;
				}
				else if (!strcmp(CurrentOption, "align-ctm-graph-dtw"))
				{
					cerr <<"Align ctm (with dtw) with graph"<<endl;
					ALIGN_CTM_GRAPH_DTW = true;
				}
				else if (!strcmp(CurrentOption, "align-ctm-dtw"))
				{
					cerr <<"Align ctm with dtw"<<endl;
					ALIGN_CTM_DTW = true;
				}
				else if (!strcmp(CurrentOption, "align-ctm-time"))
				{
					cerr <<"Align ctm with time"<<endl;
					ALIGN_CTM_TIME = true;
				}
				else if (!strcmp(CurrentOption, "align-ctm-dtw-verbose"))
				{
					cerr <<"Align ctm with dtw (verbose)"<<endl;
					ALIGN_CTM_DTW_VERBOSE = true;
				}
				else if (!strcmp(CurrentOption, "align-ctm-time-verbose"))
				{
					cerr <<"Align ctm with time (verbose)"<<endl;
					ALIGN_CTM_TIME_VERBOSE = true;
				}
				else if (!strcmp(CurrentOption, "compute-posteriors"))
				{
					cerr <<"compute posteriors"<<endl;
					COMPUTE_POSTERIORS = true;
				}
				else if (!strcmp(CurrentOption, "compute-viterbi"))
				{
					cerr <<"compute viterbi"<<endl;
					COMPUTE_VITERBI = true;
				}

				else if (!strcmp(CurrentOption, "compute-mesh"))
				{
					cerr <<"compute mesh"<<endl;
					COMPUTE_MESH = true;
				}

				else if (!strcmp(CurrentOption, "read-lattice"))
				{
					cerr <<"read lattice : "<<optarg<<endl;
					FileInHTK = optarg;
					READ_HTK = true;
				}
				else if (!strcmp(CurrentOption, "read-lm"))
				{
					cerr <<"read lm : "<<optarg<<endl;
					FileLM = optarg;
					READ_LM = true;
				}

				else if (!strcmp(CurrentOption, "read-mesh"))
				{
					cerr <<"read mesh : "<<optarg<<endl;
					FileInMesh = optarg;
					READ_MESH = true;
				}

				else if (!strcmp(CurrentOption, "read-ctm"))
				{
					cerr <<"read ctm"<<endl;
					FileInCTM = optarg;
					READ_CTM = true;
				}

				else if (!strcmp(CurrentOption, "noise"))
				{
					cerr <<"read noise vocabulary"<<endl;
					FileNoise = optarg;
					READ_NOISE = true;
				}


				else if (!strcmp(CurrentOption, "write-lattice"))
				{
					cerr <<"write lattice"<<endl;
					FileOutHTK = optarg;
					WRITE_HTK = true;
				}
				else if (!strcmp(CurrentOption, "write-aligned-ctm"))
				{
					cerr <<"write aligned ctm"<<endl;
					WRITE_ALIGNED_CTM = true;
				}

				else if (!strcmp(CurrentOption, "write-mesh"))
				{
					cerr <<"write mesh"<<endl;
					FileOutMesh = optarg;
					WRITE_MESH = true;
				}
				if (!strcmp(CurrentOption, "remove-null"))
				{
					cerr <<"remove nulls"<<endl;
					REMOVE_NULL = true;
				}


				else if (!strcmp(CurrentOption, "help"))
				{
					cerr <<"Help"<<endl;
					Help();
				}


				else if (!strcmp(CurrentOption, "write-ctm"))
				{
					cerr <<"write ctm"<<endl;
					WRITE_CTM = true;
				}
				else if (!strcmp(CurrentOption, "wnodetolink"))
				{
					cerr <<"convert word node to link"<<endl;
					NODE_TO_LINK = true;
				}
				else if (!strcmp(CurrentOption, "write-viterbi"))
				{
					cerr <<"write viterbi"<<endl;

					ViterbiCTM = new ofstream (optarg, ios::out | ios::binary);

					if (ViterbiCTM->is_open() == false)
					{
						delete ViterbiCTM;
						ViterbiCTM = NULL;
						cerr <<"unable to open "<<optarg<<endl;
						exit(0);
					}
					WRITE_VITERBI = true;
				}

				fprintf(stderr, "option %s", long_options[option_index].name);
				if (optarg)
					fprintf(stderr, " with arg %s", optarg);
				fprintf(stderr, "\n");
				break;

			default:
			case '?':
				cerr <<"Option error... abort"<<endl;
				exit (0);
				break;
		}
	}

	if (optind < argc) {
		printf("non-option ARGV-elements: ");
		while (optind < argc)
			printf("%s ", argv[optind++]);
		printf("\n");
	}



	vector<NODE *> *InputGraph=NULL;
	vector<NCNODE *> *Mesh=NULL;
	vector<CONT_CTM *> *TheCTM=NULL;

	if ( READ_LM )
	{
		if (VERBOSE) cerr <<"load LM"<<endl;		
		if (FileLM) LM = new ReadLM((char *)"", FileLM);

		endS=LM->GetWordId((char *)"</s>");
		debS=LM->GetWordId((char *)"<s>");
	}

	if (READ_CTM)
	{
		cerr <<"load "<<FileInCTM<<endl;
		TheCTM = LoadCTM(FileInCTM, LM);
	}

	if (READ_MESH)
	{


		Fic = ReadHTK(FileInMesh, FileSize);
		InputGraph = LoadMesh(Fic, LM);

		AddWord((char *) "*IGNORE*", LM);

		cerr <<"nb nodes in mesh : "<<InputGraph->size()<<endl;


		InputGraph = ExploseMesh(InputGraph);


		cerr <<"nb nodes in mesh after transformation : "<<InputGraph->size()<<endl;

		//Mesh = ComputeMesh(InputGraph);
		munmap(Fic, FileSize);
	}

	if (READ_HTK)
	{
		if (!LM) cerr <<"WARNING : Language Model is not available !"<<endl;
		cerr <<"read lattice : "<<FileInHTK<<endl;
		Fic = ReadHTK(FileInHTK, FileSize);
		InputGraph = LoadGraph(Fic, LM);

		AddVirtualTimeToGraph ((*InputGraph)[0], 0);

		std::sort(InputGraph->begin(), InputGraph->end(), SortByTime);
		munmap(Fic, FileSize);
		cerr <<"OK"<<endl;
	}

	if (READ_NOISE)
	{
		cerr <<"load "<<FileNoise<<endl;
		TheNoise = LoadNoise(FileNoise, LM);
	}

	if (LINK_TO_NODE)
	{
		InputGraph = LinkToNodeGraph(InputGraph, LM);
	}

	if (NODE_TO_LINK)
	{

		PropagateNodeWordsToLink(InputGraph);
	}

	if (ML_FUDGE) LINK::MLFudge = MLFudge;
	if (AC_FUDGE) LINK::AcFudge = AcFudge;
	if (PSCALING) LINK::PScaling = PScaling;
	if (PENALTY)  LINK::Penalty = Penalty;


	if (REMOVE_NULL)
	{
		InputGraph = RemoveNullAndPause(InputGraph, LM);
	}


	/*if (!InputGraph) 
	  {
	  cerr <<"ERROR : input graph not available, abort !"<<endl;
	  return 0;
	  }*/

	if (EXTEND || EXTEND2)
	{
		if (!LM) cerr <<"WARNING : Language Model is not available !"<<endl;
		vector<NODE *> *ExtendedGraph;
		//if (EXTEND2) 
		//	InputGraph = LinkToNodeGraph(InputGraph, LM);
		ExtendedGraph = ExpandGraph(InputGraph, LM, EXTEND2);


		//ExtendedGraph = ReduceGraph2(ExtendedGraph);

		delete InputGraph;
		InputGraph=ExtendedGraph;
	}	


	if (COMPUTE_POSTERIORS)
	{
		ComputePosteriors(InputGraph);
	}

	if (COMPUTE_VITERBI)
	{
		if (COMPUTE_POSTERIORS == false) ComputeViterbiDecode(InputGraph);
		BacktrackBestPath((*InputGraph)[InputGraph->size()-1], LM, InputGraph->back()->Forward, ViterbiCTM);
	}

	if (WRITE_HTK)
	{
		if (FileOutHTK) WriteLattice(InputGraph, FileOutHTK);
	}

	if (COMPUTE_MESH)
	{
		Mesh = ComputeMesh(InputGraph);

		BestMeshPath(Mesh, LM, NULL);
	}

	if (VERBOSE_CTM)
	{
		DTW_VERBOSE = true;
	}
	else DTW_VERBOSE = false;


	if (ALIGN_CTM_GRAPH)
	{
		if (TheCTM == NULL) 
		{
			cerr <<"No ctm to align"<<endl;
			exit(EXIT_SUCCESS);
		}
		vector<LINK *> CurrentPath;
		vector<LINK *> BestPath;
		float Best=-HUGE_VAL;


		int MaxID=10000000;

		if (LM) MaxID=LM->GetMaxId();

		BackTrackBestHyp((*InputGraph)[0], &CurrentPath, &BestPath, TheCTM, 0, 0, Best, MaxID);

		cerr <<"Best path size : "<<BestPath.size()<<endl;

		for (int i = 0; i < BestPath.size(); i++)
		{
			cout <<Utterance<<" "<<"1"<<" "<<BestPath[i]->From->Time<<" "<<int((BestPath[i]->Target->Time-BestPath[i]->From->Time)*100)/100.0<<" "<<IDToWord[BestPath[i]->WordId]<<" "<<BestPath[i]->Posterior<<endl;
		}
	}


	if (ALIGN_CTM_GRAPH_DTW)
	{
		bool Reverse=false;

		if (TheCTM == NULL) 
		{
			cerr <<"No ctm to align"<<endl;
			exit(EXIT_SUCCESS);
		}
		int MaxID=10000000;
		if (LM) MaxID=LM->GetMaxId();

		cerr <<"ComputeViterbiDecodeAlignWER"<<endl;

		ComputeViterbiDecodeAlignWER(InputGraph, TheCTM, NULL, Reverse);


		//ComputeAllPath((*InputGraph)[0], TheCTM);



		vector<CONT_CTM *> CurrentPath;
		cerr <<"BacktrackBestPath"<<endl;
		//BacktrackBestPath((*InputGraph)[InputGraph->size()-1], LM, 0, NULL);

		if (Reverse == false)
			BacktrackBestPath((*InputGraph)[InputGraph->size()-1], LM, 0, NULL, &CurrentPath, true, Reverse);
		else 	BacktrackBestPath((*InputGraph)[0], LM, 0, NULL, &CurrentPath, true, Reverse);

		cerr <<"size path : "<<CurrentPath.size()<<endl;

		class AlignDTW<CONT_CTM * , CONT_CTM *, float> *MyDTW = new AlignDTW<CONT_CTM * , CONT_CTM *, float>(1000, *TheCTM, CompWER, PrintAlignWER, (float) 5, (float) 6,  (float) 6);

		MyDTW->InitDTW();

		MyDTW->CalculerCheminDTW(CurrentPath, 0, 0);

		MyDTW->BackTrack(CurrentPath);
		MyDTW->SetPrintVerbose(true);
		//
		int ins, sub, del, ok;


		MyDTW->PrintBestAlign(CurrentPath, &ins, &sub, &del, &ok);

		cout <<endl<<"ins: "<<ins<<", sub: "<<sub<<", del: "<<del<<", ok:"<<ok<<endl<<endl;


		cout <<"Lattice Hyp : ";

		for (int i = 0; i < CurrentPath.size(); i++)
		{
			//if (strcmp(IDToWord[CurrentPath[i]->Word], "!NULL") != 0)
			//{
				cout<< IDToWord[CurrentPath[i]->Word]<< " ";
			//}
		}
		cout <<endl;



		cout <<"Merged Hyp  : ";

		for (int i = 0; i < Merged.size(); i++)
		{
			cout<< IDToWord[Merged[i]]<< " ";
		}
		cout <<endl;

		Merged.clear();



		cout <<"number of words in graph hypothesis: "<<CurrentPath.size()<<endl;
		cout <<"number of words in refrence: "<<TheCTM->size()<<endl;
		cout <<"WER: "<<fixed<<setprecision(2)<<(float)(ins+del+sub)/(float)TheCTM->size()*100<<" %"<<endl;

		//cout <<"after backtrack : "<<MAXVITERBI<<endl;


		//BacktrackBestPath((*InputGraph)[InputGraph->size()-1], LM, 0, NULL, &CurrentPath);
	}

	if (ALIGN_CTM_TIME)
	{
		if (TheCTM == NULL) 
		{
			cerr <<"No ctm to align"<<endl;
			exit(EXIT_SUCCESS);
		}
		ofstream FileCTM (FileOutCTMTime, ios::out | ios::binary);
		if (FileCTM.is_open()) AlignCTM(TheCTM, Mesh, &FileCTM);
		else AlignCTM(TheCTM, Mesh, NULL);
	}

	if (ALIGN_CTM_DTW)
	{
		if (TheCTM == NULL) 
		{
			cerr <<"No ctm to align"<<endl;
			exit(EXIT_SUCCESS);
		}
		ofstream FileCTM (FileOutCTMDTW, ios::out | ios::binary);
		if (FileCTM.is_open()) AlignCTMWithDTW(TheCTM, Mesh, DTW_VERBOSE, &FileCTM);
		else AlignCTMWithDTW(TheCTM, Mesh, DTW_VERBOSE, NULL);
	}



	if (WRITE_MESH)
	{

		ofstream FileMesh (FileOutMesh, ios::out | ios::binary);

		if (FileMesh.is_open())
		{	
			FileMesh << "name "<<FileInHTK<<endl;
			FileMesh << "numaligns " << Mesh->size()-1<<endl;
			FileMesh << "posterior 1"<<endl;

			for (int i = 0; i < Mesh->size()-1; i++)
			{
				FileMesh << "align "<<i<<" ";

				sort((*Mesh)[i]->MeshLinks->begin(), (*Mesh)[i]->MeshLinks->end(), SortByPost);

				for (int j = 0; j < (*Mesh)[i]->MeshLinks->size(); j++)
				{
					FileMesh<< IDToWord[(*(*Mesh)[i]->MeshLinks)[j]->WordId]<<" "<<(*(*Mesh)[i]->MeshLinks)[j]->Posterior<<" ";
				}
				FileMesh <<endl;
			}
		}
	}




	exit(EXIT_SUCCESS);
}



int main(int argc, char **argv)
{	
	Utterance=new char[512];

	strcpy (Utterance, "nothing");
	cerr <<"fastnc version 7.3 -- Lecouteux Benjamin"<<endl;
	cerr <<"--help for help"<<endl;

	ArgAnalyze(argc, argv);
}



set<int> *LoadNoise(char *noiseFile, ReadLM *LM)
{
	char *Line;
	int i;
	int Sizenoise;
	char *Buffer;
	char *Cursor;
	FILE *Fnoise;

	char *Word;
	int WordId;

	bool Continue = true;

	set<int> *Retour;

	Retour = new set<int>;

	if (VERBOSE) cerr <<"open "<<noiseFile<<endl;

	Fnoise = fopen(noiseFile, "r");

	if (Fnoise)
	{
		fseek(Fnoise, 0, SEEK_END);
		Sizenoise = ftell(Fnoise);
		fseek(Fnoise, 0, SEEK_SET);

		if (VERBOSE) cerr<<"taille noise : "<<Sizenoise<<endl;

		Buffer = new char[Sizenoise+1];



		fread(Buffer, Sizenoise, 1, Fnoise);

		Buffer[Sizenoise] = '\0';

		Cursor = NULL;

		bool Origin=true;

		do
		{
			Line = ForEach(Buffer, Cursor, "\n");

			if (Line)
			{
				Word = strdup(Line);
				WordId = AddWord(Line, LM);
				Retour->insert(WordId);

				cerr <<"word "<<Line<<" ["<<WordId<<"] considered as noise"<<endl;

				delete [] Line;
			}
			else Continue = false;
		}
		while(Continue);
	}
	else perror("Wrong Filename");

	return Retour;
}



vector<CONT_CTM *> *LoadCTM(char *CTMFile, ReadLM *LM)
{
	char *Line;
	char *Token;
	int i;
	int SizeCtm;
	char *Buffer;
	char *Cursor;
	char *Cursor2;
	FILE *FCTM;

	float TimeStart;
	float Duration;
	char *Word;

	bool Continue = true;

	vector<CONT_CTM *> *Retour;

	Retour = new vector<CONT_CTM *>;
	if (VERBOSE) cerr <<"open "<<CTMFile<<endl;
	FCTM = fopen(CTMFile, "r");

	if (FCTM)
	{
		fseek(FCTM, 0, SEEK_END);
		SizeCtm = ftell(FCTM);
		fseek(FCTM, 0, SEEK_SET);

		if (VERBOSE) cerr<<"taille ctm : "<<SizeCtm<<endl;

		Buffer = new char[SizeCtm+1];



		fread(Buffer, SizeCtm, 1, FCTM);

		Buffer[SizeCtm] = '\0';

		Cursor = NULL;

		bool Origin=true;
		float TimeBegin;

		do
		{
			Line = ForEach(Buffer, Cursor, "\n");


			//cerr<<"Line : "<<Line<<" - "<<(int)Cursor[0] <<" -> "<<Cursor[0] <<endl;

			if (Line)
			{
				CONT_CTM *Tmp = new CONT_CTM;

				Tmp->Line = strdup(Line);

				Cursor2 = NULL;

				for (i = 0; i < 5; i++)
				{
					Token = ForEach(Line, Cursor2, " \t\n");

					//cout <<"--->"<<Token<<endl;

					switch(i)
					{
						case 0:break;
						case 1:break;
						case 2:Tmp->Start = TimeStart = atof(Token);

						       if (Origin == true)
						       {
							       TimeBegin = TimeStart;
							       Origin = false;
						       }
						       Tmp->Origin = TimeBegin;

						       break;
						case 3:Tmp->Duration = Duration = atof(Token);
						       break;
						case 4:	Word = strdup(Token);
							Tmp->Word = AddWord(Token, LM);
							Retour->push_back(Tmp);
					}

					delete [] Token;
				}


				delete [] Line;

			}
			else Continue = false;

		}
		while(Continue);
	}
	else perror("Wrong Filename");

	return Retour;
}


float CompWER(CONT_CTM *a, CONT_CTM *b)
{
	//if (TheNoise && (TheNoise->find(a->Word) != TheNoise->end() || TheNoise->find(b->Word) != TheNoise->end())) return -1;
	//9.9

	if (IGNORE_CASE == true)
	{
		if (strcasecmp(IDToWord[a->Word], IDToWord[b->Word]) == 0) 
		{
			return 9.9;
		}
	}
	else 
	{	if (a->Word == b->Word) 
		{
			return 9.9;
		}
	}
	return -1;
}




float Comp(NCNODE *a, CONT_CTM *b)
{
	for (int i = 0; i < a->MeshLinks->size(); i++)
		//if (((*(a->MeshLinks))[i])->WordId == b->Word) return 5+((*(a->MeshLinks))[i])->Posterior*10000;
		if (((*(a->MeshLinks))[i])->WordId == b->Word) return 5+((*(a->MeshLinks))[i])->Posterior;

	//for (int i = 0; i < a->MeshLinks->size(); i++)
	//	if (((*(a->MeshLinks))[i])->WordId == 0) return /*((*(a->MeshLinks))[i])->Posterior*/-0.01;

	return -5;

}


bool PrintAlignWER(CONT_CTM *Ref, CONT_CTM *Hyp, ofstream *Out)
{
	bool Nan = true;
	bool Ret=false;

	if (Out == NULL) Out = static_cast<ofstream*>(&cout);

	if (Ref && Hyp)
	{

		*Out << IDToWord[Ref->Word]<<"\t";
		*Out << IDToWord[Hyp->Word]<<"\t["<<Hyp->NodeFrom<<", "<<Hyp->NodeTarget<<"]"<<" DTW score : "<<Hyp->Viterbi;
		if (strcasecmp(IDToWord[Ref->Word], IDToWord[Hyp->Word]) == 0)
			Merged.push_back(Hyp->Word);
		else Merged.push_back(Ref->Word);
		Ret = true;
	}
	else if (Hyp)
	{
		*Out << "\t";
		*Out << IDToWord[Hyp->Word]<<  "\t["<<Hyp->NodeFrom<<", "<<Hyp->NodeTarget<<"]"<<" "<<"DTW score : "<<Hyp->Viterbi;
		Ret = true;
		//Merged.push_back(Ref->Word);
	}
	else if (Ref)
	{
		*Out << IDToWord[Ref->Word] <<"\t";
		Merged.push_back(Ref->Word);
	}

	return Ret;
}



bool Print(NCNODE *Ref, CONT_CTM *Hyp, ofstream *Out)
{
	bool Nan = true;
	bool Ret=false;

	if (Out == NULL) Out = static_cast<ofstream*>(&cout);

	if (Ref && Hyp)
	{

		*Out << IDToWord[Hyp->Word]<<"\t";

		//cout <<Hyp->Line<<"\t";

		double mean=0;
		double var=0;
		double EcartType=0;
		double min=HUGE_VAL, max=-HUGE_VAL;


		for (int i = 0; i < Ref->MeshLinks->size(); i++)
		{
			if (((*(Ref->MeshLinks))[i])->Posterior > max) max = ((*(Ref->MeshLinks))[i])->Posterior;
			if (((*(Ref->MeshLinks))[i])->Posterior < min) min = ((*(Ref->MeshLinks))[i])->Posterior;
			mean+=((*(Ref->MeshLinks))[i])->Posterior;
		}
		mean/=Ref->MeshLinks->size();



		for (int i = 0; i < Ref->MeshLinks->size(); i++)
			var+=(((*(Ref->MeshLinks))[i])->Posterior-mean)*(((*(Ref->MeshLinks))[i])->Posterior-mean);


		EcartType = sqrt(var);



		for (int i = 0; i < Ref->MeshLinks->size() && Nan == true; i++)
		{
			if (((*(Ref->MeshLinks))[i])->WordId == Hyp->Word) 
			{
				int Trame = roundf(Hyp->Start*100.0-Hyp->Origin*100.0);

				*Out <<((*(Ref->MeshLinks))[i])->Posterior <<" ( time="<<Trame<<" nodes="<<Ref->MeshLinks->size()<<" min="<<min<<" max="<<max<<" mean="<<mean<<" var="<<var<<" svar="<<EcartType<<" )";
				//cout <<((*(Ref->MeshLinks))[i])->Posterior;
				Nan = false;
			}
		}
		if (Nan == true) *Out <<"1.0";

		Ret = true;
	}
	else if (Hyp)
	{
		*Out << IDToWord[Hyp->Word]<<"\t1.0";
		//cout<<Hyp->Line<<"\t1.0";
		Ret = true;
	}

	return Ret;
}


int AlignCTMWithDTW(vector<CONT_CTM *> *TheCTM, vector<NCNODE *> *Mesh, bool DTW_VERBOSE, ofstream *Out)
{
	class AlignDTW<NCNODE *, CONT_CTM *, float> MyDTW(TheCTM->size(), *Mesh, Comp, Print, (float) 5, (float) 6,  (float) 6);
	if (Out == NULL) Out = static_cast<ofstream*>(&cout);

	MyDTW.InitDTW();
	MyDTW.SetOut(Out);
	MyDTW.CalculerCheminDTW(*TheCTM, 0, 0);
	MyDTW.BackTrack(*TheCTM);
	MyDTW.SetPrintVerbose(DTW_VERBOSE);
	MyDTW.PrintBestAlign(*TheCTM);


	return 1;
}


int AlignCTM(vector<CONT_CTM *> *TheCTM, vector<NCNODE *> *Mesh, ofstream *Out)
{
	int i;
	//vector<CONT_CTM *> *TheCTM;

	if (Out == NULL) Out= static_cast<ofstream*> (&cout);
	//TheCTM = LoadCTM(CTMFile);

	//cout <<((*(Ref->MeshLinks))[i])->Posterior <<" (nodes="<<Ref->MeshLinks->size()<<", min="<<min<<", max="<<max<<", mean="<<mean<<", var="<<var<<", svar="<<EcartType<<")";
	for (i = 0; i < TheCTM->size(); i++)
	{
		*Out <<(*TheCTM)[i]->Line<<"\t";

		float res = FoundInMesh((*TheCTM)[i]->Word, (*TheCTM)[i]->Start, (*TheCTM)[i]->Duration, Mesh);
		if (res != -1) *Out <<res<<endl;
		else *Out<<"1.0"<<endl;
	}
	for (i = 0; i < TheCTM->size(); i++)
		free((*TheCTM)[i]->Line);

	for (i = 0; i < TheCTM->size(); i++)
		delete (*TheCTM)[i];

	delete TheCTM;

	return 1;
}


float FoundInMesh(int Word, float Start, float Duration, vector<NCNODE *> *Mesh)
{
	//cout <<"recherche du mot : "<<Word<<" start : "<<Start <<endl;
	for (int i = 0; i < Mesh->size()-1; i++)
	{
		for (int j = 0; j < (*Mesh)[i]->MeshLinks->size(); j++)
		{

			for (int k = 0; k < (*(*Mesh)[i]->MeshLinks)[j]->TimeLinks.size(); k++)
			{

				if(Word == (*(*Mesh)[i]->MeshLinks)[j]->WordId && fabs((*(*Mesh)[i]->MeshLinks)[j]->TimeLinks[k]->Start-Start) <= 0.02 && fabs((*(*Mesh)[i]->MeshLinks)[j]->TimeLinks[k]->Duration - Duration) <= 0.02)
				{
					//cout <<IDToWord[Word]<<" - "<<(*(*Mesh)[i]->MeshLinks)[j]->Posterior<<endl;
					//cout <<"align : "<< IDToWord[Word] <<" d : "<<Duration<<" - "<< (*(*Mesh)[i]->MeshLinks)[j]->TimeLinks[k]->Duration <<endl;
					return (*(*Mesh)[i]->MeshLinks)[j]->Posterior;
				}

			}
		}
	}
	return -1;
	//cout <<IDToWord[Word]<<" - "<<"not found !!"<<endl;
}


int AddWord(char *Token, ReadLM *LM)
{

	int WID;
	char *Word = strdup(Token);

	if (WordsID.count(Word))
	{
		WID = WordsID[Word];
	}
	else
	{
		if (LM) Ids = LM->GetWordId(Word);


		if (LM && Ids < 0) 
		{
			cerr <<"WARNING : unknow word "<<Word<< " -> mapped in null transition"<<endl;
			IdsUNK++;
			Ids = LM->GetMaxId()+IdsUNK;
			IDToWord[Ids] = Word;
		}
		else	IDToWord[Ids] = Word;

		WordsID[Word] = Ids;
		WID = Ids;

		if (LM) Ids = LM->GetMaxId()+IdsUNK;
		else Ids++;
	}


	return WID;
}



void ParseLink(char *Line, vector<NODE *> *Graphe, ReadLM *LM=NULL)
{
	char *Token;
	char *Cursor=NULL;
	bool Again = true;

	int StartNode = 0;
	int EndNode = 0;
	float Posterior = 1;
	char *Word;
	int WID;
	float LmProb, AcProb;

	LmProb = AcProb = 0;

	while (Again)
	{
		Token = ForEach(Line, Cursor, " \t#");

		if (Token)
		{
			if (strstr(Token, "p="))
			{
				Posterior = atof(&Token[2]);
			}

			if (strstr(Token, "a="))
			{
				AcProb = atof(&Token[2]);
			}

			if (strstr(Token, "l="))
			{
				LmProb = atof(&Token[2]);
			}
			else if (strstr(Token, "S="))
			{
				StartNode = atoi(&Token[2]);
			}

			else if (strstr(Token, "E="))
			{
				EndNode = atoi(&Token[2]);
			}

			else if (strstr(Token, "W=")) WID = AddWord(&Token[2], LM);

			delete [] Token;
		}
		else Again = false;
	}


	//if ((*Graphe)[StartNode]->Time != (*Graphe)[EndNode]->Time)
	//{
	//cerr <<"link node "<<(*Graphe)[StartNode]->Number<<" with "<<(*Graphe)[EndNode]->Number<<" -> "<<WID<<endl;
	if (StartNode >= 0 && EndNode >= 0)
	{

		if ((*Graphe)[StartNode]->Time >= (*Graphe)[EndNode]->Time && (*Graphe)[EndNode]->Time != -1) 
		{
			cerr <<"Possibility of corrupt graph : link across nodes "<< StartNode<<" and "<< EndNode <<endl;
			cerr <<"start link time >= end link time : "<< (*Graphe)[StartNode]->Time<<", "<<(*Graphe)[EndNode]->Time<<endl;
		}
		new LINK((*Graphe)[StartNode], (*Graphe)[EndNode], Posterior, WID, LmProb, AcProb);
	}
	else cerr <<"Line ignored because of num nodes < 0"<<endl;
	//}
	//else cerr << "-->link node "<<(*Graphe)[StartNode]->Number<<" with "<<(*Graphe)[EndNode]->Number<<" -> "<<WID<<endl;
}

NODE *ParseNode(char *Line, ReadLM *LM=NULL)
{
	char *Token;
	char *Cursor=NULL;
	bool Again = true;
	int Number=0;
	int WID=-1;

	float Posterior = 1;
	float Time = -1;
	NODE *NewNode;

	while (Again)
	{
		Token = ForEach(Line, Cursor, " \t#");

		if (Token)
		{
			if (strstr(Token, "I="))
			{
				Number = atoi(&Token[2]);
			}

			if (strstr(Token, "p="))
			{
				Posterior = atof(&Token[2]);
			}

			if (strstr(Token, "t="))
			{
				Time = atof(&Token[2]);
			}

			if (strstr(Token, "W=")) WID = AddWord(&Token[2], LM);

			delete [] Token;
		}
		else Again = false;
	}

	NewNode=new NODE(Time, Posterior, Number);

	if (WID >= 0) NewNode->WordId = WID;

	return NewNode;
}


vector<NODE *> *ExploseMesh(vector<NODE *> *Mesh)
{
	vector<NODE *> *Explosed;


	NODE *Previous=NULL;
	NODE *Next=NULL;
	NODE *Empty=NULL;
	Explosed = new vector<NODE *>;

	vector<NODE *>::iterator it;

	bool First=true;

	set<struct LINK *>::iterator itlink;

	for (it = Mesh->begin(); it != Mesh->end(); it++)
	{
		if (First == false)
		{
			Next = (*it)->CloneDup(false);

			for (itlink = (*it)->BackLinks.begin(); itlink != (*it)->BackLinks.end(); itlink++)
			{
				Empty = (*it)->CloneDup(false);
				Empty->Time -= 0.5;

				new LINK(Previous, Empty, 1, WordsID[(char *)"*IGNORE*"]);
				new LINK(Empty, Next, (*itlink)->Posterior, (*itlink)->WordId, 0.0, (*itlink)->AcProbability); 

				Explosed->push_back(Empty);
			}

			Explosed->push_back(Next);
			Previous = Next;
		}
		else 
		{
			Previous = (*it)->CloneDup(false);
			Explosed->push_back(Previous);

			First = false;
		}
	}


	std::sort(Explosed->begin(), Explosed->end(), SortByTime);

	for (int n=0; n < Explosed->size(); n++)
		(*Explosed)[n]->Number=n;

	return Explosed;
}




vector<NODE *> *LoadMesh(char *Data, ReadLM *LM)
{
	char Tampon[1024];
	char *Tmp = Data;
	int EndTmp;
	bool ReadOK = true;
	bool Tokenize;
	float Posterior;

	int WID;

	char *Line = NULL;
	char *Cursor = NULL;
	char *Token;
	char *TokenCursor;

	vector<NODE *> *Graphe;

	Graphe = new vector<NODE *>;

	int NbToken;
	char *str;
	bool isWord=true;
	int CurrentNode;

	while (ReadOK == true)
	{
		Line = ForEach(Data, Cursor, "\n");


		if (Line == NULL) ReadOK = false;
		if (Line) str = strstr(Line, "align");
		else str = NULL;

		if (Line && str && str == &Line[0])
		{
			Tokenize=true;
			TokenCursor = NULL;
			NbToken=0;		
			isWord = true;

			while (Tokenize == true)
			{
				Token = ForEach(Line, TokenCursor, " \t#");

				if (Token)
				{
					if (NbToken)
					{
						if (NbToken == 1) 
						{
							CurrentNode =  atoi(Token);
							if (CurrentNode == 0) Graphe->push_back( new NODE(CurrentNode, Posterior, CurrentNode)  );
							Graphe->push_back( new NODE(CurrentNode+1, Posterior, CurrentNode+1)  );
						}
						else if (isWord)
						{
							WID = AddWord(Token, LM);
							isWord = false;
						}
						else
						{
							Posterior = atof(Token);
							new LINK((*Graphe)[CurrentNode], (*Graphe)[CurrentNode+1], Posterior, WID, 0.0, log(Posterior));
							isWord = true;
						}
					}
					NbToken++;
					delete [] Token;
				}
				else Tokenize = false;
			}


			delete [] Line;
		}
	}

	return Graphe;
}




vector<NODE *> *LoadGraph(char *Data, ReadLM *LM)
{
	char Tampon[1024];
	char *Tmp = Data;
	int EndTmp;
	bool ReadOK = true;
	bool Tokenize;

	char *Line = NULL;
	char *Cursor = NULL;
	char *TokenCursor;

	vector<NODE *> *Graphe;

	Graphe = new vector<NODE *>;

	while (ReadOK == true)
	{
		Line = ForEach(Data, Cursor, "\n");

		if (Line)
		{
			if (strstr(Line, "lmscale=")) LINK::MLFudge = atof(&Line[8]);
			if (strstr(Line, "acscale=")) LINK::AcFudge = atof(&Line[8]);
			if (strstr(Line, "wdpenalty=")) LINK::Penalty = atof(&Line[10]);
			if (strstr(Line, "UTTERANCE=")) Utterance = strdup(&Line[10]);

			if (strstr(Line, "I="))
			{
				Graphe->push_back(ParseNode(Line, LM));
			}

			if (strstr(Line, "J="))
			{
				ParseLink(Line, Graphe, LM);
			}
			delete [] Line;
		}
		else ReadOK = false;	
	}
	return Graphe;
}



vector<NODE*>* ReduceGraph2(vector<NODE *> *Graph)
{

	vector<NODE *> *ReducedGraph = new vector<NODE *>;
	set<struct LINK *>::iterator it;
	set<struct LINK *>::iterator it2;
	set<NODE *> Deleted;
	int n;


	bool Reset=false;

	for (n = Graph->size()-1; n >= 0; n--)
	{
		if (Deleted.count((*Graph)[n]) == 0 && (*Graph)[n]->NextLinks.size())
		{
			for (it = (*Graph)[n]->BackLinks.begin();it != (*Graph)[n]->BackLinks.end() ; it++)
			{
				for (it2 = (*Graph)[n]->BackLinks.begin(); it2 != (*Graph)[n]->BackLinks.end(); it2++)
				{
					if (*it != *it2 &&  (*it)->AcProbability == (*it2)->AcProbability && (*it)->LmProbability == (*it2)->LmProbability  && (*it)->From->WordId == (*it2)->From->WordId && (*it)->From != (*it2)->From && (*it)->From->NextLinks.size() == 1 && (*it2)->From->NextLinks.size() == 1)
					{
						LINK *LinkToRemove = *it2;
						LINK *KeepedLink = *it;

						Deleted.insert(LinkToRemove->From);
						KeepedLink->From->merge2(LinkToRemove->From, LinkToRemove);


						it = (*Graph)[n]->BackLinks.begin();
						it2 = (*Graph)[n]->BackLinks.begin();
						//n = Graph->size() -1;
					}
				}
				//if (Reset) break;
			}
		}
	}
	/*
	   for (n = 0; n < Graph->size(); n++)
	   if (!Deleted.count((*Graph)[n]))
	   ReducedGraph->push_back((*Graph)[n])  ;
	   */
	vector<NODE *>::iterator itv;

	cerr <<"Graph size : "<<Graph->size()<<endl;
	for (itv = Graph->begin(); itv != Graph->end(); itv++)
	{
		if (Deleted.count(*itv)) 
		{
			Graph->erase(itv), itv = Graph->begin();
			//cerr <<"Graph size : "<<Graph->size()<<endl;
		}
	}

	cerr <<"Graph size : "<<Graph->size()<<endl;

	for (int n=0; n < Graph->size(); n++)
		(*Graph)[n]->Number=n;

	Deleted.clear();



	return Graph;
}





void RemoveNULL(NODE *Current, LINK *LinkToRemove, set<CONNECT *, CompareConnects> *Connections, vector<NODE *> *NewGraph)
{
	cerr <<"remove null"<<endl;
	if (LinkToRemove->Target->BackLinks.size() == 1) RemoveNULLGeneralCase(Current, LinkToRemove, Connections, NewGraph, true);
	else if (Current->NextLinks.size() == 1) RemoveUniqNULL(Current, LinkToRemove, Connections, NewGraph); //(2)
	else RemoveNULLGeneralCase(Current, LinkToRemove, Connections, NewGraph, false); // (1)
}


// prend en compte que le lien peut comporter des probabilités non nulles
void RemovePau(NODE *&Current, LINK *LinkToRemove , set<CONNECT *, CompareConnects> *Connections, vector<NODE *> *NewGraph)
{
	bool DelNode = false;
	if(LinkToRemove->Target->BackLinks.size() <= 1) DelNode = true; // (3)	
	RemoveNULLGeneralCase(Current, LinkToRemove,  Connections, NewGraph, DelNode); // (1)
}


void RemoveNULLGeneralCase(NODE *&Current, LINK *LinkToRemove, set<CONNECT *, CompareConnects> *Connections, vector<NODE *> *NewGraph, bool DelNode)
{
	set<struct LINK *, LinkCompare > ::iterator itlinka;

	for (itlinka = LinkToRemove->Target->NextLinks.begin(); itlinka != LinkToRemove->Target->NextLinks.end(); itlinka++)
	{

		CONNECT *ConnectTmp = new CONNECT(LinkToRemove->From, (*itlinka)->Target);

		if (Connections->find(ConnectTmp) == Connections->end() || (*itlinka)->Target->NextLinks.size() == 0)
		{
			new LINK(LinkToRemove->From, (*itlinka)->Target, (*itlinka)->Posterior, (*itlinka)->WordId, (*itlinka)->LmProbability + LinkToRemove->LmProbability, (*itlinka)->AcProbability + LinkToRemove->AcProbability);

			Connections->insert(ConnectTmp);
		}
		else
		{
			delete ConnectTmp;

			NODE *Clone = (*itlinka)->Target->CloneDup(true, false, true);

			new LINK(Current, Clone, (*itlinka)->Posterior, (*itlinka)->WordId, (*itlinka)->LmProbability + LinkToRemove->LmProbability, (*itlinka)->AcProbability + LinkToRemove->AcProbability);

			NewGraph->push_back(Clone);
		}


	}

	set <LINK *, LinkCompare> ::iterator it;

	it = LinkToRemove->From->NextLinks.find(LinkToRemove);

	if (it != LinkToRemove->From->NextLinks.end()) LinkToRemove->From->NextLinks.erase(it);

	it = LinkToRemove->Target->BackLinks.find(LinkToRemove);

	if (it != LinkToRemove->Target->BackLinks.end()) LinkToRemove->Target->BackLinks.erase(it);

	if (DelNode) Current = LinkToRemove->Target;
}



vector<NODE*> *RemoveNullAndPause(vector<NODE *> *Graph, ReadLM *LM)
{
	vector<NODE *> *NewGraph = new vector<NODE *>;


	set<CONNECT *, CompareConnects> Connections;


	std::sort(Graph->begin(), Graph->end(), SortByTime);

	int MaxId = LM->GetMaxId();
	vector<NODE *>::iterator it;
	set<struct LINK *, LinkCompare >::iterator itlink;
	int numnode=0;

	for (it = Graph->begin(); it != Graph->end(); it++, numnode++)
	{
		//cerr <<"remove null, node : " <<numnode<<" / "<<Graph->size()<<endl;
		for (itlink = (*it)->NextLinks.begin(); itlink != (*it)->NextLinks.end(); itlink++)
		{
			if ((*itlink)->WordId > MaxId && (*itlink)->Target->NextLinks.size())
			{
				NODE *Current = (*it);
				NODE *Ref = (*it);
				RemovePau(Current, (*itlink), &Connections, NewGraph);

				if (Current != Ref)
					//{
					DeleteNodeAndLinks(Current, false);
				//break;
				//}
				//else
				//{
				if ((*it)->NextLinks.size()) itlink = (*it)->NextLinks.begin();
				else itlink = (*it)->NextLinks.end();
				//}
			}
		}
	}


	for (it = Graph->begin(); it != Graph->end(); it++, numnode++)
	{
		if ((*it)->NextLinks.size() || (*it)->BackLinks.size())
			NewGraph->push_back((*it));
	}

	std::sort(NewGraph->begin(), NewGraph->end(), SortByTime);


	numnode=0;
	for (it = NewGraph->begin(); it != NewGraph->end(); it++, numnode++)
		(*it)->Number = numnode;

	return NewGraph;
}



// cas où les probabilités acoustiques et linguistiques sont nulles, et que le lien nul est unique
void RemoveUniqNULL (NODE *Current, LINK *LinkToRemove,  set<CONNECT *, CompareConnects> *Connections, vector<NODE *> *NewGraph )
{
	set<struct LINK *, LinkCompare >::iterator itlinkb;

	for (itlinkb = Current->BackLinks.begin(); itlinkb != Current->BackLinks.end(); itlinkb++)
	{//		new LINK((*itlinkb)->From, LinkToRemove->Target, (*itlinkb)->Posterior, (*itlinkb)->WordId, (*itlinkb)->LmProbability, (*itlinkb)->AcProbability);


		CONNECT *ConnectTmp = new CONNECT((*itlinkb)->From, LinkToRemove->Target);

		if (Connections->find(ConnectTmp) == Connections->end() || LinkToRemove->Target->NextLinks.size() == 0)
		{
			new LINK((*itlinkb)->From, LinkToRemove->Target, (*itlinkb)->Posterior, (*itlinkb)->WordId, (*itlinkb)->LmProbability, (*itlinkb)->AcProbability);
			Connections->insert(ConnectTmp);
		}
		else
		{
			delete ConnectTmp;

			NODE *Clone = LinkToRemove->Target->CloneDup(true, false, true);

			new LINK((*itlinkb)->From, Clone, (*itlinkb)->Posterior, (*itlinkb)->WordId, (*itlinkb)->LmProbability, (*itlinkb)->AcProbability);

			NewGraph->push_back(Clone);
		}
	}




	DeleteNodeAndLinks(Current, false);
}










