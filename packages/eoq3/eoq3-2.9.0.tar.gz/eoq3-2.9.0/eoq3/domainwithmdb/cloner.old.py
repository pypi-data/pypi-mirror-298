'''
Helper class for CmdRunner to clone elements according to different modes.
 
Bjoern Annighoefer 2022
'''


from ..command import CLO_MODES
from ..concepts import M1OBJECT, M2CLASS, M2ATTRIBUTE, M2ASSOCIATION, M2COMPOSITION
from ..value import STR,I64,NON
from .util import IsList

class Cloner:
    def __init__(self,cmdrunner,logger):
        self.cmdrunner = cmdrunner
        self.logger = logger
        
    def Clone(self, obj, mode, tid):
        clone = NON()
        if(CLO_MODES.CLS==mode):
            (clone,clazz) = self.__ECloneClass(obj,tid)
        elif(CLO_MODES.ATT==mode):
            (clone,clazz) = self.__ECloneAttributes(obj,tid)
        elif(CLO_MODES.FLT==mode):
            (clone,clazz) = self.__ECloneFlat(obj,tid)
        elif(CLO_MODES.FUL==mode):
            (clone,clazz) = self.__ECloneFull(obj,tid)
        elif(CLO_MODES.DEP==mode):
            (clone,clazz) = self.__ECloneDeep(obj,tid)
        return clone
        
    def __ECloneClass(self,obj,tid):
        clazz = self.cmdrunner._MdbRead(tid,obj,STR(M1OBJECT.CLASS))
        #classId = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ID))
        clone = self.cmdrunner._MdbCreate(tid,clazz)
        return (clone,clazz)
    
    def __ECloneAttributes(self,obj,tid):
        (clone,clazz) = self.__ECloneClass(obj,tid)
        #attributes
        attributes = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLATTRIBUTES))
        for attribute in attributes:
            featureName = self.cmdrunner._MdbRead(tid,attribute,STR(M2ATTRIBUTE.NAME))
            value = self.cmdrunner._MdbRead(tid,obj,featureName)
            if(IsList(value)):
                for v in value:
                    self.cmdrunner._MdbUpdate(tid,clone,featureName,v,I64(-1))
            elif(value): #do not copy empty single value features
                self.cmdrunner._MdbUpdate(tid,clone,featureName,value)
        return (clone,clazz)
    
    def __ECloneFlat(self,obj,tid):
        (clone,clazz) = self.__ECloneAttributes(obj,tid)
        associations = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLSRCASSOCIATIONS))
        for association in associations:
            srcType = self.cmdrunner._MdbRead(tid,association,STR(M2ASSOCIATION.SRCCLASS))
            if(srcType == clazz): #prevent cloning references in the opposite direction
                featureName = self.cmdrunner._MdbRead(tid,association,STR(M2ASSOCIATION.DSTNAME))
                value = self.cmdrunner._MdbRead(tid,obj,featureName)
                if(IsList(value)):
                    for v in value:
                        self.cmdrunner._MdbUpdate(tid,clone,featureName,v,I64(-1))
                elif(value): #do not copy empty single value features
                    self.cmdrunner._MdbUpdate(tid,clone,featureName,value)
        return (clone,clazz)
    
    def __ECloneDeep(self,obj,tid,copyReferences=True,clonedElementLut={}):
        (clone,clazz) = self.__ECloneAttributes(obj,tid)
        clonedElementLut[obj.v[0].v[0]] = clone #remember what elements have been cloned
        compositions = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLSRCCOMPOSITIONS))
        for composition in compositions:
            featureName = self.cmdrunner._MdbRead(tid,composition,STR(M2COMPOSITION.NAME))
            children = self.cmdrunner._MdbRead(tid,obj,featureName)
            if(IsList(children)):
                for child in children:
                    (clonedChild,childClass) = self.__ECloneDeep(child,tid,copyReferences,clonedElementLut)
                    self.cmdrunner._MdbUpdate(tid,clone,featureName,clonedChild,I64(-1))
            elif(children): #do not copy empty single value features
                (clonedChild,childClass) = self.__ECloneDeep(children,tid,copyReferences,clonedElementLut)
                self.cmdrunner._MdbUpdate(tid,clone,featureName,clonedChild)
        if(copyReferences): #non containments
            associations = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLSRCASSOCIATIONS))
            for association in associations:
                featureName = self.cmdrunner._MdbRead(tid,association,STR(M2ASSOCIATION.DSTNAME))
                value = self.cmdrunner._MdbRead(tid,obj,featureName)
                if(IsList(value)):
                    for v in value:
                        self.cmdrunner._MdbUpdate(tid,clone,featureName,v,I64(-1))
                elif(value): #do not copy empty single value features
                    self.cmdrunner._MdbUpdate(tid,clone,featureName,value)
            
        return (clone,clazz)
    
    def __ECloneFull(self,obj,tid):
        clonedElementLut = {}
        (clone,clazz) = self.__ECloneDeep(obj,tid,False,clonedElementLut)
        self.__ECloneFullReferenceUpdater(obj,tid,clonedElementLut)            
        return (clone,clazz)
    
    def __ECloneFullReferenceUpdater(self,obj,tid,clonedElementLut):
        clazz = self.cmdrunner._MdbRead(tid,obj,STR(M1OBJECT.CLASS))
        #iterate through all children
        compositions = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLSRCCOMPOSITIONS))
        for composition in compositions:
            featureName = self.cmdrunner._MdbRead(tid,composition,STR(M2COMPOSITION.NAME))
            children = self.cmdrunner._MdbRead(tid,obj,featureName)
            if(IsList(children)):
                for child in children:
                    self.__ECloneFullReferenceUpdater(child,tid,clonedElementLut)
            elif(children): #do not copy empty single value features
                self.__ECloneFullReferenceUpdater(children,tid,clonedElementLut)
        #set the references accordingly
        clone = clonedElementLut[obj.v[0].v[0]]
        associations = self.cmdrunner._MdbRead(tid,clazz,STR(M2CLASS.ALLSRCASSOCIATIONS))
        for association in associations:
            featureName = self.cmdrunner._MdbRead(tid,association,STR(M2ASSOCIATION.DSTNAME))
            value = self.cmdrunner._MdbRead(tid,obj,featureName)
            if(IsList(value)):
                for v in value:
                    ref = self.__ECloneFullFindCorrespondingReference(v, clonedElementLut)
                    self.cmdrunner._MdbUpdate(tid,clone,featureName,ref,I64(-1))
            elif(value): #do not copy empty single value features
                ref = self.__ECloneFullFindCorrespondingReference(value, clonedElementLut)
                self.cmdrunner._MdbUpdate(tid,clone,featureName,ref)
        

    
    def __ECloneFullFindCorrespondingReference(self,obj,clonedElementLut):
        if(obj.v[0].v[0] in clonedElementLut):
            return clonedElementLut[obj.v[0].v[0]]
        else:
            return obj
