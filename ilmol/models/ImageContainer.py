class ImageContainer(object):
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value
    
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value
    
    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, value):
        self._slug = value
    
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def f_stop(self):
        return self._f_stop

    @f_stop.setter
    def f_stop(self, value):
        self._f_stop = value

    @property
    def shutter_speed(self):
        return self._shutter_speed

    @shutter_speed.setter
    def shutter_speed(self, value):
        self._shutter_speed = value
    
    @property
    def iso_speed(self):
        return self._iso_speed

    @iso_speed.setter
    def iso_speed(self, value):
        self._iso_speed = value