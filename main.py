from direct.showbase.ShowBase import ShowBase 
from panda3d.core import WindowProperties 
from panda3d.core import CollisionTraverser, CollisionSphere, CollisionNode, CollisionBox, CollisionHandlerQueue, CollisionHandlerPusher, CollisionRay
from panda3d.core import GraphicsWindow
from panda3d.core import NodePath
from panda3d.core import BitMask32
from panda3d.core import Vec3, Vec4
from panda3d.core import loadPrcFile
from direct.gui.OnscreenImage import OnscreenImage
import sys
from direct.actor.Actor import Actor
from gameobject import *
from panda3d.core import AmbientLight, DirectionalLight
from direct.gui.DirectGui import *

loadPrcFile('NEA-PANDA3D-from-vs/Config.prc')

class game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.properties()
        self.initMenu()
        self.collision()

    def collision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()


    def properties(self): #sets up game properties
        props = WindowProperties() #creates window properties
        props.setTitle('game') #name of app running
        props.setSize(800, 600) #sets display size
        base.win.requestProperties(props)
        base.disableMouse()
    
    def initMenu(self):
        self.startMenu()
    
    def startGame(self):
        print('starting game')
        self.destroyMenu()
        self.initEnvironment()
        self.initActor()
        self.Enemy = WalkingEnemy(Vec3(5,0,0)) # spawns an enemy at thre coords 5,0,0
        print(12)

    def update(self, task):
        dt = globalClock.getDt()
        self.Enemy.update(self.player, dt)
        return task.cont
    
    def exitGame(self):
        print('exiting game')
        self.destroy()
    
    def startMenu(self):
        self.start_frame = DirectFrame(frameSize=(-1, 1, -1, 1), frameColor=(0, 0, 0, 0.5))
        self.start_frame.setPos(0, 0, 0)

        start_button = DirectButton(text="Start Game", scale=0.1, command=self.startGame)
        start_button.setPos(0, 0, 0.2)
        start_button.reparentTo(self.start_frame)

        exit_button = DirectButton(text="Exit", scale=0.1, command=self.exitGame)
        exit_button.setPos(0, 0, -0.2)
        exit_button.reparentTo(self.start_frame)
    
    def destroyMenu(self):
        self.start_frame.destroy()

    def initEnvironment(self):
        self.environment1()

    def environment1(self):
        self.scene = self.loader.loadModel('environment/OldWestTerrain/OldWestTerrain.egg')
        #self.scene.setScale(1, 1, 1)
        self.scene.reparentTo(self.render)
        self.scene.setTwoSided(True)
        
    def initActor(self):
        self.actor = Player()
    

class Player(Actor):

    speed = 50
    FORWARD = Vec3(0,2,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-1,0,0)
    RIGHT = Vec3(1,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    readyToJump = False
    jump = 0

    
    def __init__(self):
        self.loadModel()
        self.setupCamera()
        self.collision()
        self.controls()
        #health - initial health, items in game that increase health,
        #weapon = Weapon(), argument dictates how strong the weapon is,

        taskMgr.add(self.mouseTask, 'mouse-update')
        taskMgr.add(self.moveTask, 'move-update')
        taskMgr.add(self.jumpTask, 'jump-update')
    
    def loadModel(self):
        self.player = NodePath('player')
        self.player.reparentTo(render)
        self.player.setPos(0, 10, 1)

    def setupCamera(self):
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.player)
    
    def collision(self):
        colliderNode = CollisionNode('player')
        colliderNode.addSolid(CollisionSphere(0,0,0,3))
        solid = self.player.attachNewNode(colliderNode)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.player, base.drive.node())

        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        colliderNode = CollisionNode('playerRay')
        colliderNode.addSolid(ray)
        colliderNode.setFromCollideMask(BitMask32.bit(1))   # Set from collide mask
        colliderNode.setIntoCollideMask(BitMask32.allOff())  # Set into collide mask
        solid = self.player.attachNewNode(colliderNode)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)

    
    def controls(self):
        base.accept('space', self.__setattr__, ['readyToJump', True])
        base.accept('space-up', self.__setattr__, ['readyToJump', False])
        base.accept( "w" , self.__setattr__,["walk",self.FORWARD])
        base.accept( "s" , self.__setattr__,["walk",self.BACK] )
        base.accept( "s-up" , self.__setattr__,["walk",self.STOP] )
        base.accept( "w-up" , self.__setattr__,["walk",self.STOP] )
        base.accept( "a" , self.__setattr__,["strafe",self.LEFT])
        base.accept( "d" , self.__setattr__,["strafe",self.RIGHT] )
        base.accept( "a-up" , self.__setattr__,["strafe",self.STOP] )
        base.accept( "d-up" , self.__setattr__,["strafe",self.STOP] )
        #base.accept("mouse1", self.__setattr__, ["shoot", True])
        #base.accept("mouse1-up", self.__setattr__, ["shoot", False])
            
    def mouseTask(self, task):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, base.win.getXSize()//2, base.win.getYSize()//2):
            self.player.setH(self.player.getH() - (x - base.win.getXSize()/2)*0.1)
            base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2)*0.1)
        return task.cont
    
    def moveTask(self,task):
        self.player.setPos(self.player,self.walk*globalClock.getDt()*self.speed)
        self.player.setPos(self.player,self.strafe*globalClock.getDt()*self.speed)
        return task.cont
    
    def jumpTask(self, task):
        # get the highest Z from the down casting ray
        highestZ = -100
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            if z > highestZ and entry.getIntoNode().getName() == "Cube":
                highestZ = z
        # gravity effects and jumps
        self.player.setZ(self.player.getZ()+self.jump*globalClock.getDt())
        self.jump -= 6*globalClock.getDt()
        if highestZ > self.player.getZ()-4:
            self.jump = 0
            self.player.setZ(highestZ+.3)
            if self.readyToJump:
                self.jump = 1
        return task.cont

app = game()
app.run()