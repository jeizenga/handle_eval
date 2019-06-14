#!/usr/bin/env python3

import os
import argparse
import subprocess



class resultMaker:
    def __init__(self, testFileDir, outputFile):
        self.outputFile = outputFile
        self.testFileDir = testFileDir
        self.numberOfIterations = 5
        self.graphTypes = ["vg", "hg", "pg", "og", "xg"]
        self.testTypes = ["convert", "serialize", "deserialize", "access"]

    def runFiles(self):
        with open(self.outputFile, "w") as outputFile:
            
            for i in range(0,self.numberOfIterations):
                for graphType in self.graphTypes:
                    for fileName in os.listdir(self.testFileDir):
                        if not fileName.endswith(".gfa"):
                            continue
                    
                        constructStats, outputFile = self.getStatistics("serialize", graphType, self.testFileDir, fileName, True)
                        loadStats, dummy = self.getStatistics("deserialize", graphType, self.testFileDir, outputFile)
                        accessStats, dummy = self.getStatistics("access", graphType, self.testFileDir, outputFile)
                    
                        print("constructStats")
                        print(constructStats)
                        print("loadStats")
                        print(loadStats)
                        print("accessStats")
                        print(accessStats)
                    
#                    for test in range(0, 2):
#                        for graph in range(1, self.numberOfGraphTypes):
#                            timeMemStats = self.parseData(rawStats)
#                            outputFile.write(fileName)
#                            outputFile.write("\t")
#                            outputFile.write(str(test))
#                            outputFile.write("\t")
#                            outputFile.write(str(graph))
#                            outputFile.write("\t")
#                            for stat in timeMemStats:
#                                outputFile.write(str(stat))
#                                outputFile.write("\t")
#                            outputFile.write("\n")
#
#            for i in range(0, self.numberOfIterations):
#                for fileName in os.listdir(os.path.join(self.testFileDir)):
#                    for test in range(2, 6):
#                        graphName = fileName[-3:]
#                        if graphName == ".vg":
#                            graphType = 1
#                        elif graphName == ".pg":
#                            graphType = 2
#                        elif graphName == ".hg":
#                            graphType = 3
#                        elif graphName == ".og":
#                            graphType = 4
#
#                        if graphType:
#                            rawStats = self.getStatistics(test, graphType, self.testFileDir, fileName)
#                            timeMemStats = self.parseData(rawStats)
#                            outputFile.write(fileName)
#                            outputFile.write("\t")
#                            outputFile.write(str(test))
#                            outputFile.write("\t")
#                            outputFile.write(str(graphType))
#                            outputFile.write("\t")
#                            for stat in timeMemStats:
#                                outputFile.write(str(stat))
#                                outputFile.write("\t")
#                            outputFile.write("\n")


    def getStatistics(self, testType, graphType, directory, file, serialize=False):
        
        assert(graphType in self.graphTypes)
        assert(testType in self.testTypes)
        
        print(testType, graphType, directory, file, serialize)
        print("/usr/bin/time","-v","./bin/project", testType, graphType, os.path.join(directory,file))
        
        outName = None
        
        if serialize:
            
            outName = os.path.basename(file) + "." + graphType
            
            with open(os.path.join(directory, outName), "w") as outFile:
                p = subprocess.Popen( ["/usr/bin/time", "-v", "./bin/project", testType, graphType, os.path.join(directory,file)], stdout=outFile, stderr=subprocess.PIPE, encoding='utf8')
                out, err = p.communicate()
        else:
            p = subprocess.Popen( ["/usr/bin/time", "-v", "./bin/project", testType, graphType, os.path.join(directory,file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
            out, err = p.communicate()

        return err, outName


    def parseData(self, rawStats):
        rawStats = str(rawStats).split("\n")
        numberItems = None
        accessTime = None
        for line in rawStats:
            line = line.rstrip()
            line = line.split()
            if len(line) > 3:
                if line[1] == "real":
                    realTime = line[0]
                    usrTime = line[2]
                    sysTime = line[4]
                elif line[1] == "maximum" and line[2] == "resident":
                    memoryUsage = line[0]
                elif line[0] == "number":
                    if line[4] == "graph:":
                        if numberItems:
                            assert(numberItems == line[-1])
                            numberItems = line[-1]
                    elif line[3] == "accessed:":
                        numberItems = line[-1]
            if len(line) >2:
                if line[0] == "elapsed":
                    accessTime = line[-1]

        return (realTime, usrTime, sysTime, memoryUsage, numberItems, accessTime)




def argParser():
    parser=argparse.ArgumentParser(add_help=True)
    parser.add_argument("--outputFile","-o",
                        type=str,
                        help="specify the file name of the output file")
    parser.add_argument("--testFileDir","-i",
                        type=str,
                        help="specify the directory name of the input files")


    return vars(parser.parse_args())

def main():
    args = argParser()
    myResultMaker = resultMaker(args["testFileDir"],args["outputFile"])
    myResultMaker.runFiles()


if __name__ == "__main__":
    main()
