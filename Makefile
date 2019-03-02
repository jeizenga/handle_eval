
FINDLIB=
FINDLIB+=-L vg/lib
FINDLIB+=-L /usr/local/lib
FINDLIB+=-L /opt/local/lib
FINDLIB+=-L /opt/local/lib/libomp -lomp

LIB=
LIB+=-lvg
LIB+=-lvcflib -lgssw -lssw -lprotobuf -lsublinearLS -lhts -ldeflate -lpthread -ljansson -lncurses -lgcsa2 -lgbwt -ldivsufsort -ldivsufsort64 -lvcfh -lgfakluge -lraptor2 -lsdsl -lpinchesandcacti -l3edgeconnected -lsonlib -lfml -llz4 -lstructures -lvw -lboost_program_options -lallreduce

INC=
INC+=-I dankgraph/dynamic-prefix/src/dynamic/include
INC+=-I dankgraph/gfakluge-prefix/src/gfakluge/src
INC+=-I dankgraph/sdsl-lite-prefix/src/sdsl-lite/src
INC+=-I dankgraph/sparsepp-prefix/src/sparsepp/sparsepp
INC+=-I dankgraph/tayweeargs-prefix/src/tayweeargs
INC+=-I dankgraph/src
INC+=-I vg/include

CXXFLAGS=
CXXFLAGS += -Xpreprocessor -fopenmp
CXXFLAGS += -I/opt/local/include/libomp

all: bin/project

vg/lib/libvg.a: vg/src/*
	cd vg && make -j 4

dankgraph/CMakeFiles/dg.dir/src/graph.cpp.o: dankgraph/src/*
	cd dankgraph && cmake CMakeLists.txt && make -j 4

bin/project: src/project.cpp vg/lib/libvg.a dankgraph/CMakeFiles/dg.dir/src/graph.cpp.o
	g++ src/project.cpp $(INC) $(CXXFLAGS) -c -o obj/project.o
	g++ obj/project.o dankgraph/CMakeFiles/dg.dir/src/graph.cpp.o $(FINDLIB) $(LIB) $(CXXFLAGS) -o bin/project
