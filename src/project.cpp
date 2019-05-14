//  project.cpp

#include <stdio.h>
#include <iostream>
#include <chrono>

//#include "dankgraph/src/graph.hpp"
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
//using namespace odgi;

void help_me(char** argv) {
    cerr << "usage: " << argv[0] << " project [test_type] [convert_type] input_file" << endl;
}


void convert_graphs_test(int convert_type, string input_file, bool make_serialized){
    bool quit_out = false;
    bool vg_out = false;
    bool pg_out = false;
    bool hg_out = false;
    bool dg_out = false;
    switch(convert_type){
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
    
        cerr << "vg_in" << input_file << endl;
        cerr << "quit_out" << quit_out << endl;
        cerr << "vg_out" << vg_out << endl;
        cerr << "pg_out" << pg_out << endl;
        cerr << "hg_out" << hg_out << endl;
        cerr << "dg_out" << dg_out << endl;
    
    ifstream in(input_file);
    cerr << "opened file" << endl;
    VG graph(in); // input graph called "graph"
    
    cerr << "node_size " << graph.node_size() << endl;
    cerr << "edge_count " << graph.edge_count() << endl;
    cerr << "path_count " << graph.get_path_count() << endl;
    
    int path_occurance = 0;
    graph.for_each_path_handle([&](const path_handle_t& path) {
        
        path_occurance += graph.get_step_count(path);
    });
    cerr << "path_occurance " << path_occurance << endl;
    
    // let's try converting
    if (vg_out){
        VG vg;
        convert_path_handle_graph(&graph, &vg);
        if (make_serialized){
            vg.serialize_to_ostream(cout);
        }
    }
    else if (pg_out){
        PackedGraph pg;
        convert_path_handle_graph(&graph, &pg);
        if (make_serialized){
            pg.compactify();
            pg.serialize(cout);
        }
    }
    else if (hg_out){
        HashGraph hg;
        convert_path_handle_graph(&graph, &hg);
        if (make_serialized){
            hg.serialize(cout);
        }
    }
//    else if (dg_out){
//        graph_t dg;
//        convert_path_handle_graph(&graph, &dg);
//        if (make_serialized){
//            dg.serialize(cout);
//        }
//    }
}

void make_deserialize_test(int convert_type, string input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool dg_in = false;
    switch(convert_type){
        case 0:
            quit_in = true;
            break;
        case 1:
            vg_in = true;
            break;
        case 2:
            pg_in = true;
            break;
        case 3:
            hg_in = true;
            break;
        case 4:
            dg_in = true;
            break;
        default:
            abort();
    }
    ifstream in(input_file);
    if (vg_in){
        VG vg(in);
    }
    else if (pg_in){
        PackedGraph pg;
        pg.deserialize(in);
    }
    else if (hg_in){
        HashGraph hg;
        hg.deserialize(in);
    }
//    else if (dg_in){
//        graph_t dg;
//        dg.load(in);
//    }
    
}

void make_nodes_per_second(int convert_type, string input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool dg_in = false;
    switch(convert_type){
        case 0:
            quit_in = true;
            break;
        case 1:
            vg_in = true;
            break;
        case 2:
            pg_in = true;
            break;
        case 3:
            hg_in = true;
            break;
        case 4:
            dg_in = true;
            break;
        default:
            abort();
    }
    ifstream in(input_file);
    
//    VG* vg_graph = nullptr;
//    HashGraph* hg = nullptr;
//
//    PathHandleGraph* test_graph = nullptr;
//    if (vg_in) {
//        vg_graph = new VG(in);
//        test_graph = vg_graph;
//    }
//    else {
//        hg->deserialize(in);
//        test_graph = hg;
//    }
//
//    vector<vg::id_t> ids = {};
//    test_graph->for_each_handle([&](const handle_t& h) {
//        ids.push_back(test_graph->get_id(h));
//    });
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
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg->deserialize(in);
        test_graph = hg;
    }
    //    else if (dg_in){
    //        dg = new graph_t(in);
    //        test_graph = dg;
    //    }
    
    int node_counter = 0;
    auto start = std::chrono::system_clock::now();
    test_graph->for_each_handle([&](const handle_t& h) {
        volatile vg::id_t id = test_graph->get_id(h);
        node_counter++;
    });
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end - start;
    cerr << "number of nodes accessed: " << node_counter << endl;
    cerr << "number of nodes in graph: " << test_graph->node_size() << endl;
    cerr << "elapsed time: " << elapsed_seconds.count() << endl;

//    if (vg_in){
//        VG vg(in);
//        vector<vg::id_t> correct_ids = {};
//        for (vg::id_t id = vg.min_node_id(); id <= vg.max_node_id(); id++){
//            if (vg.has_node(id) == true){
//                correct_ids.push_back(id);
//            }
//        }
//        auto start = std::chrono::system_clock::now();
//        for (int i = 0; i <= correct_ids.size(); i++){
//            vg.get_handle(correct_ids[i]);
//        }
//        auto end = std::chrono::system_clock::now();
//        std::chrono::duration<double> elapsed_seconds = end - start;
//        cerr << "elapsed time: " << elapsed_seconds.count() << endl;
//    }
//    else if (pg_in){
//        PackedGraph pg;
//        pg.deserialize(in);
//        vector<vg::id_t> correct_ids = {};
//        for (vg::id_t id = pg.min_node_id(); id <= pg.max_node_id(); id++){
//            if (pg.has_node(id) == true){
//                correct_ids.push_back(id);
//            }
//        }
//        auto start = std::chrono::system_clock::now();
//        for (int i = 0; i <= correct_ids.size(); i++){
//            pg.get_handle(correct_ids[i]);
//        }
//        auto end = std::chrono::system_clock::now();
//        std::chrono::duration<double> elapsed_seconds = end - start;
//        cerr << "elapsed time: " << elapsed_seconds.count() << endl;
//    }
//    else if (hg_in){
//        HashGraph hg;
//        hg.deserialize(in);
//        vector<vg::id_t> correct_ids = {};
//        for (vg::id_t id = hg.min_node_id(); id <= hg.max_node_id(); id++){
//            if (hg.has_node(id) == true){
//                correct_ids.push_back(id);
//            }
//        }
//        auto start = std::chrono::system_clock::now();
//        for (int i = 0; i <= correct_ids.size(); i++){
//            hg.get_handle(correct_ids[i]);
//        }
//        auto end = std::chrono::system_clock::now();
//        std::chrono::duration<double> elapsed_seconds = end - start;
//        cerr << "elapsed time: " << elapsed_seconds.count() << endl;
//    }
//    else if (dg_in){
//        graph_t dg;
//        dg.load(in);
//        vector<vg::id_t> correct_ids = {};
//        for (vg::id_t id = dg.min_node_id(); id <= dg.max_node_id(); id++){
//            if (dg.has_node(id) == true){
//                correct_ids.push_back(id);
//            }
//        }
//        auto start = std::chrono::system_clock::now();
//        for (int i = 0; i <= correct_ids.size(); i++){
//            dg.get_handle(correct_ids[i]);
//        }
//        auto end = std::chrono::system_clock::now();
//        std::chrono::duration<double> elapsed_seconds = end - start;
//        cerr << "elapsed time: " << elapsed_seconds.count() << endl;
//    }
}

void make_edges_per_second(int convert_type, string input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool dg_in = false;
    switch(convert_type){
        case 0:
            quit_in = true;
            break;
        case 1:
            vg_in = true;
            break;
        case 2:
            pg_in = true;
            break;
        case 3:
            hg_in = true;
            break;
        case 4:
            dg_in = true;
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
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg->deserialize(in);
        test_graph = hg;
    }
//    else if (dg_in){
//        dg = new graph_t(in);
//        test_graph = dg;
//    }

    int edge_counter = 0;
    vector<handle_t> handles = {};
    test_graph->for_each_handle([&](const handle_t& h) {
        for (bool orientation : {false, true}) {
            handles.push_back(test_graph->get_handle(test_graph->get_id(h), orientation));
        }
    });

    auto start = std::chrono::system_clock::now();
    for(handle_t handle:handles){
        test_graph->follow_edges(handle, true, [&](const handle_t& next) {
            volatile handle_t temp_handle = next;
            edge_counter++;
        });
    }
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end - start;
    cerr << "number of edges accessed: " << edge_counter << endl;
//    cerr << "number of edges in graph: " << test_graph->edge_count() << endl;
    cerr << "elapsed time: " << elapsed_seconds.count() << endl;
}

void make_paths_per_second(int convert_type, string input_file){
    bool quit_in = false;
    bool vg_in = false;
    bool pg_in = false;
    bool hg_in = false;
    bool dg_in = false;
    switch(convert_type){
        case 0:
            quit_in = true;
            break;
        case 1:
            vg_in = true;
            break;
        case 2:
            pg_in = true;
            break;
        case 3:
            hg_in = true;
            break;
        case 4:
            dg_in = true;
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
        pg->deserialize(in);
        test_graph = pg;
    }
    else if (hg_in){
        hg->deserialize(in);
        test_graph = hg;
    }
    //    else if (dg_in){
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
    cerr << "number of paths in graph: " << test_graph->get_path_count() << endl;
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
    
    string input_file = argv[3];
    
    // what test should we run?
    
    bool convert_graphs = false;
    bool make_serialized = false;
    bool make_deserialize = false;
    bool nodes_per_second = false;
    bool edges_per_second = false;
    bool paths_per_second = false;
    int c = atoi(argv[1]);
    // look at out commands
    switch(c){
        case 0:
            convert_graphs = true;
            break;
        case 1:
            make_serialized = true;
            break;
        case 2:
            make_deserialize = true;
            break;
        case 3:
            nodes_per_second = true;
            break;
        case 4:
            edges_per_second = true;
            break;
        case 5:
            paths_per_second = true;
            break;
        default:
            abort();
    }
    
    // for converting to another graph
    int convert_type = atoi(argv[2]);
    // look at out commands
    
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
