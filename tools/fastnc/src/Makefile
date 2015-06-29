ifndef CXXFLAGS
#CXXFLAGS= -O3 -msse2 -ip
#CXXFLAGS= -fast -fpermissive 
#CXXFLAGS= -O3 -ip
#CXXFLAGS= -fast

CXXFLAGS= -g3 -O3
endif

#ifndef CXX
#CXX=icpc

CXX=g++
#endif

BINDIR=../bin
INCDIRLM=../../lm/include
INCDIR=../include

LIBDIR=../lib

INC=-I $(INCDIR) -I $(INCDIRLM)
LIB=

all: fastnc

fastnc: fastnc.o ../../lm/src/readlm.o ../../lm/src/MurmurHash3.o ../../lm/src/myregex.o ../../lm/src/chargementtrans.o ../../lm/src/buildlm.o
	$(CXX) $(CXXFLAGS) $(INC) $(LIB) -o $(BINDIR)/fastnc fastnc.o ../../lm/src/readlm.o ../../lm/src/MurmurHash3.o  ../../lm/src/myregex.o ../../lm/src/chargementtrans.o ../../lm/src/buildlm.o

fastnc.o: fastnc.cpp $(INCDIRLM)/readlm.h $(INCDIRLM)/dataLM.h $(INCDIR)/fastnc.h $(INCDIR)/alignContainer.h $(INCDIRLM)/buildlm.h
	 $(CXX) $(CXXFLAGS) $(INC) $(LIB) -c fastnc.cpp 

clean:
	rm -f *.o $(LIBDIR)/*.a *~ $(BINDIR)/fastnc
