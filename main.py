from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionSphere, CollisionNode, CollisionBox, CollisionHandlerQueue, CollisionHandlerPusher, CollisionRay
from panda3d.core import GraphicsWindow
from panda3d.core import NodePath
from panda3d.core import BitMask32
from panda3d.core import Vec3
from panda3d.core import loadPrcFile
from direct.gui.OnscreenImage import OnscreenImage
import sys
from direct.actor.Actor import Actor
#from actors import character1

loadPrcFile('config.prc')

def degToRad(degrees):
    return degrees * (pi / 180.0)

class WashingtonBullets(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.properties()
        self.collision()
        self.enviroment1()
        self.initPlayer()
    
    '''HERE LIES DEY BASIC INIT CODE FOR DEM MAN BHAD GAME! SKELETON TING!'''

    def properties(self): #sets up game properties
        props = WindowProperties() #creates window properties
        props.setTitle('Washington Bullets') #name of app running
        props.setSize(800, 600) #sets display size
        base.win.requestProperties(props)
        props.setCursorHidden(True)
        base.disableMouse()


    def collision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()

    def enviroment1(self):
        self.scene = self.loader.loadModel('enviroment/maps/bedroom.egg')
        #self.scene.setScale(1, 1, 1)
        self.scene.reparentTo(self.render)
        self.scene.setTwoSided(True)
    
    def initPlayer(self):
        self.node = Player()


class Player(object):

    speed = 20
    FORWARD = Vec3(0,1,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-1,0,0)
    RIGHT = Vec3(1,0,0)
    STOP = Vec3(0)
    walk = STOP

    def __init__(self):
        self.loadModel()
        self.setupCamera()
        self.createCollisions()
        self.controls()

        taskMgr.add(self.mouseTask, 'mouse-update')
        taskMgr.add(self.moveTask, 'move-update')
    
    def loadModel(self):
        self.node = NodePath('player')
        self.node.reparentTo(render)
        self.node.setPos(0, 0, 7)

    def setupCamera(self):
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.node)
    
    def createCollisions(self):
        cn = CollisionNode('player')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.node, base.drive.node())

        ray = CollisionRay()
        ray.setOrigin(0,0,0)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('player')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
    
    def controls(self):
        base.accept('escape', self.mouseRelease)
        base.accept('mouse1', self.mouseInGame)

        base.accept('w', self.__setattr__, ['walk', self.FORWARD])
        base.accept('w-up', self.__setattr__, ['walk', self.STOP])
        base.accept('a', self.__setattr__, ['walk', self.LEFT])
        base.accept('a-up', self.__setattr__, ['walk', self.STOP])
        base.accept('s', self.__setattr__, ['walk', self.BACK])
        base.accept('s-up', self.__setattr__, ['walk', self.STOP])
        base.accept('d', self.__setattr__, ['walk', self.RIGHT])
        base.accept('d-up', self.__setattr__, ['walk', self.STOP])
    
    def mouseTask(self, task):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, base.win.getXSize()//2, base.win.getYSize()//2):
            self.node.setH(self.node.getH() - (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
        return task.cont
    
    def moveTask(self,task):
        self.node.setPos(self.node,self.walk*globalClock.getDt()*self.speed)
        return task.cont
        
    #def updateKeyMap(self, key, value):
        #self.keyMap[key] = value

    def mouseInGame(self): #takes mouse input in game
        self.cameraSwingActivated = True
        props = WindowProperties()
        props.setCursorHidden(True) #hides cursor
        self.win.requestProperties(props)

    def mouseRelease(self):
        props = WindowProperties()
        props.setCursorHidden(False) #shows cursor
        self.win.requestProperties(props)


app = WashingtonBullets()
app.run()