#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""build_genealogy

Usage:
  build_genealogy (--mathid=<id>|--name=<name>)... [--output=<out>]

Options:
  --name=<name>   Name in the form "John Doe" or "John D. Doe"
  --output=<out>  Output file name (.pdf or .png) [default: output.pdf]
"""

import pydot
from pick import pick
from subprocess import call
import os
import requests
import re


# Plot the given dotfiles to PDF of PNG file, merging nodes if necessary
def make_graph(dotfiles, output):
    # Get graphs
    graphs = [pydot.graph_from_dot_file(d)[0] for d in dotfiles]
    # Combine graphs
    graph = combine_graphs(graphs)
    # Plot graph
    graph.set_overlap(0)
    if output.endswith(".png"):
        func = graph.write_png
    elif output.endswith(".pdf"):
        func = graph.write_pdf
    func(output, prog='dot')
    print("Wrote {}".format(output))


# Combine pydot graphs at nodes
def combine_graphs(graphs):
    print("Combining graphs...")
    graph = graphs[0]
    names = [n.get_name() for n in graph.get_nodes()]
    # Add nodes
    for graph2 in graphs[1:]:
        for n in graph2.get_nodes():
            if not graph2.get_name() in names:
                graph.add_node(n)
    # Add edges
    for graph2 in graphs[1:]:
        for e in graph2.get_edges():
            if e not in graph.get_edges():
                graph.add_edge(e)
    return graph


# Get Math Genealogy data by calling Geneagrapher
def get_dotfile(mathid, cache=True):
    print("Gathering data for MathID: {}".format(mathid))
    # Setup temporary folder
    tmpfolder = "/tmp/mathgenealogy/"
    if not os.path.exists(tmpfolder):
        os.mkdir(tmpfolder)
    filename = tmpfolder + str(mathid) + ".dot"
    if not cache or not os.path.isfile(filename):
        call(['ggrapher', '-f', filename, '-a', mathid, "-v"])
    else:
        print("Using cached data")
    return filename


# Get person's id
def getPerson(name):
    print("Looking up {}".format(name))
    name = name.split(" ")
    # Make request
    r = requests.post("https://www.genealogy.math.ndsu.nodak.edu/query-prep.php", data={"given_name": name[0], "family_name": name[-1]})
    # Find results
    r = list(re.findall("<a href=\"id\.php\?id=(\d+)\">(.*?)</a>", r.text))
    if len(r) == 0:
        # No resutls
        print("Error: no results found")
        exit(1)
    elif len(r) > 1:
        # Several results
        r, _ = pick(r, "Several results have been found, please make a choice:")
    else:
        # One result
        r = r[0]
    print("Found " + r[1])
    return r[0]


def graph_genealogy(mathids, names, output):
    # Get mathids
    for n in names:
        mathids.append(getPerson(n))
    # Get dotfiles
    dotfiles = [get_dotfile(m) for m in mathids]
    # Make graph
    make_graph(dotfiles, output)


if __name__ == "__main__":
    from docopt import docopt
    args = docopt(__doc__)
    graph_genealogy(args["--mathid"], args["--name"], args["--output"])
