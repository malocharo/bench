#!/usr/bin/python3

import os,sys,random,json

DATA_PATH = "../downloads/"
PROFILE= "soc-pokec-profiles-"
NEO4J = "neo4j.txt"
ARANGO = "arangodb.yxy"
GZ = ".gz"
OLD = ".old"
PATH_NEO4J_PROFILE = DATA_PATH + PROFILE + NEO4J
PATH_NEO4J_PROFILE_GZ = PATH_NEO4J_PROFILE + GZ
PATH_NEO4J_PROFILE_OLD = PATH_NEO4J_PROFILE + OLD
PATH_NEO4J_PROFILE_OLD_GZ = PATH_NEO4J_PROFILE_OLD + GZ

PATH_ARANGODB_PROFILE = DATA_PATH + PROFILE + ARANGO
PATH_ARANGODB_PROFILE_GZ = PATH_ARANGODB_PROFILE + GZ
PATH_ARANGODB_PROFILE_OLD = PATH_ARANGODB_PROFILE + OLD
PATH_ARANGODB_PROFILE_OLD_GZ = PATH_ARANGODB_PROFILE_OLD + GZ

PATH_SHORTEST1000 = "../data/shortest1000.json"
PATH_WARMUP       = "../data/warmup1000.json"
PATH_IDS          = "../data/ids100000.json"

GZIP   = 1
GZIPD  = 2
RENAME = 3
LIST   = 4
REMOVE = 5


class BenchRandomize:
    def __init__(self,db):
        self.node_list = []
        self.bodies_list = []
        self._fillList(db)
    
    def _fillList(self,db):
        if db == "neo4j":
            self._gzip(PATH_NEO4J_PROFILE_GZ,1)
            with open(PATH_NEO4J_PROFILE) as f:
                line = f.readline()
            while line:
                self.bodies_list.append(line)
                split_line = line.split('\t')
                self.node_list.append(split_line[0])
                line = f.readline()
            f.close()
            self._gzip(PATH_NEO4J_PROFILE)
        elif db == "shortest":
            self._gzip(PATH_ARANGODB_PROFILE_GZ,1)
            with open(PATH_ARANGODB_PROFILE) as f:
                line = f.readline()
            while line:
                self.bodies_list.append(line)
                split_line = line.split('\t')
                self.node_list.append(split_line[0])
                line = f.readline()
            f.close()
            self._gzip(PATH_NEO4J_PROFILE)
            
        
    
    def shortest(self,nb=1000):
        print(len(self.node_list))
        rand_list = random.sample(self.node_list,nb*2)
        self._rename(PATH_SHORTEST1000,"../data/shortest1000-old.json")
        with open(PATH_SHORTEST1000,"w") as f:
            i = 0
            f.write("[\n")
            while i<((nb*2)-2):
                line = '{\"from\":\"'+rand_list[i]+'\",\"to\":\"'+rand_list[i+1]+'\"},\n'
                f.write(line)
                i += 2
            line = '{\"from\":\"'+rand_list[i]+'\",\"to\":\"'+rand_list[i+1]+'\"}\n'
            f.write(line)
            f.write("]")
            f.close()
    

    def warmup(self,nb=1000):
        rand_list = random.sample(self.node_list,nb*2)
        self._rename(PATH_WARMUP,"../data/warmup1000-old.json")
        with open(PATH_WARMUP,"w") as f:
            f.write(json.dumps(rand_list))
            f.close()

    def warmupReset(self):
        self._log(REMOVE,PATH_WARMUP)
        os.remove(PATH_WARMUP)
        self._rename("../data/warmup1000-old.json",PATH_WARMUP)

    def shortestReset(self):
        self._log(REMOVE,PATH_SHORTEST1000)
        os.remove(PATH_SHORTEST1000)
        self._rename("../data/shortest1000-old.json",PATH_SHORTEST1000)

    def ids(self,nb):
        rand_list = random.sample(self.node_list,nb)
        self._rename(PATH_IDS,"../data/ids100000-old.json")
        with open(PATH_IDS,"w") as f:
            f.write(json.dumps(rand_list))
            f.close()

    def idsReset(self):
        self._log(REMOVE,PATH_IDS)
        os.remove(PATH_IDS)
        self._rename("../data/ids100000-old.json",PATH_IDS)



    def _gzip(self,f,d=0):
        if d:
            self._log(GZIPD,f)
            gzip = 'gzip -d ' + f
        else:
            self._log(GZIP,f)
            gzip = 'gzip '+f
        os.system(gzip)
    
    def _rename(self,f1,f2):
        self._log(RENAME,f1,f2)
        os.rename(f1,f2)
        
    
    def _log(self,meth,f1=None,f2=None,d=0):
        if meth == GZIP:
            print("compressing file {}".format(f1))
        if meth == GZIPD:
            print("decompressing file {}".format(f1))
        if meth == RENAME:
            print("Rename file {} to {}".format(f1,f2))
        if meth == REMOVE:
            print("Remove file {}".format(f1))
        if meth == LIST:
            print("List contains {}".format(len(self.node_list)))
        
if __name__ == "__main__":
    r = BenchRandomize(sys.argv[1])
    if sys.argv[2] == "shortest":
        if len(sys.argv) == 3:
            r.shortest()
        elif int(sys.argv[3]) < int(0):
            r.shortestReset()
        else:
            r.shortest(int(sys.argv[3]))
    elif sys.argv[2] == "ids":
        if int(sys.argv[3]) > 0:
            r.ids(int(sys.argv[3]))
        else:
            r.idsReset()