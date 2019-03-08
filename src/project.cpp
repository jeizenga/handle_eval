//  project.cpp

#include <stdio.h>
#include <iostream>

#include "dankgraph/src/graph.hpp"
#include "vg/src/vg.hpp"
#include "vg/src/xg.hpp"
#include "vg/src/handle.hpp"
#include "vg/src/convert_handle.hpp"
#include "vg/src/packed_graph.hpp"
#include "vg/src/hash_graph.hpp"
#include "vg/src/stream/vpkg.hpp"



using namespace std;
using namespace xg;
using namespace vg;
using namespace handlegraph;
using namespace odgi;
void help_me(char** argv) {
    cerr << "usage: " << argv[0] << " project [out_options] input_file" << endl;
}


int main(int argc, char** argv) {
    
    if (argc == 2) {
        help_me(argv);
        return 1;
    }
    if (argc < 3) {
        help_me(argv);
        return 1;
    }
    
    string vg_in = argv[2];
    bool vg_out = false;
    bool pg_out = false;
    bool hg_out = false;
    bool dg_out = false;
    
    int c = atoi(argv[1]);
    // look at out commands
    switch(c){
        case 1:
            vg_out = true;
            break;
        case 2:
            pg_out = true;
            break;
        case 3:
            hg_out = true;
            break;
        case 4:
            dg_out = true;
            break;
        default:
            abort();
    }
    
    cerr << "vg_in" << vg_in << endl;
    cerr << "vg_out" << vg_out << endl;
    cerr << "pg_out" << pg_out << endl;
    cerr << "hg_out" << hg_out << endl;
    cerr << "dg_out" << dg_out << endl;

    
    
//    if (!vg_in.empty()){
//        ifstream in(vg_in);
//        VG* vg = new VG(in);
//    }
    ifstream in(vg_in);
//    VG* vg = new VG(in);
//    delete vg;
    VG graph(in);
   
//    VG* vg;
//    convert_handle_graph(&graph, &vg);
//    // let's try converting
    if (vg_out){
        VG vg;
        convert_handle_graph(&graph, &vg);
    }
    else if (pg_out){
        PackedGraph pg;
        convert_handle_graph(&graph, &pg);
    }
    else if (hg_out){
        HashGraph hg;
        convert_handle_graph(&graph, &hg);
    }
    else if (dg_out){
        graph_t dg;
        convert_handle_graph(&graph, &dg);
    }
//    else {
//
//    }
    cerr << "end of program" << endl;
    
}
