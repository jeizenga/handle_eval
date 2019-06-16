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


def createFigure(inputFile, outputDirectory):
    # parse data
    data = {}
    df = pandas.read_csv(inputFile,  sep='\t', names=("file name", "test type", "graph type", "real", "usr", "sys", "max memory", "nodes/edges/paths", "nodes/edges/paths time", "blank"))

    df = df.drop("blank", axis=1)
    # print(df)

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
                # utilize[graphType] = np.mean(deserializeFileGraphData["max memory"])
                utilize[graphType] = [deserializeFileGraphData["max memory"]]
                convertFileGraphData  = convertFileData.loc[df["graph type"] == graphType]
                # memory[graphType] = np.mean(convertFileGraphData["max memory"])
                memory[graphType] = [convertFileGraphData["max memory"]]
                # speed[graphType] = np.mean(convertFileGraphData["sys"] + convertFileGraphData["usr"])
                speed[graphType] = [convertFileGraphData["sys"] + convertFileGraphData["usr"]]

                for testType in [3,4,5]:
                    dataFileGraphData = data[testType].loc[df["file name"] == fileName[:-3] + graphName].loc[df["graph type"] == graphType]
                    if testType == 3:
                        nodes[graphType] = [dataFileGraphData["nodes/edges/paths time"].astype(np.float)] /np.mean(dataFileGraphData["nodes/edges/paths"].astype(np.float))
                    elif testType ==4:
                        edges[graphType] = [dataFileGraphData["nodes/edges/paths time"].astype(np.float)] /np.mean(dataFileGraphData["nodes/edges/paths"].astype(np.float))
                    elif testType == 5:
                        paths[graphType] = [dataFileGraphData["nodes/edges/paths time"].astype(np.float)] /np.mean(dataFileGraphData["nodes/edges/paths"].astype(np.float))

            # colors of vg, pg, hg, and og
            R = [128/255,168/255,67/255,7/255]
            G = [171/255,221/255,162/255,104/255]
            B = [134/255,181/255,202/255,172/255]
            # graphNumbers = {1:"vg", 2:"pg", 3:"hg", 4:"og"}
            graphNumbers = {1: "vg", 2: "pg", 3: "hg"}

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
            memoryError = []
            maxMemory = 0
            speedError = []
            maxSpeed = 0
            utilizeError = []
            maxUtilize = 0

            for index in range(0,len(memory)):
                memoryHeight = np.mean(memory[index + 1])
                memoryStd = np.std(memory[index + 1])
                memoryError.append(memoryHeight+memoryStd)
                maxMemory = max(maxMemory, max(memory[index + 1][0]))

                speedHeight = np.mean(speed[index + 1])
                speedStd = np.std(speed[index + 1])
                speedError.append(speedHeight + speedStd)
                maxSpeed = max(maxSpeed, max(speed[index + 1][0]))

                utilizeHeight = np.mean(utilize[index + 1])
                utilizeStd = np.std(utilize[index + 1])
                utilizeError.append(utilizeHeight + utilizeStd)
                maxUtilize = max(maxUtilize, max(utilize[index + 1][0]))


            for index in range(0, len(memory)):
                bottom = 0
                left = bins[index] + .1
                width = bins[index + 1] - left - .1
                errorBarLeft = errorBins[index]
                # print(0, max(bins), 0, max(memoryError))
                swarmplot(panel1, memory[index+1], bins[index] + .5, 2, 2, 0, max(bins),
                          0, maxMemory * 1.05, 1, 3, (R[index], G[index], B[index]))

                swarmplot(panel2, speed[index + 1], bins[index]+.5, 2, 2, 0, max(bins),
                          0, maxSpeed * 1.05, .5, 3, (R[index], G[index], B[index]))

                swarmplot(panel3, utilize[index + 1], bins[index] + .5, 2, 2, 0, max(bins),
                          0, maxUtilize * 1.05, .5, 3, (R[index], G[index], B[index]))

            scientific = np.format_float_scientific(maxMemory*1.05)
            power = int(scientific.split("e+")[-1])
            panel1.set_ylim(0, maxMemory * 1.05)
            panel1.set_xlim(0, max(bins))

            roundedNumber = special_round(maxMemory * 1.05, 10**power)
            panel1.set_yticks([a for a in np.linspace(0, roundedNumber, 5)])
            panel1.set_yticklabels([a for a in np.linspace(0, roundedNumber/10**power,  5)])
            panel1.set_ylabel("Maximum Memory ($10^{"+str(power)+"}$ bytes)",)
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
            panel2.set_ylim(0, maxSpeed * 1.05)
            panel2.set_xlim(0, max(bins))
            panel2.set_ylabel("Time (CPU cycles)")
            # modify tick marks/labeling
            panel2.tick_params(axis="both", which="both",
                               bottom=False, labelbottom=False,
                               left=True, labelleft=True,
                               right=False, labelright=False,
                               top=False, labeltop=False
                               )

            scientific = np.format_float_scientific(max(utilizeError) * 1.1)
            power = int(scientific.split("e+")[-1])
            panel3.set_ylim(0, maxUtilize * 1.05)
            panel3.set_xlim(0, max(bins))

            roundedNumber = special_round(maxUtilize * 1.05, 10 ** power)
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
            maxnep = 0

            for nep in [nodes, edges, paths]:
                nepIndexing = 0
                for index in range(len(nodes) *(counter), len(nodes) * (counter+1)):
                    height = np.mean(nep[nepIndexing + 1])
                    speedStd = np.std(nep[nepIndexing + 1])
                    errorBars.append(height + speedStd)
                    maxnep = max(maxnep, max(nep[nepIndexing + 1][0]))
                    nepIndexing += 1
                counter += 1

            counter = 0
            for nep in [nodes, edges, paths]:
                nepIndexing = 0
                for index in range(len(nodes) *(counter), len(nodes) * (counter+1)):
                    bottom = 0
                    left = bins[index]
                    width = bins[index + 1] - left
                    height = np.mean(nep[nepIndexing +1])
                    errorBarLeft = errorBins[index]
                    #
                    # rectangle1 = mplpatches.Rectangle([left, bottom], width,
                    #                                   height,
                    #                                   edgecolor="black",
                    #                                   facecolor=(R[nepIndexing], G[nepIndexing], B[nepIndexing]),
                    #                                   linewidth=.1)
                    # panel4.add_patch(rectangle1)
                    #
                    # speedStd = np.std(nep[nepIndexing +1])
                    # errorBar = mplpatches.Rectangle([errorBarLeft, height - speedStd], errorBarWidth,
                    #                                 speedStd * 2,
                    #                                 edgecolor="black",
                    #                                 facecolor="black",
                    #                                 linewidth=.1)
                    # errorBars.append(height + speedStd)
                    # panel4.add_patch(errorBar)

                    swarmplot(panel4, nep[nepIndexing +1], bins[index] + .5, 2, 2, 0, max(bins),
                              0, maxnep * 1.05, .5, 3, (R[nepIndexing], G[nepIndexing], B[nepIndexing]))

                    nepIndexing += 1
                counter += 1
            panel4.set_ylim(0, maxnep * 1.05)
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


def swarmplot(panel, data, xcoord, pw, ph, xmin, xmax, ymin, ymax, space, size, color):
    """
    Swarmplot function from Vollmers.
    """
    data = np.array(data)[0]
    data = sorted(data)
    xr = xmax - xmin
    yr = ymax - ymin
    min_dist = size / 75
    increment = size / 200

    potential_x_positions = []
    for x_shift in np.arange(0, space, increment):
        potential_x_positions.append(xcoord + x_shift)
        potential_x_positions.append(xcoord - x_shift)

    plotted_points = []

    for y1 in data:
        if len(plotted_points) == 0:
            plotted_points.append((xcoord, y1))
        else:
            compare_points = []
            for x2, y2 in plotted_points:
                ydist = ((((y1 - y2) / yr) * ph) ** 2) ** 0.5
                if ydist < min_dist:
                    compare_points.append((x2, y2))
            if len(compare_points) > 0:
                for x1 in potential_x_positions:
                    distances = []
                    remove_list = []
                    for x2, y2 in compare_points:
                        xdist = (((x1 - x2) / xr) * pw)
                        ydist = (((y1 - y2) / yr) * ph)
                        distance = ((xdist ** 2) + (ydist ** 2)) ** 0.5
                        distances.append(distance)
                        if distance > min_dist:
                            if x1 > x2 and x2 > xcoord:
                                remove_list.append((x2, y2))
                            if x1 < x2 and x2 < xcoord:
                                remove_list.append((x2, y2))
                        else:
                            break

                    if min(distances) > min_dist:
                        plotted_points.append((x1, y1))
                        break
                    else:
                        for point in remove_list:
                            compare_points.remove(point)
            else:
                plotted_points.append((xcoord, y1))

    x_list = []
    y_list = []
    for x, y in plotted_points:
        x_list.append(x)
        y_list.append(y)

    panel.plot(x_list, y_list, markersize=size, marker='o', markeredgewidth=0,
               color=color, linewidth=0)


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return (s, size_name[i])

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