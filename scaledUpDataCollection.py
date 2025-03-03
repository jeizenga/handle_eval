#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys


class resultMaker:
    def __init__(self, testFileDir, outputDir):
        self.outputDir = outputDir
        self.testFileDir = testFileDir
        self.numberOfIterations = 1
        self.graphTypes = ["vg", "hg", "pg", "xg", "og"]
        self.testTypes = ["convert", "serialize", "deserialize", "access", "stats"]

    def runFiles(self):
        for fileName in sorted(os.listdir(self.testFileDir), key = lambda x: os.path.getsize(os.path.join(self.testFileDir, x)), reverse = True):
            if not (fileName.endswith(".gfa") or fileName.endswith(".gfa.gz")):
                continue
            
            shortFileName = fileName
            if shortFileName.endswith(".gz"):
                shortFileName = shortFileName[:shortFileName.index(".gz")]
            
            outputFileName = shortFileName + ".tsv"

            if os.path.isfile(os.path.join(self.outputDir, outputFileName)):
                
                print("output already exists, skipping file " + outputFileName, file = sys.stderr)
                continue
        
            gzipped = fileName.endswith(".gz")
            if gzipped:
                # unzip it
                subprocess.check_call(["gunzip", os.path.join(self.testFileDir, fileName)])
                # point at the unzipped file
                fileName = shortFileName
                    
            outputFile = open(os.path.join(self.outputDir, outputFileName), "w")
            
            cols = ["graph.name", "graph.node.count", "graph.edge.count", "graph.path.count", "graph.step.count", "graph.avg.path.depth", "graph.seq.length",
                    "graph.max.degree", "graph.avg.degree", "graph.cyclic", "graph.avg.edge.delta", "graph.feedback.fraction", "graph.feedback.arc.count",
                    "sglib.model", "build.mem", "load.mem", "build.time", "load.time", "handle.enumeration.time", "edge.traversal.time", "path.traversal.time"]
            
            # print a header
            print("\t".join(cols), file = outputFile)
            

            print("testing on " + fileName, file = sys.stderr)
            try:
                for graphType in self.graphTypes:
                    print("\ttesting graph type " + graphType, file = sys.stderr)
                    for i in range(0,self.numberOfIterations):
                    
                        # construct from GFA and serialize
                        constructErr, graphFile = self.getStatistics("serialize", graphType, self.testFileDir, fileName, True)
                        # load from serialized, but do nothing
                        loadErr, dummy = self.getStatistics("deserialize", graphType, self.testFileDir, graphFile)
                        # load from serliazed and time accesses to graph features
                        accessErr, dummy = self.getStatistics("access", graphType, self.testFileDir, graphFile)
                        # load from serliazed compute
                        graphStatsErr, dummy = self.getStatistics("stats", graphType, self.testFileDir, graphFile)
                    
                        # parse the stderr output
                        constructStats = self.parseTime(constructErr)
                        loadStats = self.parseTime(loadErr)   
                        accessStats = self.parseAccess(accessErr)    
                        graphStats = self.parseGraphStats(graphStatsErr)
                        
#                        cols = ["graph.name", "graph.node.count", "graph.edge.count", "graph.path.count", "graph.step.count", "graph.avg.path.depth", "graph.seq.length",
#                                "graph.max.degree", "graph.avg.degree", "graph.cyclic", "graph.avg.edge.delta", "graph.feedback.fraction", "graph.feedback.arc.count",
#                                "sglib.model", "build.mem", "load.mem", "build.time", "load.time", "handle.enumeration.time", "edge.traversal.time", "path.traversal.time"]
                        
                        # print the row out to the output file
                        
                        row = [fileName, graphStats["nodeCount"], graphStats["edgeCount"], graphStats["pathCount"], graphStats["stepCount"], 
                               graphStats["avgPathDepth"], graphStats["seqLength"], graphStats["maxDegree"], graphStats["avgDegree"], graphStats["cyclic"], graphStats["avgEdgeDelta"],
                               graphStats["feedbackFraction"], graphStats["feedbackArcs"], graphType, constructStats["memoryUsage"], loadStats["memoryUsage"],
                               constructStats["cpuTime"], loadStats["cpuTime"], accessStats["nodes"][1], accessStats["edges"][1], accessStats["paths"][1]]
                        print("\t".join(str(val) for val in row), file = outputFile)
                            
                        # clean up the graph we made
                        os.remove(os.path.join(self.testFileDir, graphFile))
                        
            except subprocess.CalledProcessError as err:
                # we had an issue, clean up the output file so we don't have half-finished ones around
                outputFile.close()
                if os.path.isfile(os.path.join(self.outputDir, outputFileName)):
                    os.remove(os.path.join(self.outputDir, outputFileName))
                raise err
            
            if gzipped:
                # zip it back up
                subprocess.check_call(["gzip", os.path.join(self.testFileDir, fileName)])
            
    def parseTimeStr(self, timeStr):
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
            raise subprocess.CalledProcessError(p.returncode, " ".join(cmd))

        return err, outName

    def parseAccess(self, rawErr):
        stats = {}

        gen = (line for line in rawErr.split("\n"))
        for line in gen:
            if line.startswith("number of"):
                tokens = line.split()
                accessType = tokens[2]
                numberItems = int(tokens[-1])
                # the next line contains the actual time it took
                accessTime = float(next(gen).strip().split()[-1])
                
                stats[accessType] = (numberItems, accessTime)
                
        return stats

    def parseTime(self, rawErr):
        
        stats = {}
        
        for line in str(rawErr).split("\n"):
            line = line.strip().lower()
            if line.startswith("elapsed (wall clock)"):
                stats["realTime"] = self.parseTimeStr(line.split()[-1])
            elif line.startswith("user time"):
                stats["usrTime"] = self.parseTimeStr(line.split()[-1])
            elif line.startswith("system time"):
                stats["sysTime"] = self.parseTimeStr(line.split()[-1])
            elif line.startswith("maximum resident set size"):
                stats["memoryUsage"] = float(line.split()[-1])
        
        stats["cpuTime"] = stats["usrTime"] + stats["sysTime"]

        return stats
    
    def parseGraphStats(self, rawErr):
        
        stats = {}
        
        for line in str(rawErr).split("\n"):
            if line.startswith("node count"):
                stats["nodeCount"] = int(line.split()[-1])
            elif line.startswith("edge count"):
                stats["edgeCount"] = int(line.split()[-1])
            elif line.startswith("path count"):
                stats["pathCount"] = int(line.split()[-1])
            elif line.startswith("path steps"):
                stats["stepCount"] = int(line.split()[-1])
            elif line.startswith("avg path depth"):
                stats["avgPathDepth"] = float(line.split()[-1])
            elif line.startswith("seq length"):
                stats["seqLength"] = int(line.split()[-1])
            elif line.startswith("avg seq length"):
                stats["avgSeqLength"] = float(line.split()[-1])
            elif line.startswith("avg edge delta"):
                stats["avgEdgeDelta"] = float(line.split()[-1])
            elif line.startswith("is cyclic"):
                stats["cyclic"] = bool(int(line.split()[-1]))
            elif line.startswith("feedback arc set"):
                stats["feedbackArcs"] = int(line.split()[-1])
            elif line.startswith("feedback fraction"):
                stats["feedbackFraction"] = float(line.split()[-1])
            elif line.startswith("max degree"):
                stats["maxDegree"] = int(line.split()[-1])
            elif line.startswith("avg degree"):
                stats["avgDegree"] = float(line.split()[-1])
        
        return stats




def argParser():
    parser=argparse.ArgumentParser(add_help=True)
    parser.add_argument("--outputDir","-o",
                        type=str,
                        help="specify the directory to drop the output files in")
    parser.add_argument("--testFileDir","-i",
                        type=str,
                        help="specify the directory name of the input files")


    return vars(parser.parse_args())

def main():
    args = argParser()
    myResultMaker = resultMaker(args["testFileDir"],args["outputDir"])
    myResultMaker.runFiles()


if __name__ == "__main__":
    main()
