//  project.cpp

#include <stdio.h>
#include <iostream>
#include <chrono>
#include <unordered_map>
#include <vector>
#include <string>
#include <cmath>

#include "odgi/src/odgi.hpp"
#include "odgi/src/gfa_to_handle.hpp"
#include "odgi/src/algorithms/topological_sort.hpp"
#include "xg/src/xg.hpp"
#include "vg/src/vg.hpp"
#include "vg/src/handle.hpp"
#include "vg/src/convert_handle.hpp"
#include "vg/src/split_strand_graph.hpp"
#include "vg/src/algorithms/eades_algorithm.hpp"
#include "vg/src/algorithms/is_acyclic.hpp"
#include "sglib/packed_graph.hpp"
#include "sglib/hash_graph.hpp"
#include <vg/io/vpkg.hpp>


using namespace std;
using namespace handlegraph;

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
        vg::VG vg;
        odgi::gfa_to_handle(input_file, &vg);
        if (make_serialized){
            vg.optimize();
            vg.serialize(cout);
        }
    }
    else if (pg_out){
        sglib::PackedGraph pg;
        odgi::gfa_to_handle(input_file, &pg);
        if (make_serialized){
            pg.optimize();
            pg.serialize(cout);
        }
    }
    else if (hg_out){
        sglib::HashGraph hg;
        odgi::gfa_to_handle(input_file, &hg);
        if (make_serialized){
            hg.optimize();
            hg.serialize(cout);
        }
    }
    else if (og_out){
        odgi::graph_t og;
        odgi::gfa_to_handle(input_file, &og);
        if (make_serialized){
            // TODO: this should really be the default optimize, but for now we just include it
            og.apply_ordering(odgi::algorithms::topological_order(&og), true);
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

void test_from_serialized(string& serlialized_type, string& input_file, bool test_accesses, bool print_stats) {
    
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
    
    vg::VG* vg_graph = nullptr;
    sglib::PackedGraph* pg  = nullptr;
    sglib::HashGraph* hg = nullptr;
    odgi::graph_t* og = nullptr;
    xg::XG* xg = nullptr;
    
    PathHandleGraph* test_graph = nullptr;
    
    ifstream in(input_file);
    if (vg_in) {
        vg_graph = new vg::VG();
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
        og = new odgi::graph_t();
        og->load(in);
        test_graph = og;
    }
    else if (xg_in){
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
        test_graph->for_each_path_handle([&](const path_handle_t& path_handle) {
            test_graph->for_each_step_in_path(path_handle, [&](const step_handle_t& step) {
                path_counter++;
            });
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
    
    if (print_stats) {
        
        // node count
        cerr << "node count: " << test_graph->get_node_count() << endl;
        
        // edge count
        size_t num_edges = 0;
        test_graph->for_each_edge([&](const edge_t& edge) {
            num_edges++;
        });
        cerr << "edge count: " << num_edges << endl;
        
        // path count
        cerr << "path count: " << test_graph->get_path_count() << endl;
        
        // path depth
        size_t total_path_length = 0;
        test_graph->for_each_path_handle([&](const path_handle_t& path_handle) {
            total_path_length += test_graph->get_step_count(path_handle);
        });
        cerr << "path steps: " << total_path_length << endl;
        cerr << "avg path depth: " << (double(total_path_length) / double(test_graph->get_node_count())) << endl;
        
        // sequence length
        size_t total_seq_length = 0;
        test_graph->for_each_handle([&](const handle_t& handle) {
            total_seq_length += test_graph->get_length(handle);
        });
        cerr << "seq length: " << total_seq_length << endl;
        cerr << "avg seq length: " << (double(total_seq_length) / double(test_graph->get_node_count())) << endl;
        
        // avg edge delta
        double total_delta = 0.0;
        test_graph->for_each_edge([&](const edge_t& edge) {
            total_delta += abs(int64_t(test_graph->get_id(edge.first)),
                               int64_t(test_graph->get_id(edge.second)));
        });
        cerr << "avg edge delta: " << (total_delta / double(num_edges)) << endl;
        
        // is cyclic
        cerr << "is acyclic: " << !vg::algorithms::is_acyclic(test_graph) << endl;
        
        // feedback arc set
        vg::StrandSplitGraph split(test_graph);
        vector<handle_t> layout = vg::algorithms::eades_algorithm(&split);
        unordered_map<handle_t, size_t> order;
        order.reserve(layout.size());
        for (size_t i = 0; i < layout.size(); ++i) {
            order[layout[i]] = i;
        }
        
        size_t num_feedback_arcs = 0;
        split.for_each_handle([&](const handle_t& handle) {
            split.follow_edges(handle, false, [&](const handle_t& next) {
                if (order[next] <= order[handle]) {
                    ++num_feedback_arcs;
                }
            });
        });
        cerr << "feedback arc set: " << num_feedback_arcs << endl;
        
        // max degree
        size_t max_degree = 0;
        test_graph->for_each_handle([&](const handle_t& handle) {
            max_degree = max(max_degree,
                             test_graph->get_degree(handle, false) + test_graph->get_degree(handle, true));
        });
        cerr << "max degree: " << max_degree << endl;
        cerr << "avg degree: " << (double(2 * num_edges) / double(test_graph->get_node_count())) << endl;
        
        // maximum planar subgraph?
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
    else if (test_name == "deserialize" || test_name == "access" || test_name == "stats") {
        test_from_serialized(convert_type, input_file, test_name == "access", test_name == "stats");
    }
    else {
        cerr << "available tests: convert, serialize, deserialize, access, stats" << endl;
        return 1;
    }
}
