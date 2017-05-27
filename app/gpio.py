import RPi.GPIO as GPIO

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

BOUNCE_TIME = 200

def get_left_callback(gpiocontroller, mplayer):
    def callback(channel): 
        if GPIO.input(GPIO_BTNS['TOP']):
            mplayer.volume_down()
        else:
            mplayer.prev()
            gpiocontroller.light_led(mplayer.curr_station)
    return callback

def get_right_callback(gpiocontroller, mplayer):
    def callback(channel): 
        if GPIO.input(GPIO_BTNS['TOP']):
            mplayer.volume_up()
        else:
            mplayer.next()
            gpiocontroller.light_led(mplayer.curr_station)
    return callback
        
def get_top_callback(gpiocontroller, mplayer):
    def callback(channel):
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(GPIO_LEDS.values()), GPIO.OUT)
        GPIO.setup(list(GPIO_BTNS.values()), GPIO.IN)

        self.mplayer = mplayer

        for key, channel in GPIO_BTNS.items():
            GPIO.add_event_detect(channel, GPIO.FALLING,
                    callback = GPIO_CALLBACK_FACTORIES[key](self, self.mplayer),
                    bouncetime = BOUNCE_TIME)
        
        self.light_led(1)

    def clean(self):
        GPIO.cleanup()

    def light_led(self, led):
        led_bcm = list(GPIO_LEDS.values())[int(led) - 1]
        for led_no in list(GPIO_LEDS.values()): 
            if led_no == led_bcm:
                GPIO.output(led_no, GPIO.HIGH)
            else:
                GPIO.output(led_no, GPIO.LOW)
