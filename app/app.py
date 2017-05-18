import os.path
import tornado.web

from .handlers import (
        MainHandler,
        PauseHandler,
        TrackHandler,
        VolumeHandler,
        )
from .player import MusicPlayer
from .gpio import GPIOController
from . import modules

class FMApplication(tornado.web.Application):
    def __init__(self):
        self.mplayer = MusicPlayer()
        self.gpiocontroller = GPIOController()
        init_dict = {
                'mplayer': self.mplayer,
                'gpiocontroller': self.gpiocontroller,
                }
        top_dir = os.path.dirname(os.path.dirname(__file__))

        handlers = [
                (r'/', MainHandler, init_dict),
                (r'/pause', PauseHandler, init_dict),
                (r'/track/(\d+)', TrackHandler, init_dict),
                (r'/volume/(up|down)', VolumeHandler, init_dict),
                (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
                ]
        settings = {
                'ui_modules': modules,
                'template_path': os.path.join(top_dir, 'templates'),
                'static_path': os.path.join(top_dir, 'static'),
                'debug': True
                }

        self.gpiocontroller.init(self.mplayer)
        tornado.web.Application.__init__(self, handlers, **settings)

def make_application():
    return FMApplication()
