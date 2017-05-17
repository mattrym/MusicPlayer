import os.path
import tornado.web

class TrackModule(tornado.web.UIModule):
    def render(self, track_no, track_name):
        return self.render_string("track-module.html",
                track_no = track_no, track_name = track_name)
