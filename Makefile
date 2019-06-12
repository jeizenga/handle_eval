
FINDLIB=
FINDLIB+=-L ./vg/lib
FINDLIB+=-L /usr/lib
FINDLIB+=-L /usr/local/lib
FINDLIB+=-L /opt/local/lib
FINDLIB+=-L /opt/local/lib/libomp

LIB=
LIB+=-lvg -lvgio -latomic
LIB+=-lvcflib -lgssw -lssw -lprotobuf -lsublinearLS -lhts -ldeflate -lpthread -ljansson -lncurses -lgcsa2 -lgbwt -ldivsufsort -ldivsufsort64 -lvcfh -lgfakluge -lraptor2 -lsdsl -lpinchesandcacti -l3edgeconnected -lsonlib -lfml -llz4 -lstructures -lvw -lboost_program_options -lallreduce -lz -lbz2 -llzma -lhandlegraph -lomp -lstdc++
LIB+=-lcairo -lz -lgobject-2.0 -lffi -lglib-2.0 -lpcre  -liconv -lpixman-1 -lfontconfig -liconv -lexpat -luuid -lfreetype -lbz2 -lpng16 -lz -lX11-xcb -lxcb-render -lXrender -lXext -lX11 -lxcb -lXau -lXdmcp -ldl -llzma -lrocksdb  -lsnappy -lz -lbz2 -llz4 

INC=
INC+=-I .
INC+=-I odgi/build/dynamic-prefix/src/dynamic/include
INC+=-I odgi/build/gfakluge-prefix/src/gfakluge/src
INC+=-I odgi/build/sdsl-lite-prefix/src/sdsl-lite/src
INC+=-I odgi/build/sparsepp-prefix/src/sparsepp/sparsepp
INC+=-I odgi/build/tayweeargs-prefix/src/tayweeargs
INC+=-I odgi/build/handlegraph-prefix/src
INC+=-I odgi/build/backwardscpp-prefix/src
INC+=-I odgi/build/bbhash-prefix/src
INC+=-I odgi/build/bsort-prefix/src
INC+=-I odgi/build/ska-prefix/src/ska
INC+=-I odgi/src
INC+=-I vg/include
INC+=-I vg/cpp
INC+=-I vg
INC+=-I vg/include/dynamic
INC+=-I vg/include/sonLib
INC+=-I vg/src
INC+=-I vg/src/algorithms
INC+=-I xg/src
INC+=-I xg/build/mmmultimap-prefix/src/mmmultimap/src
INC+=-I xg/build/ips4o-prefix/src/ips4o
INC+=-I /usr/local/include
INC+=-I /opt/local/include/pixman-1
INC+=-I /opt/local/include/ossp
INC+=-I /opt/local/include/freetype2
INC+=-I /opt/local/include/libpng16
INC+=-I /opt/local/include/cairo
INC+=-I /opt/local/include/glib-2.0 -I/opt/local/lib/glib-2.0/include

ODGI_OBJ=
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/odgi.cpp.o
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/crash.cpp.o
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/node.cpp.o
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/position.cpp.o
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/threads.cpp.o
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/gfa_to_handle.cpp.o

XG_OBJ=
XG_OBJ+=xg/build/CMakeFiles/xg.dir/src/xg.cpp.o

CXXFLAGS=
CXXFLAGS += -O3 --std=c++14 -march=native
CXXFLAGS += -Xpreprocessor -fopenmp
CXXFLAGS += -I/opt/local/include/libomp

all: bin/eval

vg/lib/libvg.a: vg/src/*
	cd vg && make -j 8

xg/build/CMakeFiles/xg.dir/src/xg.cpp.o: xg/src/*
	cd xg && mkdir -p build && cd build && cmake .. && make -j 8

odgi/build/CMakeFiles/odgi.dir/src/graph.cpp.o: odgi/src/*
	cd odgi && mkdir -p build && cd build && cmake .. && make -j 8

bin/eval: src/eval.cpp vg/lib/libvg.a odgi/build/CMakeFiles/odgi.dir/src/graph.cpp.o xg/build/CMakeFiles/xg.dir/src/xg.cpp.o
	g++ src/eval.cpp $(INC) $(CXXFLAGS) -c -o obj/eval.o
	g++ obj/eval.o $(ODGI_OBJ) $(XG_OBJ) $(FINDLIB) $(LIB) $(CXXFLAGS) -o bin/eval

-include pre-build

pre-build:
	mkdir -p obj
	mkdir -p bin

.PHONY: pre-build all;
