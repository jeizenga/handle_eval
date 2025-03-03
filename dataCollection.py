#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys


class resultMaker:
    def __init__(self, testFileDir, outputFile):
        self.outputFile = outputFile
        self.testFileDir = testFileDir
        self.numberOfIterations = 1
        self.graphTypes = ["vg", "hg", "pg", "xg", "og"]
        self.testTypes = ["convert", "serialize", "deserialize", "access"]

    def runFiles(self):
        with open(self.outputFile, "w") as outputFile:
            for fileName in os.listdir(self.testFileDir):
                if not fileName.endswith(".gfa"):
                    continue

                print("testing on " + fileName, file = sys.stderr)
                for graphType in self.graphTypes:
                    print("\ttesting graph type " + graphType, file = sys.stderr)
                    for i in range(0,self.numberOfIterations):
                    
                        # construct from GFA and serialize
                        constructErr, graphFile = self.getStatistics("serialize", graphType, self.testFileDir, fileName, True)
                        # load from serialized, but do nothing
                        loadErr, dummy = self.getStatistics("deserialize", graphType, self.testFileDir, graphFile)
                        # load from serliazed and time accesses to graph features
                        accessErr, dummy = self.getStatistics("access", graphType, self.testFileDir, graphFile)
                    
                        # parse the stderr output
                        constructStats = self.parseData(constructErr)
                        loadStats = self.parseData(loadErr)   
                        accessStats = self.parseData(accessErr)    
                        
                        # match (roughly) the format that Emily's plotting script expects
                        
                        row = [fileName, "construct", graphType, constructStats["realTime"], constructStats["usrTime"], 
                               constructStats["sysTime"], constructStats["memoryUsage"], "NA", "NA"]
                        print("\t".join(str(val) for val in row), file = outputFile)
                        
                        row = [fileName, "deserialize", graphType, loadStats["realTime"], loadStats["usrTime"], 
                               loadStats["sysTime"], loadStats["memoryUsage"], "NA", "NA"]
                        print("\t".join(str(val) for val in row), file = outputFile)
                        
                        for accessType in ["nodes", "edges", "paths"]:
                            numItems, accessTime = accessStats[accessType]
                            row = [fileName, accessType, graphType, accessStats["realTime"], accessStats["usrTime"], 
                                   accessStats["sysTime"], accessStats["memoryUsage"], numItems, accessTime]
                            print("\t".join(str(val) for val in row), file = outputFile)
                            
                        # clean up the graph we made
                        os.remove(os.path.join(self.testFileDir, graphFile))

    def parseTime(self, timeStr):
        tokens = timeStr.split(":")
        secs = 0.0
        for i in range(len(tokens)):
            secs += 60**i * float(tokens[len(tokens) - 1 - i])
        return secs

    def getStatistics(self, testType, graphType, directory, file, serialize=False):
        
        assert(graphType in self.graphTypes)
        assert(testType in self.testTypes)
        
        #print(testType, graphType, directory, file, serialize)
        #print("/usr/bin/time","-v","./bin/eval", testType, graphType, os.path.join(directory,file))
        
        outName = None
        
        cmd = ["/usr/bin/time", "-v", "./bin/eval", testType, graphType, os.path.join(directory,file)]   
        
        if serialize:
            
            outName = os.path.basename(file) + "." + graphType
            
            with open(os.path.join(directory, outName), "w") as outFile:
                p = subprocess.Popen(cmd, stdout=outFile, stderr=subprocess.PIPE, encoding='utf8')
                out, err = p.communicate()
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
            out, err = p.communicate()
        
        if p.returncode != 0:
            print("Command failed: " + " ".join(cmd), file = sys.stderr)
            print("stderr:\n" + err, file = sys.stderr)
            assert(False)

        return err, outName


    def parseData(self, rawStats):
        
        stats = {}
        
        gen = (line for line in str(rawStats).split("\n"))
        for line in gen:
            line = line.strip().lower()
            if line.startswith("elapsed (wall clock)"):
                stats["realTime"] = self.parseTime(line.split()[-1])
            elif line.startswith("user time"):
                stats["usrTime"] = self.parseTime(line.split()[-1])
            elif line.startswith("system time"):
                stats["sysTime"] = self.parseTime(line.split()[-1])
            elif line.startswith("maximum resident set size"):
                stats["memoryUsage"] = float(line.split()[-1])
            elif line.startswith("number of"):
                tokens = line.split()
                accessType = tokens[2]
                numberItems = int(tokens[-1])
                # the next line contains the actual time it took
                accessTime = float(next(gen).strip().split()[-1])
                
                stats[accessType] = (numberItems, accessTime)

        return stats




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
