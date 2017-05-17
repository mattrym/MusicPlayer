import subprocess
import os, os.path
from pygame import mixer
from pygame.mixer import music

class MusicPlayer():
    commands = {
            'add': ['mpc', 'add', ],
            'play': ['mpc', 'play', ],
            'stop': ['mpc', 'stop', ],
            'pause': ['mpc', 'pause', ],
            'volume': ['mpc', 'volume', ],
            'clear': ['mpc', 'clear' ],
            }
    volume_interval = 2

    def __mpc(self, cmd):
        print(cmd)
        p = subprocess.Popen(cmd, 
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                )
        return p.stdout.read()

    def __init__(self):
        self.clear()
        
        self.tracks = list(enumerate([filename 
                for filename in os.listdir('/var/lib/mpd/music')
                if os.path.splitext(filename)[1] == '.mp3']))
        self.tracks.sort(key = lambda entry: entry[1])
        for track_no, track_name in self.tracks:
            cmd = list(self.commands['add'])
            cmd.append(track_name)
            self.__mpc(cmd)

        self.paused = False

    def play(self, track_no):
        cmd = list(self.commands['play'])
        cmd.append(str(track_no))
        self.__mpc(cmd)
    
    def pause(self):
        cmd = list(self.commands['pause'])
        self.__mpc(cmd)
        self.paused = True

    def unpause(self):
        cmd = list(self.commands['play'])
        self.__mpc(cmd)
        self.paused = False

    def volume_up(self):
        cmd = list(self.commands['volume'])
        cmd.append('+' + str(self.volume_interval))
        self.__mpc(cmd)

    def volume_down(self):
        cmd = list(self.commands['volume'])
        cmd.append('-' + str(self.volume_interval))
        self.__mpc(cmd)

    def clear(self):
        cmd = list(self.commands['clear'])
        self.__mpc(cmd)
