
FINDLIB=
FINDLIB+=-L vg/lib
FINDLIB+=-L /usr/lib
FINDLIB+=-L /usr/local/lib
FINDLIB+=-L /opt/local/lib
FINDLIB+=-L /opt/local/lib/libomp

LIB=
LIB+=-lvg
LIB+=-lvcflib -lgssw -lssw -lprotobuf -lsublinearLS -lhts -ldeflate -lpthread -ljansson -lncurses -lgcsa2 -lgbwt -ldivsufsort -ldivsufsort64 -lvcfh -lgfakluge -lraptor2 -lsdsl -lpinchesandcacti -l3edgeconnected -lsonlib -lfml -llz4 -lstructures -lvw -lboost_program_options -lallreduce -lz -lbz2 -llzma -lhandlegraph -lomp -lstdc++
LIB+=-lcairo -lz -lgobject-2.0 -lffi -lglib-2.0 -lintl -lpcre -lintl  -liconv -lpixman-1 -lfontconfig -liconv -lexpat -luuid -lfreetype -lbz2 -lpng16 -lz -lX11-xcb -lxcb-render -lXrender -lXext -lX11 -lxcb -lXau -lXdmcp -ldl -llzma -lrocksdb  -lsnappy -lz -lbz2 -llz4 

INC=
INC+=-I dankgraph/dynamic-prefix/src/dynamic/include
INC+=-I dankgraph/gfakluge-prefix/src/gfakluge/src
INC+=-I dankgraph/sdsl-lite-prefix/src/sdsl-lite/src
INC+=-I dankgraph/sparsepp-prefix/src/sparsepp/sparsepp
INC+=-I dankgraph/tayweeargs-prefix/src/tayweeargs
INC+=-I dankgraph/handlegraph-prefix/src
INC+=-I dankgraph/backwardscpp-prefix/src
INC+=-I dankgraph/bbhash-prefix/src
INC+=-I dankgraph/bsort-prefix/src
INC+=-I dankgraph/ska-prefix/src/ska
INC+=-I dankgraph/src
INC+=-I vg/include
INC+=-I vg/cpp
INC+=-I vg
INC+=-I vg/include/dynamic
INC+=-I vg/include/sonLib
INC+=-I vg/src
INC+=-I vg/src/algorithms
INC+=-I /usr/local/include
INC+=-I /opt/local/include/pixman-1
INC+=-I /opt/local/include/ossp
INC+=-I /opt/local/include/freetype2
INC+=-I /opt/local/include/libpng16
INC+=-I /opt/local/include/cairo
INC+=-I /opt/local/include/glib-2.0 -I/opt/local/lib/glib-2.0/include


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
	g++ obj/project.o /opt/local/lib/libstdc++.6.dylib dankgraph/CMakeFiles/dg.dir/src/graph.cpp.o $(FINDLIB) $(LIB) $(CXXFLAGS) -o bin/project
