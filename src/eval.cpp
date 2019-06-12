//  project.cpp

#include <stdio.h>
#include <iostream>
#include <chrono>

#include "odgi/src/odgi.hpp"
#include "odgi/src/gfa_to_handle.hpp"
#include "xg/src/xg.hpp"
#include "vg/src/vg.hpp"
#include "vg/src/handle.hpp"
#include "vg/src/convert_handle.hpp"
#include "sglib/packed_graph.hpp"
#include "sglib/hash_graph.hpp"
#include <vg/io/vpkg.hpp>


using namespace std;
using namespace vg;
using namespace handlegraph;
using namespace odgi;

void help_me(char** argv) {
    cerr << "usage: " << argv[0] << " [test_type] [convert_type] input_file" << endl;
}


void convert_graphs_test(string& output_format, string& input_file, bool make_serialized){
    
    bool vg_out = false;
    bool pg_out = false;
    bool hg_out = false;
    bool og_out = false;
    bool xg_out = false;
    
    if (output_format == "vg") {
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
    else if (output_format == "xg") {
        xg_out = true;
    }
    else {
        abort();
    }
    
    // convert into the format we indicated
    if (vg_out){
        VG vg;
        gfa_to_handle(input_file, &vg);
        if (make_serialized){
            vg.optimize();
            vg.serialize(cout);
        }
    }
    else if (pg_out){
        sglib::PackedGraph pg;
        gfa_to_handle(input_file, &pg);
        if (make_serialized){
            pg.optimize();
            pg.serialize(cout);
        }
    }
    else if (hg_out){
        sglib::HashGraph hg;
        gfa_to_handle(input_file, &hg);
        if (make_serialized){
            hg.optimize();
            hg.serialize(cout);
        }
    }
    else if (og_out){
        graph_t og;
        gfa_to_handle(input_file, &og);
        if (make_serialized){
            og.optimize();
            og.serialize(cout);
        }
    }
    else if (xg_out){
        xg::XG xg;
        xg.from_gfa(input_file);
        if (make_serialized){
            xg.serialize(cout);
        }
    }
}

void test_from_serialized(string& serlialized_type, string& input_file, bool test_accesses) {
    
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool og_in = false;
    bool xg_in = false;
    
    if (serlialized_type == "vg") {
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
    else if (serlialized_type == "xg") {
        xg_in = true;
    }
    else {
        abort();
    }
    
    VG* vg_graph = nullptr;
    sglib::PackedGraph* pg  = nullptr;
    sglib::HashGraph* hg = nullptr;
    graph_t* og = nullptr;
    xg::XG* xg = nullptr;
    
    PathHandleGraph* test_graph = nullptr;
    
    ifstream in(input_file);
    if (vg_in) {
        vg_graph = new VG();
        vg_graph->deserialize(in);
        test_graph = vg_graph;
    }
    else if (pg_in){
        pg = new sglib::PackedGraph();
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg = new sglib::HashGraph();
        hg->deserialize(in);
        test_graph = hg;
    }
    else if (og_in){
        og = new graph_t();
        og->load(in);
        test_graph = og;
    }
    else if (og_in){
        xg = new xg::XG();
        xg->load(in);
        test_graph = xg;
    }
    
    if (test_accesses) {
        
        int node_counter = 0;
        auto node_start = std::chrono::system_clock::now();
        test_graph->for_each_handle([&](const handle_t& h) {
            node_counter++;
        });
        auto node_end = std::chrono::system_clock::now();
        std::chrono::duration<double> node_elapsed_seconds = node_end - node_start;
        
        vector<handle_t> handles;
        test_graph->for_each_handle([&](const handle_t& h) {
            for (bool orientation : {false, true}) {
                handles.push_back(test_graph->get_handle(test_graph->get_id(h), orientation));
            }
        });
        
        int edge_counter = 0;
        auto edge_start = std::chrono::system_clock::now();
        for(handle_t handle:handles){
            test_graph->follow_edges(handle, true, [&](const handle_t& next) {
                edge_counter++;
            });
        }
        auto edge_end = std::chrono::system_clock::now();
        
        std::chrono::duration<double> edge_elapsed_seconds = edge_end - edge_start;
        
        int path_counter = 0;
        auto path_start = std::chrono::system_clock::now();
        test_graph->for_each_path_handle([&](const path_handle_t& path_handle_1){
            for (handle_t handle : test_graph->scan_path(path_handle_1)) {
                volatile handle_t temp_handle = handle;
            }
            path_counter++;
        });
        auto path_end = std::chrono::system_clock::now();
        std::chrono::duration<double> path_elapsed_seconds = path_end - path_start;
        
        
        cerr << "number of nodes accessed: " << node_counter << endl;
        cerr << "elapsed time: " << node_elapsed_seconds.count() << endl;
        cerr << "number of edges accessed: " << edge_counter << endl;
        cerr << "elapsed time: " << edge_elapsed_seconds.count() << endl;
        cerr << "number of paths accessed: " << path_counter << endl;
        cerr << "elapsed time: " << path_elapsed_seconds.count() << endl;
    }
}

int main(int argc, char** argv) {
    
    if (argc != 4) {
        help_me(argv);
        return 1;
    }
    
    // get the command line args
    string test_name = argv[1];
    string convert_type = argv[2];
    string input_file = argv[3];
    
    // either convert from GFA and serialize or test a serialized handle graph
    if (test_name == "convert" || test_name == "serialize") {
        convert_graphs_test(convert_type, input_file, test_name == "serialize");
    }
    else if (test_name == "deserialize" || test_name == "access") {
        test_from_serialized(convert_type, input_file, test_name == "access");
    }
    else {
        cerr << "available tests: convert, serialize, deserialize, access" << endl;
    }
}
