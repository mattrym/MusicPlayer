import RPi.GPIO as GPIO

class GPIOController():
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

    GPIO_CALLBACKS = {
        'LEFT': left_callback,
        'RIGHT': right_callback,
        'TOP': top_callback,
        }

    def init(self, mplayer):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_LEDS.values(), GPIO.OUT)
        GPIO.setup(self.GPIO_BTNS.values(), GPIO.IN)

        self.mplayer = mplayer

        for key, channel in self.GPIO_CALLBACKS:
            GPIO.add_event_detect(channel, GPIO.FALLING,
                    callback = self.GPIO_CALLBACKS[key],
                    bouncetime = self.BOUNCE_TIME)

    def clear(self):
        GPIO.remove_event_detect(self.GPIO_BTNS.values())
        GPIO.cleanup()

    def light_led(self, led):
        led_bcm = GPIO_LEDS.values()[led - 1]
        for led_no in self.GPIO_LEDS.values(): 
            if led_no != led_bcm:
                GPIO.output(led_no, GPIO.HIGH)
            else:
                GPIO.output(led_no, GPIO.LOW)

# Custom GPIO input callbacks
# -----------------------------
# Can be redefined for the user
# related purpose

    def left_callback(channel):
        self.mplayer.volume_down()

    def right_callback(channel):
        self.mplayer.volume_up()

    def top_callback(channel):
        if self.mplayer.curr_station != None:
            if self.mplayer.paused:
                self.mplayer.unpause()
            else:
                self.mplayer.pause()
