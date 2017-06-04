import os
import select
import threading

GPIO_LEDS = {
    'RED': 24,
    'GREEN': 23,
    'WHITE': 18,
    'BLUE': 17,
}

GPIO_BTNS = {
    'LEFT': 10,
    'RIGHT': 22,
    'TOP': 27,
}

GPIO_SYSFS = '/sys/class/gpio'
BASE_TIMEOUT = 2000
DBNC_TIMEOUT = 250

def get_left_callback(gpiocontroller, mplayer):
    def callback(): 
        if gpiocontroller.get(GPIO_BTNS['TOP']):
            mplayer.volume_down()
        else:
            mplayer.prev()
            gpiocontroller.light_led(mplayer.curr_station)
    return callback

def get_right_callback(gpiocontroller, mplayer):
    def callback(): 
        if gpiocontroller.get(GPIO_BTNS['TOP']):
            mplayer.volume_up()
        else:
            mplayer.next()
            gpiocontroller.light_led(mplayer.curr_station)
    return callback
        
def get_top_callback(gpiocontroller, mplayer):
    def callback():
        if mplayer.curr_station != None:
            if mplayer.paused:
                mplayer.unpause()
            else:
                mplayer.pause()
    return callback

GPIO_CALLBACK_FACTORIES = {
    'LEFT': get_left_callback,
    'RIGHT': get_right_callback,
    'TOP': get_top_callback,
    }

class GPIOController():
    def init(self, mplayer):
        for btn in list(GPIO_BTNS.values()):
            self.export(btn, 'in')
        for led in list(GPIO_LEDS.values()):
            self.export(led, 'out')

        self.light_led(1)
        self.mplayer = mplayer
        self.running = True
        self.add_event_detect()

    def clean(self):
        self.event_thread.join()
        for (key, (fd, callback)) in self.btn_callbacks.items():
            fd.close()

        for btn in GPIO_BTNS.values():
            self.unexport(btn)
        for led in GPIO_LEDS.values():
            self.unexport(led)

    def export(self, gpio, mode):
        with open(os.path.join(GPIO_SYSFS, 'export'), 'w') as fd:
            fd.write(str(gpio))
        self.mode(gpio, mode)

    def mode(self, gpio, mode, edge='falling'):
        with open(os.path.join(GPIO_SYSFS, 'gpio%d' % gpio, 'direction'), 'w') as fd:
            fd.write(mode)

        if mode == 'in':
            with open(os.path.join(GPIO_SYSFS, 'gpio%d' % gpio, 'edge'), 'w') as fd:
                fd.write(edge)

    def clear(self, fd):
        with open(fd, 'r') as f:
            f.read(8)

    def get(self, gpio):
        with open(os.path.join(GPIO_SYSFS, 'gpio%d' % gpio, 'value'), 'r') as fd:
            return int(fd.read(1))

    def set(self, gpio, value):
        with open(os.path.join(GPIO_SYSFS, 'gpio%d' % gpio, 'value'), 'w') as fd:
            fd.write(str(int(bool(value))))

    def unexport(self, gpio):
        with open(os.path.join(GPIO_SYSFS, 'unexport'), 'w') as fd:
            fd.write(str(gpio))
        
    def add_event_detect(self):
        self.btn_callbacks = dict()
        for key in list(GPIO_BTNS.keys()):
            self.btn_callbacks[key] = (
                open(os.path.join(GPIO_SYSFS, 'gpio%d' % GPIO_BTNS[key], 'value'), 'r'),
                GPIO_CALLBACK_FACTORIES[key](self, self.mplayer),
                )

        self.event_thread = threading.Thread(target = self.event_handler)
        self.event_thread.start()
        
    def event_handler(self):
        base_poll = select.poll()
        dbnc_poll = select.poll()

        for (key, (fd, callback)) in self.btn_callbacks.items():
            base_poll.register(fd, select.POLLPRI)
            dbnc_poll.register(fd, select.POLLPRI)

        while self.running:
            ready = base_poll.poll(BASE_TIMEOUT)
            if ready:
                for fd, event in ready:
                    os.lseek(fd, 0, os.SEEK_SET)
                    os.read(fd, 16)
                
                dbnc_ready = True
                while dbnc_ready:
                    dbnc_ready = dbnc_poll.poll(DBNC_TIMEOUT)
                    for fd, event in dbnc_ready:
                        os.lseek(fd, 0, os.SEEK_SET)
                        os.read(fd, 16)

                for (key, (fd, callback)) in self.btn_callbacks.items():
                    if fd.fileno() in [rfd for rfd, revent in ready]:
                        callback()

    def light_led(self, led):
        led_bcm = list(GPIO_LEDS.values())[int(led) - 1]

        for led_no in GPIO_LEDS.values(): 
            if led_no == led_bcm:
                self.set(led_no, 1)
            else:
                self.set(led_no, 0)
