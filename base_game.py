class task_functions:
    
    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.audio_inst.play()
        while self.instructions._player.time <= int(self.instructions.duration):
            self.instructions.draw()
            win.flip()
        win.flip()

    