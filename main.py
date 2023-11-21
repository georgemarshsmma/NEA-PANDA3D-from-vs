from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import GraphicsWindow

def degToRad(degrees):
    return degrees * (pi / 180.0)

class WashingtonBullets(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.properties()
        self.enviroment1()
        self.setupCamera()
        self.mouseInGame()
        self.controls()

        taskMgr.add(self.update, 'update')

    def update(self, task):
        dt = globalClock.getDt()

        x_movement = 0
        y_movement = 0
        z_movement = 0

        playerMoveSpeed = 10

        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))

        self.camera.setPos(
            camera.getX() + x_movement,
            camera.getY() + y_movement,
            camera.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.prevMouseX
            mouseChangeY = mouseY - self.prevMouseY

            self.cameraSwingFactor = 10

            currentH = self.camera.getH()
            currentP = self.camera.getP()

            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0)

            self.prevMouseX = mouseX
            self.prevMouseY = mouseY
            
        return task.cont



    def controls(self):
        self.accept('escape', self.mouseRelease)
        self.accept('mouse1', self.mouseInGame )

        self.keyMap = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'up': False,
            'down': False
        }

        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
    
    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def properties(self): #sets up game properties
        props = WindowProperties() #creates window properties
        props.setTitle('Washington Bullets') #name of app running
        props.setSize(800, 600) #sets display size
        base.win.requestProperties(props)

    def setupCamera(self):
        self.disableMouse()
        self.scene.setPos(0, 0, -7)

    def enviroment1(self):
        self.scene = self.loader.loadModel('enviroment/maps/bedroom.egg')
        self.scene.reparentTo(self.render)
        
    def mouseInGame(self): #takes mouse input in game
        self.cameraSwingActivated = True
        props = WindowProperties()
        md = self.win.getPointer(0)
        self.prevMouseX = md.getX()
        self.prevMouseY = md.getY()

        props.setCursorHidden(True) #hides cursor
        props.setMouseMode(WindowProperties.M_relative) #holds mouse in place in game, ONLY WORKS ON MAC FOR SOME REASON????
        self.win.requestProperties(props)
    
    def mouseRelease(self):
        self.cameraSwingActivated = False
        props = WindowProperties()
        props.setCursorHidden(False) #shows cursor
        props.setMouseMode(WindowProperties.M_absolute) #holds mouse can go outside window
        self.win.requestProperties(props)


app = WashingtonBullets()
app.run()