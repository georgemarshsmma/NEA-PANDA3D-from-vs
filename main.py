from direct.showbase.ShowBase import ShowBase 
from panda3d.core import WindowProperties 
from panda3d.core import CollisionTraverser, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionHandlerPusher, CollisionRay
from panda3d.core import NodePath
from panda3d.core import BitMask32
from panda3d.core import Vec3
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from panda3d.core import Point3
from panda3d.core import TextNode
import sys
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
import random

class game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.collision()
        self.properties()
        self.initMenu()

    def collision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()

    def properties(self):
        base.disableMouse()
        props = WindowProperties()
        props.setTitle('game')
        props.setSize(800, 600)
        base.win.requestProperties(props)

    def initMenu(self):
        self.startMenu()

    def exitGame(self):
        print('exiting game')
        sys.exit()

    def startMenu(self):
        self.startFrame = DirectFrame(frameSize=(-1, 1, -1, 1), frameColor=(0, 0, 0, 0.5))
        self.startFrame.setPos(0, 0, 0)

        map1Button = DirectButton(text='Map 1', scale=0.1, command=self.startGameMap1)
        map1Button.setPos(0, 0, 0.4)
        map1Button.reparentTo(self.startFrame)

        map2Button = DirectButton(text='Map 2', scale=0.1, command=self.startGameMap2)
        map2Button.setPos(0, 0, 0)
        map2Button.reparentTo(self.startFrame)

        map3Button = DirectButton(text='Map 3', scale=0.1, command=self.startGameMap3)
        map3Button.setPos(0, 0, -0.4)
        map3Button.reparentTo(self.startFrame)

        exitButton = DirectButton(text='Exit', scale=0.1, command=self.exitGame)
        exitButton.setPos(0, 0, -0.8)
        exitButton.reparentTo(self.startFrame)

    def destroyMenu(self):
        self.startFrame.destroy()

    def initEnvironment1(self):
        self.environment1()
    
    def initEnvironment2(self):
        self.environment2()
    
    def initEnvironment3(self):
        self.environment3()

    def environment1(self):
        self.scene = self.loader.loadModel('environment/OldWestTerrain/OldWestTerrain.egg')
        self.scene.reparentTo(self.render)
        self.scene.setTwoSided(True)
    
    def environment2(self):
        self.scene = self.loader.loadModel('environment/Cafeteria/Cafeteria.egg')
        self.scene.setScale(0.06, 0.06, 0.06)
        self.scene.reparentTo(self.render)
        self.scene.setTwoSided(True)
    
    def environment3(self):
        pass

    def initActor(self):
        self.actor = Player()

    def initEnemy(self):
        self.enemy = Enemy(self.actor)

    def startGameMap1(self):
        print('starting game - Map 1')
        self.destroyMenu()
        self.initEnvironment1()
        self.initActor()
        self.initEnemy()

    def startGameMap2(self):
        print('starting game - Map 2')
        self.destroyMenu()
        self.initEnvironment2()
        self.initActor()
        self.initEnemy()

    def startGameMap3(self):
        print('starting game - Map 3')
        self.destroyMenu()
        self.initEnvironment3()
        self.initActor()
        self.initEnemy()

    
class Player(Actor):

    speed = 50
    FORWARD = Vec3(0,2,0)
    BACK = Vec3(0,-1,0)
    LEFT = Vec3(-1,0,0)
    RIGHT = Vec3(1,0,0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    GRAVITY = 9.8
    health = 100

    
    def __init__(self):
        self.loadModel()
        self.setupCamera()
        self.collision()
        self.controls()
        self.properties()
        self.displayHealth()
        self.velocity = Vec3(0,0,0)

        taskMgr.add(self.mouseTask, 'mouse-update')
        taskMgr.add(self.moveTask, 'move-update')
        taskMgr.add(self.gravityTask, 'gravity')
        
    def loadModel(self):
        self.player = NodePath('player')
        self.player.reparentTo(render)
        self.player.setPos(0, 10, 2)

    def setupCamera(self):
        playerView = base.cam.node().getLens()
        playerView.setFov(70)
        base.cam.node().setLens(playerView)
        base.camera.reparentTo(self.player)

        crosshairs = OnscreenImage(image = 'UI/crosshairs.png', pos = (0,0,0), scale = 0.1)
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)
    
    def displayHealth(self):
        self.healthText = OnscreenText(text = "Health: {}".format(self.health),
                                       pos = (-1.3, 0.9), 
                                       scale = 0.1, 
                                       fg=(1, 1, 1, 1),
                                       align=TextNode.ALeft)
        self.healthText.setTransparency(TransparencyAttrib.MAlpha)

    def updateHealth(self):
        self.health += -20
        self.healthText.setText("Health: {}".format(self.health))
    
    def properties(self):
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        
    def collision(self):
        colliderNode = CollisionNode('player')
        colliderNode.addSolid(CollisionSphere(0,0,0,5))
        solid = self.player.attachNewNode(colliderNode)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.player, base.drive.node())

        ray = CollisionRay(0,0,0,0,0,-1)
        colliderNode = CollisionNode('playerRay')
        colliderNode.addSolid(ray)
        colliderNode.setFromCollideMask(BitMask32.bit(1))
        colliderNode.setIntoCollideMask(BitMask32.allOff())
        solid = self.player.attachNewNode(colliderNode)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)

        
    def controls(self):
        self.accept('escape', sys.exit)
        self.accept('w' , self.__setattr__,['walk',self.FORWARD])
        self.accept('s' , self.__setattr__,['walk',self.BACK])
        self.accept('s-up' , self.__setattr__,['walk',self.STOP])
        self.accept('w-up' , self.__setattr__,['walk',self.STOP])
        self.accept( 'a' , self.__setattr__,['strafe',self.LEFT])
        self.accept( 'd' , self.__setattr__,['strafe',self.RIGHT])
        self.accept( 'a-up' , self.__setattr__,['strafe',self.STOP])
        self.accept( 'd-up' , self.__setattr__,['strafe',self.STOP])
        self.accept('mouse1', self.shoot)
    

    def shoot(self):
        if base.mouseWatcherNode.hasMouse():
            mousePos = base.mouseWatcherNode.getMouse()
            nearPoint = Point3()
            farPoint = Point3()
            base.camLens.extrude(mousePos, nearPoint, farPoint)
            picker = CollisionTraverser()
            queue = CollisionHandlerQueue()
            pickerRay = CollisionRay()
            pickerNode = CollisionNode('mouseRay')
            pickerNode.setFromCollideMask(BitMask32.bit(1))
            pickerNode.addSolid(pickerRay)
            pickerNP = base.camera.attachNewNode(pickerNode)
            pickerNode.setFromCollideMask(BitMask32.bit(0)) 
            picker.addCollider(pickerNP, queue)
            picker.traverse(render)
            if queue.getNumEntries() > 0:
                queue.sortEntries()
                pickedObj = queue.getEntry(0).getIntoNodePath()
                if pickedObj.hasPythonTag("enemy"):
                    enemy = pickedObj.getPythonTag("enemy")
                    enemy.cleanup()
                    return


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
    

    def gravityTask(self,task):
        self.velocity.z -= self.GRAVITY * globalClock.getDt()
        self.player.setPos(self.player, self.velocity*globalClock.getDt()*self.speed)
        if self.player.getZ() < 10:
            self.player.setZ(2)
            self.velocity.z = 0
        return task.cont

    
class Enemy(Actor):
    
    def __init__(self, player):
        self.player = player
        self.enemy = Actor('models/panda-model.egg',
                           {'walk': 'models/panda-walk4'})
        self.enemy.setScale(0.009,0.009,0.009)
        pos = random.randint(-100,100)
        self.enemy.setPos(pos, pos, 1)
        self.enemy.setZ(2)
        self.enemy.reparentTo(render)
        self.enemy.setPythonTag('enemy','target')
        self.enemy.loop('walk')
        self.followPlayer()
        self.collision()
    
    def followPlayer(self):
        taskMgr.add(self.updateFollow, 'update-follow' , extraArgs=[self.player], appendTask=True)
    
    def cleanup(self):
        taskMgr.remove('update-follow')
    
    def collision(self):
        colliderNode = CollisionNode('enemy')
        colliderNode.addSolid(CollisionSphere(0,0,0,5))
        solid = self.enemy.attachNewNode(colliderNode)
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.enemy, base.drive.node())

    def updateFollow(self, player, task):
        distanceToPlayer = player.player.getPos() - self.enemy.getPos()
        distanceToPlayer.setZ(0)
        distanceToPlayer.normalize()
        self.enemy.setPos(self.enemy.getPos() + distanceToPlayer * 0.4)
        self.enemy.lookAt(player.player)
        return task.cont
    
    def updateHealthEnemy(self, player, task):
        distance = self.enemy.getDistance(player.player)
        if distance < 5:
            player.updateHealth()  
        return task.cont
    

app = game()
app.run()
