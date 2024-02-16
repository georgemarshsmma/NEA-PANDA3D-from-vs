from panda3d import Vec2, Vec3
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode 

FRICTION = 150

class GameObject():
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

        self.maxHealth = maxHealth
        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0,0,0)
        self.acceleration = 300.0

        self.walking = False

        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0,0,0,0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.setPythonTag('owner', self)
    
    def update(self, dt):
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed

        if not self.walking:
            frictionVal = FRICTION*dt

        else:
            frictionVec = -self.velocity
            frictionVec.normalize()
            frictionVec *= frictionVal
            self.velocity += frictionVec
        
        self.actor.setPos(self.actor.getPost() + self.velocity*dt)
    
    def Health(self, dHealth):
        self.health += dHealth

        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def c

class Player(GameObject):
    pass

class Enemy(GameObject):
    #self.enemy = [], if 3 enemies needed, create 3 instantiations and append to list in Player class
    #one type of enemy, same as enemy, instantiate enemy class as weapon does
    #checkProximity between enemy and player, def attack(self),
    #checkProxim() first, if in proxim., then attack()
    pass

class FollowingEnemy(Enemy):
    pass

