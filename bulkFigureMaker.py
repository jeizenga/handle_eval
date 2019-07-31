#!/usr/bin/env python3

# example usage:
# python3 bulkFigureMaker.py -i file.tsv  -o figures -cx graph.seq.length -cy build.mem -n graph.node.count


import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse
import math
import pandas
import os


def createFigure(inputFile, outputDirectory, comparex, comparey, normalize=False):
    """
    Create figures.
    :param inputFile: tsv file
    :param outputDirectory: a directory to put all the figures
    :param comparex: graph feature that will be on the x axis
    :param comparey: graph stat (performance measurement) that will be on the y axis
    :param normalize: graph stat divided by the comparey data
    """

    # Create output directory if don't exist, where all the figures will be put
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)


    with open(inputFile, "r") as inFile:
        header = inFile.readline().rstrip().split()

        # got to deal with the missing data
        header.remove("graph.avg.degree")
        header.append("graph.avg.degree")

    df = pandas.read_csv(inputFile,  sep='\t', header=None, skiprows=[0], names=header)

    # calculate the missing graph.avg.degree column
    df["graph.avg.degree"] = (2*df["graph.edge.count"])/df["graph.node.count"]


    # create a smaller data frame called data to store columns that we will be working with
    if normalize:
        data = df[[comparex, "sglib.model", "graph.cyclic"]]
        # normalize the y axis here (save new data as under the column name, comparey for ease of access)
        data[comparey] = df[comparey]/df[normalize]
        print(data)
    else:
        data = df[[comparex, comparey, "sglib.model", "graph.cyclic"]]

    # make the figure
    figure_width = 3
    figure_height = 3

    # color legend. TODO: make real legend, choose pretty colors
    colorDict = {"vg":"red", "pg":"blue", "og":"orange", "xg":"purple", "hg":"pink"}
    # size legend. If cyclic, make larger point.
    cyclicDict = {True:2, False:1}

    plt.figure(figsize=(figure_width, figure_height))

    panel_width = 1 / figure_width  # gives fraction so that we get 1 inch
    panel_height = 1 / figure_height

    panel1 = plt.axes([.2, .2, panel_width * 2, panel_height * 2])

    # figure out what color to plot
    for model in data["sglib.model"].unique():
        filteredData = data.loc[data['sglib.model'] == model]
        # then figure out what size to plot
        for cycle in set(filteredData["graph.cyclic"]):
            cycleFilterData = filteredData.loc[data['graph.cyclic'] == cycle]
            panel1.plot(cycleFilterData[comparex], cycleFilterData[comparey],
                        color="black",
                        marker="o",
                        markeredgecolor="red",
                        markeredgewidth=0,
                        markerfacecolor=colorDict[model],
                        # markersize=1.425,
                        markersize=cyclicDict[cycle],
                        linewidth=0,
                        linestyle="--",
                        alpha=1)
    if normalize:
        panel1.set_ylabel(comparey +" per "+ normalize)
    else:
        panel1.set_ylabel(comparey)
        panel1.set_xlabel(comparex)

    if normalize:
        plt.savefig(outputDirectory + "/" + comparey + "PER" + normalize + "AND" + comparex + ".png",dpi=600)
    else:
        plt.savefig(outputDirectory + "/" + comparey + "AND" + comparex + ".png", dpi=600)

    plt.close()


def argParser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--outputDirectory", "-o",
                        type=str,
                        help="specify the file name of the output file")
    parser.add_argument("--inputFile", "-i",
                        type=str,
                        help="specify the file name of the input file")
    parser.add_argument("--comparex", "-cx",
                        type=str,
                        help="1st column to compare to")
    parser.add_argument("--comparey", "-cy",
                        type=str,
                        help="column to compare to")
    parser.add_argument("--normalize", "-n",
                        type=str,
                        help="comparex items will be divided by this column")

    return vars(parser.parse_args())

def main():
    args = argParser()
    if args["comparex"] is None:
        print("Running all comparisons")
        runAll(args["inputFile"], args["outputDirectory"])
    else:
        # if the comparex argument is given, run with the user input
        createFigure(args["inputFile"], args["outputDirectory"], args["comparex"], args["comparey"], args["normalize"])


def runAll(inputFile, outputDirectory):
    """
    Runs if comparex is not given. Creates figures for all graphFeatures compared to all graphStats.
    :param inputFile: tsv file
    :param outputDirectory: a directory to put all the figures
    """
    graphFeatures = ["graph.node.count", "graph.edge.count",
                     "graph.path.count",
                     "graph.step.count", "graph.avg.path.depth",
                     "graph.seq.length",
                     "graph.max.degree", "graph.avg.degree",
                     "graph.avg.edge.delta", "graph.feedback.fraction",
                     "graph.feedback.arc.count"]
    graphStats = ["build.mem", "load.mem", "build.time", "load.time",
                  "handle.enumeration.time",
                  "edge.traversal.time",
                  "path.traversal.time"]

    for feature in graphFeatures:
        for stat in graphStats:
            createFigure(inputFile, outputDirectory, feature, stat)
        print(feature)


if __name__ == "__main__":
    main()
