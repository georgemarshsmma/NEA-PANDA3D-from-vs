from direct.actor.Actor import Actor

class Player():
    def character1(self):
        self.actor = Actor('actors/actor.egg')
        self.actor.reparentTo(self.render)
        self.actor.setPos(0,0,-6)