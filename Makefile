CWD=$(shell pwd)


FINDLIB=
FINDLIB+=-L lib
FINDLIB+=-L vg/lib
FINDLIB+=-L xg/lib
FINDLIB+=-L /usr/lib
FINDLIB+=-L /usr/local/lib
FINDLIB+=-L /opt/local/lib
FINDLIB+=-L /opt/local/lib/libomp

LIB=
LIB+=-lvg -lvgio -lbdsg -lxg
LIB+=-lvcflib -lgssw -lssw -lprotobuf -lsublinearLS -lhts -ldeflate -lpthread -ljansson -lncurses -lgcsa2 -lgbwt -ldivsufsort -ldivsufsort64 -lvcfh -lgfakluge -lraptor2 -lsdsl -lpinchesandcacti -l3edgeconnected -lsonlib -lfml -llz4 -lstructures -lvw -lboost_program_options -lallreduce -lz -lbz2 -llzma -lhandlegraph -lomp -lstdc++
LIB+=-lcairo -lz -lgobject-2.0 -lffi -lglib-2.0 -lpcre  -liconv -lpixman-1 -lfontconfig -liconv -lexpat -luuid -lfreetype -lbz2 -lpng16 -lz -lX11-xcb -lxcb-render -lXrender -lXext -lX11 -lxcb -lXau -lXdmcp -ldl -llzma -lrocksdb  -lsnappy -lz -lbz2 -llz4
LIB+=-latomic

INC=
INC+=-I .
INC+=-I include/
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
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/algorithms/topological_sort.cpp.o
ODGI_OBJ+=odgi/build/CMakeFiles/odgi.dir/src/algorithms/is_single_stranded.cpp.o

CXXFLAGS=
CXXFLAGS += -O3 --std=c++14 -march=native
CXXFLAGS += -Xpreprocessor -fopenmp

all: bin/eval

lib/libbdsg.a: $(wildcard libbdsg-easy/deps/bdsg/src/*) $(wildcard libbdsg-easy/deps/bdsg/include/*)
	cd libbdsg-easy && make && INSTALL_PREFIX=$(CWD) make install

vg/lib/libvg.a: $(wildcard vg/src/*)
	cd vg && make

xg/lib/libxg.a: $(wildcard xg/src/*)
	cd xg && mkdir -p build && cd build && cmake .. && make

odgi/build/CMakeFiles/odgi.dir/src/graph.cpp.o: $(wildcard odgi/src/*)
	cd odgi && mkdir -p build && cd build && cmake .. && make

bin/eval: src/eval.cpp lib/libbdsg.a vg/lib/libvg.a odgi/build/CMakeFiles/odgi.dir/src/graph.cpp.o xg/lib/libxg.a
	g++ src/eval.cpp $(INC) $(CXXFLAGS) -c -o obj/eval.o
	g++ obj/eval.o $(ODGI_OBJ) $(FINDLIB) $(LIB) $(CXXFLAGS) -o bin/eval

-include pre-build

pre-build:
	mkdir -p obj
	mkdir -p bin

.PHONY: pre-build all;
