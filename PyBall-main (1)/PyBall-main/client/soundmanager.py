import pygame as pg

class SoundManager:
    def __init__(self):
        self.sounds = {

        }
        self.sounds["music"] = pg.mixer.Sound("../shared/assets/audio/music.mp3")
        self.sounds["click"] = pg.mixer.Sound("../shared/assets/audio/click.mp3")
        self.sounds["alert"] = pg.mixer.Sound("../shared/assets/audio/alert.wav")
        self.sounds["leave"] = pg.mixer.Sound("../shared/assets/audio/leave.wav")

    

    def play(self, name):
        self.sounds[name].play()

    def setVolume(self,volume):
        for sound in self.sounds:
            self.sounds[sound].set_volume(volume)

    def playMusic(self):
        self.sounds["music"].play(-1)
