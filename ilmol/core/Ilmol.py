from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from iptcinfo3 import IPTCInfo
from models.ImageContainer import ImageContainer
import ntpath
import math

import json

class Ilmol(object):
    CONFIG_DATA=''

    def __init__(self):
        self.load_config()
        # print(self.CONFIG_DATA)

    def _map_key(self, k):
        try:
            return TAGS[k]
        except KeyError:
            return GPSTAGS.get(k, k)

    def load_config(self):
        print ("[INFO] Loading application configuration...")
        with open('ilmol.json') as f:
            self.CONFIG_DATA = json.load(f)

    def generate_markdown_file(self, imageslug):
        return 0
    
    # https://stackoverflow.com/a/8384788/303696
    def get_file_name(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    # https://www.media.mit.edu/pia/Research/deepview/exif.html
    def get_shutter_speed(self, shutter_speed_value):
        # To convert this value to ordinary 'Shutter Speed'; calculate this value's power of 2, then reciprocal. For example, if value is '4', shutter speed is 1/(2^4)=1/16 second.
        # raw_shutter_speed = 2**math.ceil(float(shutter_speed_value[0])/float(shutter_speed_value[1]))
        
        # shutter_speed_string = "1/" + str(raw_shutter_speed)
        shutter_speed_string = str(shutter_speed_value[0]) + "/" + str(shutter_speed_value[1])
        return shutter_speed_string


    def get_f_stop(self, aperture_value):
        if (len(aperture_value)<2):
            return 0
        else:
            # In Python, by default the int is taken out of context - we need to convert to
            # float to make sure that we get the "true" value.
            apex_aperture = math.ceil(float(aperture_value[0])/float(aperture_value[1]))
            f_stop = float(str(math.sqrt(2**apex_aperture))[:3])
            return f_stop

    def process_images(self, images):
        for image in images:
            image_container = ImageContainer()

            metadata = {}

            image_container.file_name = self.get_file_name(image)

            with Image.open(image) as i:
                print ("[INFO] Getting IPTC information from ", image)
                iptc_info = IPTCInfo(image)

                # print("[INFO] ", iptc_info)

                # Using "in" to check whether something is in the array for this case
                # produces a hang.

                if (iptc_info):
                    try:
                        image_container.title = iptc_info['object name'].decode('utf-8')
                        print("[INFO] Title recognized: ", image_container.title)
                    except:
                        print("[ERROR] Could not obtain title.")

                    try:
                        image_container.country = iptc_info['country/primary location name'].decode('utf-8')
                        print("[INFO] Country recognized: ", image_container.country)
                    except:
                        print("[ERROR] Could not obtain country.")

                    try:
                        image_container.city = iptc_info['city'].decode('utf-8')
                        print("[INFO] City recognized: ", image_container.city)
                    except:
                        print("[ERROR] Could not obtain city.")
                else:
                    print ("[INFO] No IPTC data to process.")

                print ("[INFO] Getting EXIF information from ", image)

                info = i._getexif()
            try:
                [ metadata.__setitem__(self._map_key(k), v) for k, v in info.items() ]
                # print (metadata)
            except:
                print ('Error occurred reading the metadata.')

            if ('ImageDescription' in metadata):
                image_container.caption = metadata['ImageDescription']
                print("[INFO] Caption recognized: ", image_container.caption)

            if ('Model' in metadata):
                image_container.model = metadata['Model']
                print("[INFO] Model recognized: ", image_container.model)

            if ('UserComment' in metadata):
                image_container.slug = metadata['UserComment'].decode('ascii').split('\x00\x00\x00')[1]
                print("[INFO] Slug recognized: ", image_container.slug)
            
            # ApertureValue = log2(FStop^2)
            # FStop = Sqrt(2^(ApertureValue))
            if ('ApertureValue' in metadata):
                image_container.f_stop = self.get_f_stop(metadata['ApertureValue'])
                print("[INFO] Aperture recognized: ", image_container.f_stop)

            if ('ExposureTime' in metadata):
                image_container.shutter_speed = self.get_shutter_speed(metadata['ExposureTime'])
                print("[INFO] Shutter speed recognized: ", image_container.shutter_speed)

            if ('ISOSpeedRatings' in metadata):
                image_container.iso_speed = metadata['ISOSpeedRatings']
                print("[INFO] ISO speed recognized: ", image_container.iso_speed)