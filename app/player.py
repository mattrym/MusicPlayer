import os, os.path
import subprocess

class MusicPlayer():
    stations = [
        'http://radio.nolife-radio.com:9000/stream',
        'http://proxy.tuned.svada.net:8000/radiojazzfm.mp3',
        'http://148.163.81.10:8006/stream',
        'http://live.slovakradio.sk:8000/Devin_256.mp3',
        ]
    commands = {
            'add': ['mpc', 'add', ],
            'play': ['mpc', 'play', ],
            'stop': ['mpc', 'stop', ],
            'pause': ['mpc', 'pause', ],
            'volume': ['mpc', 'volume', ],
            'clear': ['mpc', 'clear' ],
        }
    volume_interval = 5

    def __mpc(self, cmd):
        p = subprocess.Popen(cmd, 
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                )
        return p.stdout.read()

    def __init__(self):
        self.clear()
        stations = list(enumerate(MusicPlayer.stations, start = 1))
        
        for station_no, station_url in stations:
            cmd = list(self.commands['add'])
            cmd.append(station_url)
            self.__mpc(cmd)

        self.paused = True 
        self.curr_station = 1 

    def clear(self):
        cmd = list(self.commands['clear'])
        self.__mpc(cmd)

    def play(self, station_no):
        self.pause()

        cmd = list(self.commands['play'])
        cmd.append(str(station_no))
        self.__mpc(cmd)

        self.paused = False
        self.curr_station = int(station_no)

    def pause(self):
        cmd = list(self.commands['pause'])
        self.__mpc(cmd)
        self.paused = True

    def unpause(self):
        cmd = list(self.commands['play'])
        self.__mpc(cmd)
        self.paused = False

    def prev(self):
        self.play((self.curr_station - 2) % 4 + 1)
    
    def next(self):
        self.play(self.curr_station % 4 + 1)
    
    def volume_up(self):
        cmd = list(self.commands['volume'])
        cmd.append('+' + str(self.volume_interval))
        self.__mpc(cmd)

    def volume_down(self):
        cmd = list(self.commands['volume'])
        cmd.append('-' + str(self.volume_interval))
        self.__mpc(cmd)
