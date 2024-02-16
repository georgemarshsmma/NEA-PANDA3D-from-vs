    def update(self, task):
        dt = globalClock.getDt()

        x_movement = 0
        y_movement = 0
        z_movement = 0

        playerMoveSpeed = 20

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

        node.setPos(
            node.getX() + x_movement,
            node.getY() + y_movement,
            node.getZ() + z_movement,
        )

        if self.cameraSwingActivated:
            md = self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()

            mouseChangeX = mouseX - self.prevMouseX
            mouseChangeY = mouseY - self.prevMouseY

            self.cameraSwingFactor = 10

            currentH = self.node.getH()
            currentP = self.node.getP()

            self.node.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
                0)

            self.prevMouseX = mouseX
            self.prevMouseY = mouseY
            
        return task.cont




        self.keyMap = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'run': False,
        }
