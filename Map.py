import numpy as np
from PIL import Image
import pickle
import Utilities as util

class Layer:
    def __init__(self, layer_name: str, layer_data=None, layer_map=None, resolution=None):
        self.name = layer_name
        if layer_data != None:
            self.data = layer_data
        else:
            if resolution == None:
                raise ValueError("Neither Resolution nor Data provided")
            self.data = np.ones(shape=resolution, dtype=np.uint8)
        self.map = {}
        
    def add_value(self, key, value) -> None:
        if key in self.map or value in self.map.values():
            raise ValueError("Key or Value already mapped")
        self.map[key] = value

class MapObject:
    def __init__(self, image_path=None, map_object_name="") -> None:
        self.name = map_object_name
        if image_path == None:
            image_path = util.choose_file()
        self.load_map(image_path)
        self.resolution = (self.map.shape[0], self.map.shape[1])
        assert self.map.shape[2] == 3, f"Imported map {map_object_name} is not RGB" #TODO alpha channels not handled
        self.layers = {}
    
    def add_layer(self, layer_name: str, layer_data=None) -> None:
        self.layers[layer_name] = (Layer(layer_name, layer_data, resolution=self.resolution))
    
    def update_layer(self, layer_name:str, data=None, name=None, map=None) -> None:
        assert layer_name in self.layers, "Layer not found"
        old = self.layers[layer_name]
        if data == None:
            data = old.data
        if map == None:
            map = old.map
        if name == None:
            self.layers[layer_name] = Layer(name, layer_data=data, layer_map=map, resolution=old.resolution)
        else:
            del self.layers[layer_name]
            self.layers[name] = Layer(name, layer_data=data, layer_map=map, resolution=old.resolution)
    
    def save_MapObject(self, path):
        with open(f"{path}.pickle", 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
    
    def load_map(self, path: str) -> np.array:
        img = Image.open(path)
        self.map = np.asarray(img)
        
def load_MapObject(path=None) -> MapObject:
    if path == None:
        path = util.choose_file()
    with open(path, 'rb') as f:
        loaded_object = pickle.load(f)
    return loaded_object        