import RPi.GPIO as GPIO

def left_callback(mplayer):
    def callback(channel): 
        mplayer.volume_down()
    return callback

def right_callback(mplayer):
    def callback(channel): 
        mplayer.volume_up()
    return callback
	
def top_callback(mplayer):
    def callback(channel):
        if mplayer.curr_station != None:
            if mplayer.paused:
                mplayer.unpause()
            else:
                mplayer.pause()
    return callback

class GPIOController():
    GPIO_LEDS = {
        'RED': 5,
        'GREEN': 6,
        'WHITE': 13,
        'BLUE': 19,
    }

    GPIO_BTNS = {
        'LEFT': 16,
        'RIGHT': 20,
        'TOP': 21,
    }
    
    BOUNCE_TIME = 200
    
    # Custom GPIO input callbacks
	# -----------------------------
	# Can be redefined for the user
	# related purpose
    
    GPIO_CALLBACKS = {
        'LEFT': left_callback,
        'RIGHT': right_callback,
        'TOP': top_callback,
        }

    def init(self, mplayer):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.GPIO_LEDS.values()), GPIO.OUT)
        GPIO.setup(list(self.GPIO_BTNS.values()), GPIO.IN)

        self.mplayer = mplayer

        for key, channel in self.GPIO_BTNS.items():
            GPIO.add_event_detect(channel, GPIO.FALLING,
                    callback = self.GPIO_CALLBACKS[key](self.mplayer),
                    bouncetime = self.BOUNCE_TIME)

    def clean(self):
        GPIO.cleanup()

    def light_led(self, led):
        led_bcm = list(self.GPIO_LEDS.values())[int(led) - 1]
        for led_no in list(self.GPIO_LEDS.values()): 
            if led_no == led_bcm:
                GPIO.output(led_no, GPIO.HIGH)
            else:
                GPIO.output(led_no, GPIO.LOW)
