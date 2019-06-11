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
    
    if (output_format == "none") {
        quit_out = true;
    }
    else if (output_format == "vg") {
        vg_out = true;
    }
    else if (output_format == "pg") {
        pg_out = true;
    }
    else if (output_format == "hg") {
        hg_out = true;
    }
    else if (output_format == "og") {
        og_out = true;
    }
    else {
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

void test_from_serialized(string& serlialized_type, string& input_file, string& test_name) {
    
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool og_in = false;
    
    if (serlialized_type == "none") {
        quit_in = true;
    }
    else if (serlialized_type == "vg") {
        vg_in = true;
    }
    else if (serlialized_type == "pg") {
        pg_in = true;
    }
    else if (serlialized_type == "hg") {
        hg_in = true;
    }
    else if (serlialized_type == "og") {
        og_in = true;
    }
    else {
        abort();
    }
    
    VG* vg_graph = nullptr;
    PackedGraph* pg  = nullptr;
    HashGraph* hg = nullptr;
//    graph_t dg = nullptr;
    
    
    PathHandleGraph* test_graph = nullptr;
    
    ifstream in(input_file);
    if (vg_in) {
        vg_graph = new VG();
        vg_graph->deserialize(in);
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
    
    if (test_name == "deserialize") {
        // we're already done
    }
    else if (test_name == "nodes") {
        
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
    else if (test_name == "edges") {
        
        vector<handle_t> handles;
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
    else if (test_name == "paths") {
        
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
    
    // for converting to another graph
    string test_name = argv[1];
    string convert_type = argv[2];
    string input_file = argv[3];
    
    // look at out commands
    if (test_name == "convert"){
        convert_graphs_test(convert_type, input_file, false);
    }
    else if (test_name == "serialize"){
        convert_graphs_test(convert_type, input_file, true);
    }
    else {
        test_from_serialized(convert_type, input_file, test_name);
    }
}
