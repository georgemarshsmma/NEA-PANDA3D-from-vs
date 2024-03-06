from panda3d.core import Vec2, Vec3
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode


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
        #faster than max speed set velocity vector to the max.
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
        
        # Move the character, using our velocity and
        # the time since the last update.
        self.actor.setPos(self.actor.getPost() + self.velocity*dt)
    
    def Health(self, dHealth):
        self.health += dHealth

        if self.health > self.maxHealth:
            self.health = self.maxHealth
    
    def cleanUp(self):
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)
        
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None


class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self, 
                            Vec3(0,0,0),
                            'actors/Man/Man.egg',
                            5,
                            10,
                            'player')
        self.score = 0

        self.scoreUI = OnscreenText(text = "0",
                            pos = (-1.3, 0.825),
                            mayChange = True,
                            align = TextNode.ALeft)

        self.healthIcons = []
        for i in range(self.maxHealth):
            icon = OnscreenImage(image = "UI/health.jpg",
                         pos = (-1.275 + i*0.075, 0, 0.95),
                         scale = 0.04)
            # Since our icons have transparent regions,
            # we'll activate transparency.
            icon.setTransparency(True)
            self.healthIcons.append(icon)
        
    def updateScore(self):
        self.scoreUI.setText(str(self.score))

    def alterHealth(self, dHealth):
        GameObject.alterHealth(self, dHealth)

        self.updateHealthUI()

    def updateHealthUI(self):
        for index, icon in enumerate(self.healthIcons):
            if index < self.health:
                icon.show()
            else:
                icon.hide()



class Enemy(GameObject):
    #self.enemy = [], if 3 enemies needed, create 3 instantiations and append to list in Player class
    #one type of enemy, same as enemy, instantiate enemy class as weapon does
    #checkProximity between enemy and player, def attack(self),
    #checkProxim() first, if in proxim., then attack()

    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        GameObject.__init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName)
        self.scoreValue = 1
        #points awarded if enemy is killed

    def update(self, player, dt):
        GameObject.update(self, dt)

        self.runLogic(player, dt)

        #allows to run different logic for different enemies

        if self.walking:
            walkingControl = self.actor.getAnimControl('walk')
            if not walkingControl.isPlaying():
                self.actor.loop('walk')
        else:
            spawnControl = self.actor.getAnimControl('spawn')
            if spawnControl is None or not spawnControl.isPlaying():
                attackControl = self.actor.getAnimControl('attack')
                if attackControl is None or not attackControl.isPlaying():
                    standControl = self.actor.getAnimControl('stand')
                    if not standControl.isPlaying():
                        self.actor.loop('stand')
    
    ##runs logic to find the vector between this enemy and the player. aim to face the player as well
    def runLogic(self, player, dt):
        print(123)
        vectorToPlayer = player.actor.getPos() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        if distanceToPlayer > self.attackDistance*0.9:
            vectorToPlayer.setZ(0)
            vectorToPlayer.normalize()
            self.velocity += vectorToPlayer * self.acceleration * dt
        else:
            self.walking = False
            self.velocity.set(0, 0, 0)

        self.actor.setH(heading)

    


class WalkingEnemy(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self,
                       pos,
                       'models/panda-model',
                       {'walk': 'models/panda-walk4'},
                       3.0,
                       7.0,
                       'enemy')
        
        self.actor.setScale(0.009, 0.009, 0.009)
        self.attackDistance = 0.75
        self.acceleration = 100.0
        print('enemy created')

        self.yVector = Vec2(0,1)
    

    #runs logic to find the vector between this enemy and the player. aim to face the player as well

    def runLogic(self, player, dt):
        print(123)
        vectorToPlayer = player.actor.getPos() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        if distanceToPlayer > self.attackDistance*0.9:
            vectorToPlayer.setZ(0)
            vectorToPlayer.normalize()
            self.velocity += vectorToPlayer * self.acceleration * dt
        else:
            self.walking = False
            self.velocity.set(0, 0, 0)

        self.actor.setH(heading)
    
    def alterHealth(self, dHealth):
        Enemy.alterHealth(self, dHealth)
        self.updateHealthVisual()

    def updateHealthVisual(self):
        perc = self.health/self.maxHealth
        if perc < 0:
            perc = 0
        # The parameters here are red, green, blue, and alpha
        self.actor.setColorScale(perc, perc, perc, 1)
