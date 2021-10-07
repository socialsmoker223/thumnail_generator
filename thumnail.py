from openslide import OpenSlide
import numpy as np
from PIL import Image
import json

class Thumbnail:
    def __init__(self):
        pass
    def load_data(self, slide_path, data_path):
        self.slide = OpenSlide(slide_path)
        with open(data_path)as f:
            self.data = json.load(f)           
        self.img = self.slide.get_thumbnail((1000,1000))
        self.x_ratio = self.img.size[0]/self.slide.dimensions[0]
        self.y_ratio = self.img.size[1]/self.slide.dimensions[1]
        self.img_data = np.array(self.img)
        
        pass
    
    def transform(self, size=3):
        red = np.array([255,0,0])
        green = np.array([0,128,0])
        orange = np.array([255,165,0])
        for case in self.data:
            if case == 'tumor':
                color = red
            if case == 'stroma':
                color = green
            if case == 'other':
                color = orange
            if case == 'no_label':
                pass
            for item in self.data[case]:
                for vertice in item['vertices']:
                    for i in range(size):
                        self.img_data[min(int(vertice[1]*self.y_ratio+i), self.img.size[1]-1), min(int(vertice[0]*self.x_ratio+i),self.img.size[0]-1)] = color
                        self.img_data[min(int(vertice[1]*self.y_ratio+i), self.img.size[1]-1), min(int(vertice[0]*self.x_ratio-i),self.img.size[0]-1)] = color
                        self.img_data[min(int(vertice[1]*self.y_ratio-i), self.img.size[1]-1), min(int(vertice[0]*self.x_ratio+i),self.img.size[0]-1)] = color
                        self.img_data[min(int(vertice[1]*self.y_ratio-i), self.img.size[1]-1), min(int(vertice[0]*self.x_ratio-i),self.img.size[0]-1)] = color
        new_image = Image.fromarray(self.img_data)
        return(new_image)

if __name__ == '__main__':
    slide_path = './data/sample.svs'
    data_path = './data/sample.json'
    t = Thumbnail()
    t.load_data(slide_path, data_path)
    png = t.transform()
    png.save('./output/sample.png')
