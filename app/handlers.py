import tornado.web
import tornado.httpclient

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, mplayer, gpiocontroller):
        self.mplayer = mplayer
        self.gpiocontroller = gpiocontroller

class MainHandler(BaseHandler):
    def get(self):
        self.render('main-template.html',
                tracklist = list(
                enumerate(self.mplayer.stations, start = 1)
            ))

class PauseHandler(BaseHandler):
    def get(self):
        if self.mplayer.paused:
            self.mplayer.unpause()
        else:
            self.mplayer.pause()
        self.redirect('/')

class TrackHandler(BaseHandler):
    def get(self, track_no):
        self.mplayer.play(track_no)
        self.gpiocontroller.light_led(track_no)
        self.redirect('/')

class VolumeHandler(BaseHandler):
    def get(self, updown):
        if updown == 'up':
            self.mplayer.volume_up()
        elif updown == 'down':
            self.mplayer.volume_down()
        else:
            raise HTTPError(500)
        self.redirect('/')
