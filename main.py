from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class WashingtonBullets(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.properties()
        self.enviroment1()
        self.mouseInGame()
        self.controls()


        taskMgr.add(self.update, 'update')


    def properties(self): #sets up game properties
        props = WindowProperties() #creates window properties
        props.setTitle('Washington Bullets') #name of app running
        props.setSize(1280, 720 ) #sets display size
        base.win.requestProperties(props)

    def enviroment1(self):
        self.scene = self.loader.loadModel('enviroment/maps/bedroom_awesome.glb')
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, -59, 0)

    def controls(self):
        self.disableMouse()
        self.accept('mouse1', self.mouseInGame)
        self.accept('escape', self.mouseRelease)
    
    def mouseInGame(self): #takes mouse input in game
        props = WindowProperties()
        props.setCursorHidden(True) #hides cursor
        props.setMouseMode(WindowProperties.M_relative) #holds mouse in place in game
        self.win.requestProperties(props)
    
    def mouseRelease(self):
        props = WindowProperties()
        props.setCursorHidden(False) #shows cursor
        props.setMouseMode(WindowProperties.M_absolute) #holds mouse can go outside window
        self.win.requestProperties(props)

    def update(self, logic)
        
        return logic.cont
    


app = WashingtonBullets()
app.run()