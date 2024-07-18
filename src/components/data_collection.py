# Imports
import csv
import cv2 as cv
import numpy as np
import os
from dataclasses import dataclass

@dataclass
class DataCollectConfig:
    data_save_path = 'src/components/data'

class DataCollect():
    
    def __init__(self):
        self.data_config = DataCollectConfig()

    def collect(self, image, label: int, data, file_name = 'data.csv'):
        
        image_h, image_w, _ = image.shape
        
        # Normalise all the points with the base of the wrist 
        base_point = data[0]
        normalised_data = (data - base_point) / [image_w, image_h]

        # Create the directory 
        os.makedirs(self.data_config.data_save_path, exist_ok=True)
        save_path = os.path.join(self.data_config.data_save_path, file_name)

        #Save the data to file
        with open(save_path,'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([label, *(normalised_data.flatten())])
        