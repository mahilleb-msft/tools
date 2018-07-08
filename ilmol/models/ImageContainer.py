class ImageContainer(object):
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value