from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from iptcinfo3 import IPTCInfo
from models.ImageContainer import ImageContainer

import json

class Ilmol(object):
    CONFIG_DATA=''

    def __init__(self):
        self.load_config()
        print(self.CONFIG_DATA)

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

    def process_images(self, images):
        for image in images:
            image_container = ImageContainer()

            metadata = {}

            caption = ''
            model = ''
            city = ''
            country = ''
            slug = ''

            with Image.open(image) as i:
                print ("[INFO] Getting IPTC information from ", image)
                iptc_info = IPTCInfo(image)

                print("[INFO] ", iptc_info)

                # Using "in" to check whether something is in the array for this case
                # produces a hang.

                if (iptc_info):
                    try:
                        image_container.title = iptc_info['object name'].decode('utf-8')
                        print("[INFO] Title recognized: ", image_container.title)
                    except:
                        print("[ERROR] Could not obtain title.")

                    try:
                        country = iptc_info['country/primary location name'].decode('utf-8')
                        print("[INFO] Country recognized: ", country)
                    except:
                        print("[ERROR] Could not obtain country.")

                    try:
                        city = iptc_info['city'].decode('utf-8')
                        print("[INFO] City recognized: ", city)
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
                caption = metadata['ImageDescription']
                print("[INFO] Caption recognized: ", caption)

            if ('Model' in metadata):
                model = metadata['Model']
                print("[INFO] Model recognized: ", model)

            if ('UserComment' in metadata):
                slug = metadata['UserComment'].decode('ascii').split('\x00\x00\x00')[1]
                print("[INFO] Slug recognized: ", slug)