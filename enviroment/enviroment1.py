from direct.showbase.ShowBase import ShowBase

class Enviroment(ShowBase):

    def __init__(self):
        self.scene = self.loader.loadModel('enviroment/maps/bedroom.egg')
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, 0, -2)