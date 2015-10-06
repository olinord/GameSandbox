import os
import yaml
import imageio

def AbsJoin(*paths):
	return os.path.abspath(os.path.join(*paths))

ABSOLUTE_RES_FOLDER = AbsJoin(os.path.dirname(__file__), "..", "..", "resources")

def LoadResFile(path):
	with open(AbsJoin(ABSOLUTE_RES_FOLDER, path)) as f:
		return yaml.load(f.read())

def LoadEntityType(entityType):
	return LoadResFile("data/entities/" + entityType + ".yaml")

def LoadImage(imageName):
	image = imageio.imread(AbsJoin(ABSOLUTE_RES_FOLDER, "images", imageName))
	return image
	