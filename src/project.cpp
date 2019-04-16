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
    bool quit_out = false;
    bool vg_out = false;
    bool pg_out = false;
    bool hg_out = false;
    bool dg_out = false;
    
    int c = atoi(argv[1]);
    // look at out commands
    switch(c){
        case 0:
            quit_out = true;
            break;
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
    
//    cerr << "vg_in" << vg_in << endl;
//    cerr << "quit_out" << quit_out << endl;
//    cerr << "vg_out" << vg_out << endl;
//    cerr << "pg_out" << pg_out << endl;
//    cerr << "hg_out" << hg_out << endl;
//    cerr << "dg_out" << dg_out << endl;

    
    
    ifstream in(vg_in);
    VG graph(in); // input graph called "graph"
    
    cerr << "node_size " << graph.node_size() << endl;
    cerr << "edge_count " << graph.edge_count() << endl;
    cerr << "path_count " << graph.get_path_count() << endl;
    
    int path_occurance = 0;
    graph.for_each_path_handle([&](const path_handle_t& path) {
        
        path_occurance += graph.get_occurrence_count(path);
    });
    cerr << "path_occurance " << path_occurance << endl;
   
//    // let's try converting
    if (vg_out){
        VG vg;
        convert_path_handle_graph(&graph, &vg);
    }
    else if (pg_out){
        PackedGraph pg;
        convert_path_handle_graph(&graph, &pg);
    }
    else if (hg_out){
        HashGraph hg;
        convert_path_handle_graph(&graph, &hg);
    }
    else if (dg_out){
        graph_t dg;
        convert_path_handle_graph(&graph, &dg);
    }
    
}
