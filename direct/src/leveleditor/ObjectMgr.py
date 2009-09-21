"""
Defines ObjectMgr
"""

import os, time, wx

from direct.task import Task
from pandac.PandaModules import *

import ObjectGlobals as OG

class ObjectMgr:
    """ ObjectMgr will create, manage, update objects in the scene """
    
    def __init__(self, editor):
        self.editor = editor

        # main obj repository of objects in the scene
        self.objects = {}
        self.npIndex = {}
        self.saveData = []

        self.lastUid = ''
        self.lastUidMode = 0
        self.currNodePath = None   

    def reset(self):
        self.deselectAll()

        for id in self.objects.keys():
            self.objects[id][OG.OBJ_NP].removeNode()
            del self.objects[id]

        for np in self.npIndex.keys():
            del self.npIndex[np]
               
        self.objects = {}
        self.npIndex = {}
        self.saveData = []

    def genUniqueId(self):
        # [gjeon] to solve the problem of unproper $USERNAME
        userId = os.path.basename(os.path.expandvars('$USERNAME'))
        if userId == '':
            userId = base.config.GetString("le-user-id")
        if userId == '':
            userId = 'unknown'
        newUid = str(time.time()) + userId
        # prevent duplicates from being generated in the same frame (this can
        # happen when creating several new objects at once)
        if (self.lastUid == newUid):
            # append a value to the end to uniquify the id
            newUid = newUid + str(self.lastUidMod)
            self.lastUidMod = self.lastUidMod + 1
        else:
            self.lastUid = newUid
            self.lastUidMod = 0
        return newUid

    def addNewObject(self, typeName, uid = None, model = None, parent=None):
        """ function to add new obj to the scene """
        if parent is None:
            parent = render

        objDef = self.editor.objectPalette.findItem(typeName)
        newobj = None
        if objDef and type(objDef) != dict:
            if objDef.createFunction:
                funcName = objDef.createFunction[OG.FUNC_NAME]
                funcArgs = objDef.createFunction[OG.FUNC_ARGS]
                if funcName.startswith('.'):
                    # when it's using default objectHandler
                    func = Functor(eval("base.le.objectHandler%s"%funcName))
                else:
                    # when it's not using default objectHandler, whole name of the handling obj
                    # should be included in function name
                    func = Functor(eval(funcName))

                # create new obj using function and keyword arguments defined in ObjectPalette
                newobj = func(**funcArgs)

            elif objDef.model is not None:
                # since this obj is simple model let's load the model
                if model is None:
                    model = objDef.model
                newobj = loader.loadModel(model)

            if newobj is None:
                return None

            newobj.reparentTo(parent)
            newobj.setTag('OBJRoot','1')

            if uid is None:
                uid = self.genUniqueId()
                isLoadingArea = False
            else:
                isLoadingArea = True

            # populate obj data using default values
            properties = {}
            for key in objDef.properties.keys():
                properties[key] = objDef.properties[key][OG.PROP_DEFAULT]

            # insert obj data to main repository
            self.objects[uid] = [uid, newobj, objDef, model, properties]
            self.npIndex[NodePath(newobj)] = uid

            if not isLoadingArea:
                base.direct.select(newobj)

        return newobj

    def removeObjectByNodePath(self, nodePath):
        uid = self.npIndex.get(nodePath)
        if uid:
            del self.objects[uid]
            del self.npIndex[nodePath]

    def findObjectById(self, uid):
        return self.objects.get(uid)

    def findObjectByNodePath(self, nodePath):
        uid = self.npIndex.get(nodePath)
        if uid is None:
            return None
        else:
            return self.objects[uid]

    def deselectAll(self):
        self.currNodePath = None
        taskMgr.remove('_le_updateObjectUITask')
        self.editor.ui.objectPropertyUI.clearPropUI()

    def selectObject(self, nodePath):
        obj = self.findObjectByNodePath(nodePath)
        if obj is None:
            return

        self.currNodePath = obj[OG.OBJ_NP]
        self.spawnUpdateObjectUITask()
        self.updateObjectPropertyUI(obj)

    def updateObjectPropertyUI(self, obj):
        objDef = obj[OG.OBJ_DEF]
        objProp = obj[OG.OBJ_PROP]
        self.editor.ui.objectPropertyUI.updateProps(obj)

    def onEnterObjectPropUI(self, event):
        taskMgr.remove('_le_updateObjectUITask')        
        
    def onLeaveObjectPropUI(self, event):
        self.spawnUpdateObjectUITask()
        
    def spawnUpdateObjectUITask(self):
        if self.currNodePath is None:
            return

        taskMgr.remove('_le_updateObjectUITask')
        t = Task.Task(self.updateObjectUITask)
        t.np = self.currNodePath
        taskMgr.add(t, '_le_updateObjectUITask')
        
    def updateObjectUITask(self, state):
        self.editor.ui.objectPropertyUI.propX.setValue(state.np.getX())
        self.editor.ui.objectPropertyUI.propY.setValue(state.np.getY())
        self.editor.ui.objectPropertyUI.propZ.setValue(state.np.getZ())

        h = state.np.getH()
        while h < 0:
            h = h + 360.0

        while h > 360:
            h = h - 360.0

        p = state.np.getP()
        while p < 0:
            p = p + 360.0

        while p > 360:
            p = p - 360.0

        r = state.np.getR()
        while r < 0:
            r = r + 360.0

        while r > 360:
            r = r - 360.0 
            
        self.editor.ui.objectPropertyUI.propH.setValue(h)
        self.editor.ui.objectPropertyUI.propP.setValue(p)
        self.editor.ui.objectPropertyUI.propR.setValue(r)        

        self.editor.ui.objectPropertyUI.propSX.setValue(state.np.getSx())
        self.editor.ui.objectPropertyUI.propSY.setValue(state.np.getSy())
        self.editor.ui.objectPropertyUI.propSZ.setValue(state.np.getSz())
        
        return Task.cont
        
    def updateObjectTransform(self, event):
        if self.currNodePath is None:
            return

        np = self.currNodePath
        np.setX(float(self.editor.ui.objectPropertyUI.propX.getValue()))
        np.setY(float(self.editor.ui.objectPropertyUI.propY.getValue()))
        np.setZ(float(self.editor.ui.objectPropertyUI.propZ.getValue()))

        h = float(self.editor.ui.objectPropertyUI.propH.getValue())
        while h < 0:
            h = h + 360.0

        while h > 360:
            h = h - 360.0

        p = float(self.editor.ui.objectPropertyUI.propP.getValue())
        while p < 0:
            p = p + 360.0

        while p > 360:
            p = p - 360.0

        r = float(self.editor.ui.objectPropertyUI.propR.getValue())
        while r < 0:
            r = r + 360.0

        while r > 360:
            r = r - 360.0 
            
        np.setH(h)
        np.setP(p)
        np.setR(r)

        np.setSx(float(self.editor.ui.objectPropertyUI.propSX.getValue()))
        np.setSy(float(self.editor.ui.objectPropertyUI.propSY.getValue()))
        np.setSz(float(self.editor.ui.objectPropertyUI.propSZ.getValue()))        

    def updateObjectModel(self, event, obj):
        """ replace object's model """
        model = event.GetString()
        if model is None:
            return

        if obj[OG.OBJ_MODEL] != model:
            base.direct.deselectAll()

            objNP = obj[OG.OBJ_NP]

            # load new model
            newobj = loader.loadModel(model)
            newobj.setTag('OBJRoot','1')

            # reparent children
            objNP.findAllMatches("=OBJRoot").reparentTo(newobj)
            
            # reparent to parent
            newobj.reparentTo(objNP.getParent())

            # copy transform
            newobj.setPos(objNP.getPos())
            newobj.setHpr(objNP.getHpr())
            newobj.setScale(objNP.getScale())

            # delete old geom
            del self.npIndex[NodePath(objNP)]
            objNP.removeNode()

            # register new geom
            obj[OG.OBJ_NP] = newobj
            obj[OG.OBJ_MODEL] = model
            self.npIndex[NodePath(newobj)] = obj[OG.OBJ_UID]
            
            base.direct.select(newobj)        

    def updateObjectProperty(self, event, obj, propName):
        """
        When an obj's property is updated in UI,
        this will update it's value in data structure.
        And call update function if defined.        
        """
        
        objDef = obj[OG.OBJ_DEF]
        objProp = obj[OG.OBJ_PROP]
        
        propDef = objDef.properties[propName]
        if propDef is None:
            return

        propType = propDef[OG.PROP_TYPE]
        propDataType = propDef[OG.PROP_DATATYPE]
        
        if propType == OG.PROP_UI_SLIDE:
            if len(propDef) <= OG.PROP_RANGE:
                return

            strVal = event.GetString()
            if strVal == '':
                min = float(propDef[OG.PROP_RANGE][OG.RANGE_MIN])
                max = float(propDef[OG.PROP_RANGE][OG.RANGE_MAX])
                intVal = event.GetInt()
                if intVal is None:
                    return
                val = intVal / 100.0 * (max - min) + min
            else:
                val = strVal

        elif propType == OG.PROP_UI_ENTRY:
            val = event.GetString()

        elif propType == OG.PROP_UI_SPIN:
            val = event.GetInt()

        elif propType == OG.PROP_UI_CHECK:
            if event.GetInt():
                val = True
            else:
                val = False

        elif propType == OG.PROP_UI_RADIO:
            val = event.GetString()

        elif propType == OG.PROP_UI_COMBO:
            val = event.GetString()

        else:
            # unsupported property type
            return

        # now update object prop value and call update function
        self.updateObjectPropValue(obj, propName, val)

    def updateObjectPropValue(self, obj, propName, val):
        """
        Update object property value and
        call update function if defined.         
        """
        
        objDef = obj[OG.OBJ_DEF]
        objProp = obj[OG.OBJ_PROP]
        
        propDef = objDef.properties[propName]
        propDataType = propDef[OG.PROP_DATATYPE]

        val = OG.TYPE_CONV[propDataType](val)
        objProp[propName] = val

        if propDef[OG.PROP_FUNC] is None:
            return
        
        funcName = propDef[OG.PROP_FUNC][OG.FUNC_NAME]
        funcArgs = propDef[OG.PROP_FUNC][OG.FUNC_ARGS]

        if funcName.startswith('.'):
            func = Functor(eval("base.le.objectHandler%s"%funcName))
        else:
            func = Functor(eval(funcName))

        # populate keyword arguments
        kwargs = {}
        for key in funcArgs.keys():
            if funcArgs[key] == OG.ARG_VAL:
                kwargs[key] = val
            elif funcArgs[key] == OG.ARG_OBJ:
                kwargs[key] = obj
            else:
                kwargs[key] = funcArgs[key]

        # finally call update function
        func(**kwargs)

    def updateObjectProperties(self, nodePath, propValues):
        """
        When a saved level is loaded,
        update an object's properties
        And call update function if defined.
        """

        obj = self.findObjectByNodePath(nodePath)
        if obj:
            for propName in propValues:
                self.updateObjectPropValue(obj, propName, propValues[propName])

    def traverse(self, parent, parentId = None):
        """
        Trasverse scene graph to gather data for saving
        """
        
        for child in parent.getChildren():
            if child.hasTag('OBJRoot'):
                obj = self.findObjectByNodePath(child)

                if obj:
                    uid = obj[OG.OBJ_UID]
                    np = obj[OG.OBJ_NP]
                    objDef = obj[OG.OBJ_DEF]
                    objModel = obj[OG.OBJ_MODEL]
                    objProp = obj[OG.OBJ_PROP]

                    if parentId:
                        parentStr = "objects['%s']"%parentId
                    else:
                        parentStr = "None"

                    if objModel is None:
                        self.saveData.append("\nobjects['%s'] = objectMgr.addNewObject('%s', '%s', None, %s)"%(uid, objDef.name, uid, parentStr))
                    else:
                        self.saveData.append("\nobjects['%s'] = objectMgr.addNewObject('%s', '%s', '%s', %s)"%(uid, objDef.name, uid, objModel, parentStr))
                    self.saveData.append("if objects['%s']:"%uid)
                    self.saveData.append("    objects['%s'].setPos(%s)"%(uid, np.getPos()))
                    self.saveData.append("    objects['%s'].setHpr(%s)"%(uid, np.getHpr()))
                    self.saveData.append("    objects['%s'].setScale(%s)"%(uid, np.getScale()))
                    self.saveData.append("    objectMgr.updateObjectProperties(objects['%s'], %s)"%(uid,objProp))
                    
                self.traverse(child, uid)

    def getSaveData(self):
        self.saveData = []
        self.traverse(render)
        return self.saveData
    
    