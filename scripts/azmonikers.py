# Azure Moniker Counter
# (C) Den Delimarsky, July 23, 2017
# Script that breaks down the monikers that are registered for Azure

import json
import os
import sys

from pprint import pprint
from os import listdir
from os.path import isfile, join

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

localOPSFolder = sys.argv[1]
localFrameworksIndexFolder = sys.argv[2]
opsConfigurationName = ".openpublishing.publish.config.json"
configurationLookupFolder = os.path.join(localOPSFolder, opsConfigurationName)
shouldAugmentOPSConfig = bool(sys.argv[3])

data = None

print("Azure Moniker Counter")
print("Local OPS folder: " + localOPSFolder)
print("Local Frameworks Index folder: " + localFrameworksIndexFolder)
print("Joint lookup path: " + configurationLookupFolder)

with open(configurationLookupFolder) as data_file:
    data = json.load(data_file)

# Get the list of monikers declared in the configuration file - that is NOT the source of truth
monikers = data["docsets_to_publish"][0]["monikers"]

print("Registered monikers in OPS configuration file:")
pprint(monikers)

monikerFiles = [f for f in listdir(localFrameworksIndexFolder) if (isfile(join(localFrameworksIndexFolder, f)) and f.endswith(".xml"))]

monikerFiles[:] = [mf.replace(".xml","") for mf in monikerFiles]

print ("Existing moniker files: ")
pprint(monikerFiles)

print ("Monikers that are in OPS config, but not in folder:")
pprint(set(monikers) - set(monikerFiles))

print("Monikers that are in the folder, but not OPS config file:")
pprint(set(monikerFiles) - set(monikers))

if (shouldAugmentOPSConfig == True):
    print ("Augmenting file...")
    data["docsets_to_publish"][0]["monikers"] = monikerFiles
    pprint(data)

    with open(configurationLookupFolder, mode='w') as f:
        f.write(json.dumps(data, indent=2))