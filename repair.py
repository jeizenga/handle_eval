#!/usr/bin/env python
import sys

repairing = sys.argv[1]
assert(".tsv" in repairing)
repaired = repairing[:repairing.index(".tsv")] + ".repaired.tsv"

with open(repairing) as infile:
  with open(repaired, "w") as outfile:
    header = next(infile).strip().split()
    node_idx = header.index("graph.node.count")
    edge_idx = header.index("graph.edge.count")
    degree_idx = header.index("graph.avg.degree")
    print("\t".join(header), file = outfile)
    for line in infile:
        tokens = line.strip().split()
        if len(tokens) == len(header) - 1:
            avg_deg = 2.0 * float(tokens[edge_idx]) / float(tokens[node_idx])
            tokens.insert(degree_idx, str(avg_deg))
        print("\t".join(tokens), file = outfile)
