#!/usr/bin/python3

import os,sys

PATH = '../downloads/soc-pokec-'
PATH_PROFILES = PATH+'profiles.txt'
PATH_PROFILES_GZ = PATH_PROFILES+'.gz'
PATH_PROFILES_OLD = PATH+'profiles-old.txt'
PATH_PROFILES_OLD_GZ = PATH_PROFILES_OLD+'.gz'
PATH_PROFILES_REDUCE = PATH+'profiles-red.txt'
PATH_PROFILES_REDUCE_GZ = PATH_PROFILES_REDUCE+'.gz'

PATH_RELATION = PATH+'relationships.txt'
PATH_RELATION_GZ = PATH_RELATION+'.gz'
PATH_RELATION_OLD = PATH+'relationships-old.txt'
PATH_RELATION_OLD_GZ = PATH_RELATION_OLD+'.gz'
PATH_RELATION_REDUCE = PATH+'relationships-red.txt'
PATH_RELATION_REDUCE_GZ = PATH_RELATION_REDUCE+'.gz'

GZIP   = 1
GZIPD  = 2
RENAME = 3
SET    = 4
REMOVE = 5

PROFILE  = 0
RELATION = 1
OLD      = 2


class Reducer:
    def __init__(self):
        self.user_av = set()

    def _relation(self):
        self._gzip(PATH_RELATION_GZ)
        with open(PATH_RELATION_REDUCE,"w") as r:
            with open(PATH_RELATION) as f:
                line = f.readline()
                while line:
                    int_line = line.split('\t')
                    int_line[1] = int_line[1].rstrip()
                    #print("int_line => {}  first => {}  second => {}".format(int_line,int_line[0],int_line[1]))
                    if int_line[0] in self.user_av and int_line[1] in self.user_av:
                        r.write(int_line[0]+'\t'+int_line[1]+'\n')
                    line = f.readline()
                f.close()
            r.close()
        self._rename(RELATION)
        self._gzip(PATH_RELATION,0)

    def profile(self,d=0):
        self._gzip(PATH_PROFILES_GZ)
        with open(PATH_PROFILES_REDUCE,"w") as r:
            with open(PATH_PROFILES) as f:
                line = f.readline()
                if not d:
                    while line:
                        int_line = line.split('\t')[:8]
                        self.user_av.add(int_line[0])
                        r.write('\t'.join(int_line)+'\n')
                        line = f.readline()
                else:
                    while line and d:
                        int_line = line.split('\t')[:8]
                        self.user_av.add(int_line[0])
                        r.write('\t'.join(int_line)+'\n')
                        line = f.readline()
                        d -= 1
                f.close()
            r.close()
        self._rename(PROFILE)
        self._gzip(PATH_PROFILES,0)
        self._log(SET,0,0,0)
        self._relation()
    
    def profile_complet(self,d=0):
        self._gzip(PATH_PROFILES_GZ)
        with open(PATH_PROFILES_REDUCE,"w") as r:
            with open(PATH_PROFILES) as f:
                line = f.readline()
                if not d:
                    while line:
                        int_line = line.split('\t')
                        self.user_av.add(int_line[0])
                        r.write('\t'.join(int_line)+'\n')
                        line = f.readline()
                else:
                    while line and d:
                        int_line = line.split('\t')[:8]
                        self.user_av.add(int_line[0])
                        r.write('\t'.join(int_line)+'\n')
                        line = f.readline()
                        d -= 1
                f.close()
            r.close()
        self._rename(PROFILE)
        self._gzip(PATH_PROFILES,0)
        self._log(SET,0,0,0)
        self._relation()

    def _rename(self,switch):
        if switch == PROFILE:
            self._log(RENAME,PATH_PROFILES,PATH_PROFILES_OLD)
            os.rename(PATH_PROFILES,PATH_PROFILES_OLD)
            self._gzip(PATH_PROFILES_OLD,0)
            self._log(RENAME,PATH_PROFILES_REDUCE,PATH_PROFILES)
            os.rename(PATH_PROFILES_REDUCE,PATH_PROFILES)
        elif switch == RELATION:
            self._log(RENAME,PATH_RELATION,PATH_RELATION_OLD)
            os.rename(PATH_RELATION,PATH_RELATION_OLD)
            self._gzip(PATH_RELATION_OLD,0)
            self._log(RENAME,PATH_RELATION_REDUCE,PATH_RELATION)
            os.rename(PATH_RELATION_REDUCE,PATH_RELATION)
        elif switch == OLD:
            self._log(RENAME,PATH_PROFILES_OLD_GZ,PATH_PROFILES_GZ)
            os.rename(PATH_PROFILES_OLD_GZ,PATH_PROFILES_GZ)
            self._log(RENAME,PATH_RELATION_OLD_GZ,PATH_RELATION_GZ)
            os.rename(PATH_RELATION_OLD_GZ,PATH_RELATION_GZ)

    def _gzip(self,f,d=1):
        if d:
            self._log(GZIPD,f)
            gzip = 'gzip -d ' + f
        else:
            self._log(GZIP,f)
            gzip = 'gzip '+f
        os.system(gzip)

    def reset_state(self):
        self._log(REMOVE,PATH_PROFILES_GZ)
        os.remove(PATH_PROFILES_GZ)
        self._log(REMOVE,PATH_RELATION_GZ)
        os.remove(PATH_RELATION_GZ)
        self._rename(OLD)
        self._log(REMOVE,"../downloads/soc-pokec-*-neo4j.txt.gz")
        os.system("rm ../downloads/soc-pokec-*-neo4j.txt.gz")
        self._log(REMOVE,"../downloads/*.txt")
        os.system("rm ../downloads/*.txt")
        self._log(REMOVE,"../downloads/neo4jTar")
        os.system("rm -r ../downloads/neo4jTar")

    
    def _log(self,meth,f1=None,f2=None,d=0):
        if meth == GZIP:
            print("compressing file {}".format(f1))
        if meth == GZIPD:
            print("decompressing file {}".format(f1))
        if meth == RENAME:
            print("Rename file {} to {}".format(f1,f2))
        if meth == SET:
            print("set contains {} elements".format(len(self.user_av)))
            if d < 0:
                for x in self.user_av:
                    print(x)
        if meth == REMOVE:
            print("Removing file {}".format(f1))
    
    def test(self):
        d = 20
        mock_set = set('123')
        print(mock_set)
        with open(PATH_RELATION_REDUCE,"w") as r:
            with open(PATH_RELATION) as f:
                line = f.readline()
                while line and d:
                    int_line = line.split('\t')
                    int_line[1] = int_line[1].rstrip()
                    print("int_line => {}  first => {}  second => {}".format(int_line,int_line[0],int_line[1]))
                    if int_line[0] in mock_set:
                        print("first")
                        if int_line[1] in mock_set:
                            print("second")
                            r.write('\t'.join(line)+'\n')
                    line = f.readline()
                    d -= 1
                f.close()
            r.close()




if __name__ == "__main__":
    r = Reducer()
    if sys.argv[1] == str(-1):
        r.reset_state()
        exit(0)
    if sys.argv[1] == str(-2):
        r.test()
        exit(0) 
    else:
        r.profile_complet(int(sys.argv[1]))
        exit(0)
    
    
    