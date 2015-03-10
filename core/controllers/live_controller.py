from base_controller import BaseController


class LiveController(BaseController):

    def get(self):
        self.render("live.html")
