from direct.actor.Actor import Actor

class Player():
    def __init__(self, charId, charNr):
        self.charId = charId
        charPath = 'models/panda-model'.egg(charNr)
        self.character = Actor(
            charPath + 'char', {
                'walk':charPath + 'walk'
            }
        )