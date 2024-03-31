from direct.showbase.ShowBase import ShowBase 
from panda3d.core import WindowProperties 
from panda3d.core import CollisionTraverser, CollisionSphere, CollisionNode, CollisionBox, CollisionHandlerQueue, CollisionHandlerPusher, CollisionRay
from panda3d.core import GraphicsWindow
from panda3d.core import NodePath
from panda3d.core import BitMask32
from panda3d.core import Vec3, Vec2
from panda3d.core import loadPrcFile
from direct.gui.OnscreenImage import OnscreenImage
import sys
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence
from direct.interval.FunctionInterval import Func
import random

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
        self.initEnemy()
    
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
    
    def initEnemy(self):
        self.enemy = Enemy(self.actor)

   
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
        self.player.setPos(0, 10, 2)

    def setupCamera(self):
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.player)
    
    def collision(self):
        colliderNode = CollisionNode('player')
        colliderNode.addSolid(CollisionSphere(0,0,0,4))
        solid = self.player.attachNewNode(colliderNode)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.player, base.drive.node())

        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        colliderNode = CollisionNode('playerRay')
        colliderNode.addSolid(ray)
        colliderNode.setFromCollideMask(BitMask32.bit(1)) 
        colliderNode.setIntoCollideMask(BitMask32.allOff())
        solid = self.player.attachNewNode(colliderNode)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)

    
    def controls(self):
        self.accept('escape', sys.exit)
        self.accept('space', self.__setattr__, ['readyToJump', True])
        self.accept('space-up', self.__setattr__, ['readyToJump', False])
        self.accept( "w" , self.__setattr__,["walk",self.FORWARD])
        self.accept( "s" , self.__setattr__,["walk",self.BACK] )
        self.accept( "s-up" , self.__setattr__,["walk",self.STOP] )
        self.accept( "w-up" , self.__setattr__,["walk",self.STOP] )
        self.accept( "a" , self.__setattr__,["strafe",self.LEFT])
        self.accept( "d" , self.__setattr__,["strafe",self.RIGHT] )
        self.accept( "a-up" , self.__setattr__,["strafe",self.STOP] )
        self.accept( "d-up" , self.__setattr__,["strafe",self.STOP] )
        #self.accept("mouse1", lambda: self.weapon.fire, self.enemyList)
        #self.accept("r", self.weapon.reload, ["shoot", False])
            
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
        if highestZ > self.player.getZ()-10:
            self.jump = 0
            self.player.setZ(highestZ+.3)
            if self.readyToJump:
                self.jump = 1
        return task.cont


class Enemy(Actor):
    
    def __init__(self, player):
        self.player = player
        self.enemy = Actor('models/panda-model.egg',
                           {'walk': 'models/panda-walk4'})
        self.enemy.setScale(0.009)
        pos = random.randint(-100,100)
        self.enemy.setPos(pos, pos, 1)
        self.enemy.reparentTo(render)
        self.enemy.loop('walk')
        self.followPlayer()
    
    def followPlayer(self):
        taskMgr.add(self.updateFollow, 'update follow', extraArgs=[self.player], appendTask=True)


    def updateFollow(self, player, task):
        directionToPlayer = player.player.getPos() - self.enemy.getPos()
        directionToPlayer.setZ(0)
        directionToPlayer.normalize()
        self.enemy.setPos(self.enemy.getPos() + directionToPlayer * 0.2)
        self.enemy.lookAt(player.player)
        return task.cont


class Weapon(DirectObject):
    def __init__(self, render, player, enemy_list):
        self.render = render
        self.player = player
        self.enemy_list = enemy_list
        self.accept("mouse1", self.fire, print('shoot'))
        

    def fire(self):
        bullet = Bullet(self.render, self.player.getPos(), "sprite.egg")
        bullet.move()
        bullet.detectCollision(self.enemy_list)


class Bullet:
    def __init__(self, render, start_pos, model_path):
        self.render = render
        self.bullet = loader.loadModel(model_path)  
        self.bullet.setPos(start_pos)
        self.bullet.reparentTo(self.render)

    def move(self):
        bullet_interval = self.bullet.posInterval(1, Vec3(10, 0, 0), startPos=self.bullet.getPos())
        bullet_sequence = Sequence(bullet_interval, Func(self.bullet.removeNode))
        bullet_sequence.start()

    def detectCollision(self, enemy_list):
        for enemy in enemy_list:
            if self.bullet.getPos(render).getX() == enemy.getPos(render).getX() and self.bullet.getPos(render).getY() == enemy.getPos(render).getY():
                enemy.removeNode()


app = game()
app.run()
