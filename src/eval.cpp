//  project.cpp

#include <stdio.h>
#include <iostream>
#include <chrono>

#include "odgi/src/odgi.hpp"
#include "vg/src/vg.hpp"
#include "vg/src/xg.hpp"
#include "vg/src/handle.hpp"
#include "vg/src/convert_handle.hpp"
#include "vg/src/packed_graph.hpp"
#include "vg/src/hash_graph.hpp"
#include <vg/io/vpkg.hpp>



using namespace std;
using namespace xg;
using namespace vg;
using namespace handlegraph;
using namespace odgi;

void help_me(char** argv) {
    cerr << "usage: " << argv[0] << " eval [test_type] [convert_type] input_file" << endl;
}


void convert_graphs_test(string& output_format, string& input_file, bool make_serialized){
    
    bool quit_out = false;
    bool vg_out = false;
    bool pg_out = false;
    bool hg_out = false;
    bool og_out = false;
    
    switch(output_format){
        case "none":
            quit_out = true;
            break;
        case "vg":
            vg_out = true;
            break;
        case "pg":
            pg_out = true;
            break;
        case "hg":
            hg_out = true;
            break;
        case "og":
            og_out = true;
            break;
        default:
            abort();
    }
    
    ifstream in(input_file);
    VG graph(in); // input graph called "graph"
    
    // convert into the format we indicated
    if (vg_out){
        VG vg;
        convert_path_handle_graph(&graph, &vg);
        if (make_serialized){
            vg.optimize();
            vg.serialize(cout);
        }
    }
    else if (pg_out){
        PackedGraph pg;
        convert_path_handle_graph(&graph, &pg);
        if (make_serialized){
            pg.optimize();
            pg.serialize(cout);
        }
    }
    else if (hg_out){
        HashGraph hg;
        convert_path_handle_graph(&graph, &hg);
        if (make_serialized){
            hg.optimize();
            hg.serialize(cout);
        }
    }
//    else if (og_out){
//        graph_t og;
//        convert_path_handle_graph(&graph, &og);
//        if (make_serialized){
//            og.opimize();
//            og.serialize(cout);
//        }
//    }
}

void make_deserialize_test(string& convert_type, string& input_file){
    
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool og_in = false;
    switch(convert_type){
        case "none":
            quit_in = true;
            break;
        case "vg":
            vg_in = true;
            break;
        case "pg":
            pg_in = true;
            break;
        case "hg":
            hg_in = true;
            break;
        case "og":
            og_in = true;
            break;
        default:
            abort();
    }
    ifstream in(input_file);
    if (vg_in){
        VG vg;
        vg.deserialize(in);
    }
    else if (pg_in){
        PackedGraph pg;
        pg.deserialize(in);
    }
    else if (hg_in){
        HashGraph hg;
        hg.deserialize(in);
    }
//    else if (og_in){
//        graph_t dg;
//        dg.load(in);
//    }
    
}

void make_nodes_per_second(string& convert_type, string& input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool og_in = false;
    switch(convert_type){
        case "none":
            quit_in = true;
            break;
        case "vg":
            vg_in = true;
            break;
        case "pg":
            pg_in = true;
            break;
        case "hg":
            hg_in = true;
            break;
        case "og":
            og_in = true;
            break;
        default:
            abort();
    }
    ifstream in(input_file);
    
    VG* vg_graph = nullptr;
    PackedGraph* pg  = nullptr;
    HashGraph* hg = nullptr;
//    graph_t dg = nullptr;
    
    
    PathHandleGraph* test_graph = nullptr;
    
    if (vg_in) {
        vg_graph = new VG();
        vg->deserialize(in);
        test_graph = vg_graph;
    }
    else if (pg_in){
        pg = new PackedGraph();
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg = new HashGraph();
        hg->deserialize(in);
        test_graph = hg;
    }
//    else if (og_in){
//        dg = new graph_t(in);
//        test_graph = dg;
//    }
    
    int node_counter = 0;
    auto start = std::chrono::system_clock::now();
    test_graph->for_each_handle([&](const handle_t& h) {
        node_counter++;
    });
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end - start;
    cerr << "number of nodes accessed: " << node_counter << endl;
    cerr << "elapsed time: " << elapsed_seconds.count() << endl;
}

void make_edges_per_second(string& convert_type, string& input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool og_in = false;
    switch(convert_type){
        case "none":
            quit_in = true;
            break;
        case "vg":
            vg_in = true;
            break;
        case "pg":
            pg_in = true;
            break;
        case "hg":
            hg_in = true;
            break;
        case "og":
            og_in = true;
            break;
        default:
            abort();
    }
    ifstream in(input_file);

    VG* vg_graph = nullptr;
    PackedGraph* pg  = nullptr;
    HashGraph* hg = nullptr;
//    graph_t dg = nullptr;


    PathHandleGraph* test_graph = nullptr;

    if (vg_in) {
        vg_graph = new VG(in);
        test_graph = vg_graph;
    }
    else if (pg_in){
        pg = new PackedGraph();
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg = new HashGraph();
        hg->deserialize(in);
        test_graph = hg;
    }
//    else if (og_in){
//        dg = new graph_t(in);
//        test_graph = dg;
//    }

    vector<handle_t> handles = {};
    test_graph->for_each_handle([&](const handle_t& h) {
        for (bool orientation : {false, true}) {
            handles.push_back(test_graph->get_handle(test_graph->get_id(h), orientation));
        }
    });

    int edge_counter = 0;
    auto start = std::chrono::system_clock::now();
    for(handle_t handle:handles){
        test_graph->follow_edges(handle, true, [&](const handle_t& next) {
            edge_counter++;
        });
    }
    auto end = std::chrono::system_clock::now();
    
    std::chrono::duration<double> elapsed_seconds = end - start;
    cerr << "number of edges accessed: " << edge_counter << endl;
    cerr << "elapsed time: " << elapsed_seconds.count() << endl;
}

void make_paths_per_second(string& convert_type, string& input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool og_in = false;
    switch(convert_type){
        case "none":
            quit_in = true;
            break;
        case "vg":
            vg_in = true;
            break;
        case "pg":
            pg_in = true;
            break;
        case "hg":
            hg_in = true;
            break;
        case "og":
            og_in = true;
            break;
        default:
            abort();
    }
    ifstream in(input_file);

    VG* vg_graph = nullptr;
    PackedGraph* pg  = nullptr;
    HashGraph* hg = nullptr;
    //    graph_t dg = nullptr;


    PathHandleGraph* test_graph = nullptr;

    if (vg_in) {
        vg_graph = new VG(in);
        test_graph = vg_graph;
    }
    else if (pg_in){
        pg = new PackedGraph();
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg = new HashGraph();
        hg->deserialize(in);
        test_graph = hg;
    }
//    else if (og_in){
//        dg = new graph_t(in);
//        test_graph = dg;
//    }

    int path_counter = 0;
    auto start = std::chrono::system_clock::now();
    test_graph->for_each_path_handle([&](const path_handle_t& path_handle_1){
        for (handle_t handle : test_graph->scan_path(path_handle_1)) {
            volatile handle_t temp_handle = handle;
        }
        path_counter++;
    });
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end - start;
    cerr << "number of paths accessed: " << path_counter << endl;
    cerr << "elapsed time: " << elapsed_seconds.count() << endl;
}


int main(int argc, char** argv) {
    
    if (argc == 3) {
        help_me(argv);
        return 1;
    }
    if (argc < 4) {
        help_me(argv);
        return 1;
    }
    
    // what test should we run?
    
    bool convert_graphs = false;
    bool make_serialized = false;
    bool make_deserialize = false;
    bool nodes_per_second = false;
    bool edges_per_second = false;
    bool paths_per_second = false;
    // look at out commands
    switch(argv[1]){
        case "convert":
            convert_graphs = true;
            break;
        case "serialize":
            make_serialized = true;
            break;
        case "deserialize":
            make_deserialize = true;
            break;
        case "nodes":
            nodes_per_second = true;
            break;
        case "edges":
            edges_per_second = true;
            break;
        case "paths":
            paths_per_second = true;
            break;
        default:
            abort();
    }
    
    
    // for converting to another graph
    string convert_type = argv[2];
    string input_file = argv[3];
    
    if (convert_graphs){
        convert_graphs_test(convert_type, input_file, false);
    }
    else if (make_serialized){
        convert_graphs_test(convert_type, input_file, true);
    
    }
    else if (make_deserialize){
        make_deserialize_test(convert_type, input_file);
    }
    else if (nodes_per_second){
        make_nodes_per_second(convert_type, input_file);
    }
    else if (edges_per_second){
        make_edges_per_second(convert_type, input_file);
    }
    else if (paths_per_second){
        make_paths_per_second(convert_type, input_file);
    }
}
