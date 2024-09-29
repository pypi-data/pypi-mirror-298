'''
Helper class for CmdRunner to delete elements according to different modes.
 
Bjoern Annighoefer 2022
'''

from ..concepts import M1OBJECT, M2CLASS, M2COMPOSITION
from ..value import STR, NON, LST
from .util import IsList

from typing import Tuple


class Deleter:
    def __init__(self,cmdrunner,logger):
        self.cmdrunner = cmdrunner
        self.logger = logger
        
    def DeleteAuto(self, target, tid)->Tuple[STR,LST,LST]:
        selfType = self.cmdrunner._MdbRead(tid,target,STR(M1OBJECT.CLASS))
        associates = self.cmdrunner._MdbRead(tid,target,STR(M1OBJECT.ASSOCIATES))
        #remove all associates
        for a in associates:
            self.cmdrunner._MdbUpdate(tid,a[0],a[3],NON(),a[2])
        #remove from parent 
        c = self.cmdrunner._MdbRead(tid,target,STR(M1OBJECT.PARENT))
        if(c[0]):
            featureName = self.cmdrunner._MdbRead(tid,c[1],STR(M2COMPOSITION.NAME))
            self.cmdrunner._MdbUpdate(tid,c[0],featureName,NON(),c[2])
        #now element can be deleted from mdb
        return self.cmdrunner._MdbDelete(tid,target)
        
        
    def DeleteFull(self, target, tid)->Tuple[STR,LST,LST]:
        clazz = self.cmdrunner._MdbRead(tid,target,STR(M1OBJECT.CLASS))
        compositions = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLSRCCOMPOSITIONS))
        for c in compositions:
            cname = self.cmdrunner._MdbRead(tid,c,STR(M2COMPOSITION.NAME))
            children = self.cmdrunner._MdbRead(tid,target,cname)
            if(IsList(children)):
                #remove children from parent
                nChildren = len(children)
                for i in range(nChildren-1,-1,-1):
                    child = children[i]
                    self.DeleteFull(child,tid)
            elif(not children.IsNone()): 
                self.DeleteFull(children,tid)
        return self.DeleteAuto(target,tid)