#!/usr/bin/env python3

# example usage:
# python3 createFigures.py -i outputDataCollection  -o figures

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse
import random
import math
import pandas
import time
import datetime
from datetime import datetime as dt
import os


def createFigure(inputFile, outputDirectory):
    # Create output directory if don't exist, where all the figures will be put
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

    # parse data
    data = {}
    df = pandas.read_csv(inputFile,  sep='\t', names=("file name", "test type", "graph type", "real", "usr", "sys", "max memory", "nodes/edges/paths", "nodes/edges/paths time", "blank"))
    df = df.drop("blank", axis=1)

    convertData = []
    deserializeData = []

    for testType in df["test type"].unique():
        if testType == 0:
            convertData = df.loc[df['test type'] == testType]
        if testType == 2:
            deserializeData = df.loc[df['test type'] == testType]
        elif testType > 2:
            data[testType] = df.loc[df['test type'] == testType]

    for fileName in convertData["file name"].unique():
        if fileName == "all.vg" or fileName == "created" or fileName == ".DS_Store":
            pass
        else:
            # make the figure
            figure_width = 6.5
            figure_height = 6.5

            plt.figure(figsize=(figure_width, figure_height))

            panel_width = 1 / figure_width  # gives fraction so that we get 1 inch
            panel_height = 1 / figure_height

            panel1 = plt.axes([.1, .525, panel_width * 2, panel_height * 2])
            panel2 = plt.axes([.6, .525, panel_width * 2, panel_height * 2])
            panel3 = plt.axes([.1, .1, panel_width * 2, panel_height * 2])
            panel4 = plt.axes([.6, .1, panel_width * 2, panel_height * 2])
            panel5 = plt.axes([.1, .925, panel_width * 5.25, panel_height / 4], frameon=False)
            # remove tick marks/labeling from legend
            panel5.tick_params(axis="both", which="both",
                               bottom=False, labelbottom=False,
                               left=False, labelleft=False,
                               right=False, labelright=False,
                               top=False, labeltop=False
                               )



            convertFileData = convertData.loc[df["file name"] == fileName]
            memory = {}
            speed = {}
            utilize = {}
            nodes = {}
            edges = {}
            paths = {}
            print(fileName)
            for graphType in convertFileData["graph type"].unique():
                graphName = None
                if graphType == 1:
                    graphName = ".vg"
                elif graphType == 2:
                    graphName = ".pg"
                elif graphType == 3:
                    graphName = ".hg"
                elif graphType == 4:
                    graphName = ".og"

                deserializeFileGraphData = deserializeData.loc[df["file name"] == fileName[:-3]+graphName].loc[df["graph type"] == graphType]
                utilize[graphType] = np.mean(deserializeFileGraphData["max memory"])
                convertFileGraphData  = convertFileData.loc[df["graph type"] == graphType]
                memory[graphType] = np.mean(convertFileGraphData["max memory"])
                # speed[graphType] = np.mean(convertFileGraphData["sys"] + convertFileGraphData["usr"])
                speed[graphType] = [convertFileGraphData["sys"] + convertFileGraphData["usr"]]

                for testType in [3,4,5]:
                    dataFileGraphData = data[testType].loc[df["file name"] == fileName[:-3] + graphName].loc[df["graph type"] == graphType]
                    x = [dt.strptime(a, '%M:%S.%f') for a in dataFileGraphData["nodes/edges/paths time"]]
                    timeSec = [datetime.timedelta(minutes=i.minute, seconds=i.second,  microseconds=i.microsecond).total_seconds()
                        for i in x]
                    if testType == 3:
                        nodes[graphType] = np.array(timeSec) /np.mean(dataFileGraphData["nodes/edges/paths"].astype(np.float))
                    elif testType ==4:
                        edges[graphType] = np.array(timeSec) /np.mean(dataFileGraphData["nodes/edges/paths"].astype(np.float))
                    elif testType == 5:
                        paths[graphType] = np.array(timeSec) /np.mean(dataFileGraphData["nodes/edges/paths"].astype(np.float))

            # colors of vg, pg, hg, and og
            R = [128/255,168/255,67/255,7/255]
            G = [171/255,221/255,162/255,104/255]
            B = [134/255,181/255,202/255,172/255]
            graphNumbers = {1:"vg", 2:"pg", 3:"hg", 4:"og"}
            # graphNumbers = {1: "vg", 2: "pg", 3: "hg"}

            # legend
            bins = np.arange(0, len(graphNumbers) + 1, 1)
            for index in range(0, len(graphNumbers)):
                bottom = 0
                left = bins[index]
                width = bins[index + 1] - left -.8
                height = 1
                rectangle1 = mplpatches.Rectangle([left, bottom], width, height,
                                                  edgecolor="black",
                                                  facecolor=(R[index], G[index], B[index]),
                                                  linewidth=.1)
                panel5.add_patch(rectangle1)
                panel5.text(left+ width + .15, bottom+(height/2), graphNumbers[index+1], va="center", ha="center")
            panel5.set_ylim(0, 1)
            panel5.set_xlim(0, 4)

            # panel 1, 2, 3
            bins = np.arange(0, len(memory)+1, 1)
            errorBarWidth = .015
            errorBins = [ b+.5 - errorBarWidth/2 for b in bins]
            errorBars = []

            for index in range(0, len(memory)):
                bottom = 0
                left = bins[index] + .1
                width = bins[index + 1] - left - .1
                errorBarLeft = errorBins[index]

                height = memory[index+1]
                rectangle1 = mplpatches.Rectangle([left, bottom], width, height,
                                                  edgecolor="black",
                                                  facecolor=(R[index], G[index], B[index]),
                                                  linewidth=.1)
                panel1.add_patch(rectangle1)
                speedHeight = np.mean(speed[index+1])
                rectangle2 = mplpatches.Rectangle([left, bottom], width, speedHeight,
                                                  edgecolor="black",
                                                  facecolor=(R[index], G[index], B[index]),
                                                  linewidth=.1)
                panel2.add_patch(rectangle2)
                speedStd = np.std(speed[index + 1])
                errorBar = mplpatches.Rectangle([errorBarLeft, speedHeight-speedStd], errorBarWidth, speedStd*2,
                                                  edgecolor="black",
                                                  facecolor="black",
                                                  linewidth=.1)
                errorBars.append(speedHeight+speedStd)
                panel2.add_patch(errorBar)

                utilizeHeight = utilize[index + 1]
                rectangle3 = mplpatches.Rectangle([left, bottom], width,
                                                  utilizeHeight,
                                                  edgecolor="black",
                                                  facecolor=(R[index], G[index], B[index]),
                                                  linewidth=.1)
                panel3.add_patch(rectangle3)

            scientific = np.format_float_scientific(max(memory.values())*1.1)
            power = int(scientific.split("e+")[-1])
            panel1.set_ylim(0, max(memory.values()) * 1.1)
            panel1.set_xlim(0, max(bins))

            roundedNumber = special_round(max(memory.values()) * 1.1, 10**power)
            panel1.set_yticks([a for a in np.linspace(0, roundedNumber, 5)])
            panel1.set_yticklabels([a for a in np.linspace(0, roundedNumber/10**power,  5)])
            panel1.set_ylabel("Maximum Memory ($10^{" + str(power) + "}$ bytes)", )
            panel1.set_title("Construction Memory Usage")
            # offset = panel1.get_yaxis().get_offset_text()
            # print(offset, offset.get_text())
            # panel1.set_ylabel('{0} {1}'.format(panel1.get_ylabel(), offset))
            # offset.set_visible(False)
            # modify tick marks/labeling
            panel1.tick_params(axis="both", which="both",
                               bottom=False, labelbottom=False,
                               left=True, labelleft=True,
                               right=False, labelright=False,
                               top=False, labeltop=False
                               )
            panel2.set_ylim(0, max(errorBars) * 1.05)
            panel2.set_xlim(0, max(bins))
            panel2.set_ylabel("Time (CPU cycles)")
            # modify tick marks/labeling
            panel2.tick_params(axis="both", which="both",
                               bottom=False, labelbottom=False,
                               left=True, labelleft=True,
                               right=False, labelright=False,
                               top=False, labeltop=False
                               )

            scientific = np.format_float_scientific(max(utilize.values()) * 1.1)
            power = int(scientific.split("e+")[-1])
            panel3.set_ylim(0, max(utilize.values()) * 1.1)
            panel3.set_xlim(0, max(bins))

            roundedNumber = special_round(max(utilize.values()) * 1.1, 10 ** power)
            panel3.set_yticks([a for a in np.linspace(0, roundedNumber, 5)])
            panel3.set_yticklabels([a for a in np.linspace(0, roundedNumber / 10 ** power, 5)])
            panel3.set_ylabel("Maximum Memory ($10^{" + str(power) + "}$ bytes)", )
            panel2.set_title("Construction Speed Usage")
            panel3.set_title("Utilization Memory Usage")
            # modify tick marks/labeling
            panel3.tick_params(axis="both", which="both",
                               bottom=False, labelbottom=False,
                               left=True, labelleft=True,
                               right=False, labelright=False,
                               top=False, labeltop=False
                               )


            # panel 4
            bins = np.arange(0, len(nodes) *3 + 1, 1)
            errorBarWidth = .04
            errorBins = [b + .5 - errorBarWidth / 2 for b in bins]
            errorBars = []
            counter = 0

            for nep in [nodes, edges, paths]:
                nepIndexing = 0
                for index in range(len(nodes) *(counter), len(nodes) * (counter+1)):
                    bottom = 0
                    left = bins[index]
                    width = bins[index + 1] - left
                    height = np.mean(nep[nepIndexing +1])
                    errorBarLeft = errorBins[index]

                    rectangle1 = mplpatches.Rectangle([left, bottom], width,
                                                      height,
                                                      edgecolor="black",
                                                      facecolor=(R[nepIndexing], G[nepIndexing], B[nepIndexing]),
                                                      linewidth=.1)
                    panel4.add_patch(rectangle1)

                    speedStd = np.std(nep[nepIndexing +1])
                    errorBar = mplpatches.Rectangle([errorBarLeft, height - speedStd], errorBarWidth,
                                                    speedStd * 2,
                                                    edgecolor="black",
                                                    facecolor="black",
                                                    linewidth=.1)
                    errorBars.append(height + speedStd)
                    panel4.add_patch(errorBar)

                    nepIndexing += 1
                counter += 1
            panel4.set_ylim(0, max(errorBars) * 1.1)
            panel4.set_xlim(0, max(bins))
            panel4.set_ylabel("Time per Access (seconds)")
            panel4.set_title("Access Time")
            # modify tick marks/labeling
            panel4.tick_params(axis="both", which="both",
                               bottom=False, labelbottom=True,
                               left=True, labelleft=True,
                               right=False, labelright=False,
                               top=False, labeltop=False
                               )
            panel4.set_xticks([ i + len(nodes)/2 for i in  np.arange(0, len(nodes)* (counter), 3)])
            panel4.set_xticklabels(["nodes", "edges", "paths"])

            # save plot to output file
            plt.savefig(outputDirectory+"/"+fileName[:-3]+".png", dpi=600)


def argParser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--outputDirectory", "-o",
                        type=str,
                        help="specify the file name of the output file")
    parser.add_argument("--inputFile", "-i",
                        type=str,
                        help="specify the file name of the input file")

    return vars(parser.parse_args())
def special_round(number,base):
    """
    Round numbers to a specific base.
    """
    floored = math.ceil(number/base) * base
    return floored

def main():
    args = argParser()
    createFigure(args["inputFile"], args["outputDirectory"])


if __name__ == "__main__":
    main()