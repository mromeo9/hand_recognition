# Imports
import csv
import cv2 as cv
import numpy as np
import os
from dataclasses import dataclass

@dataclass
class DataCollectConfig:
    data_save_path = 'src/components/data/data.csv'

class DataCollect():
    
    def __init__(self):
        self.data_config = DataCollectConfig()

    def collect(self, label: int, data: np.array[tuple]):
        
        # Normalise all the points with the base of the wrist 
        base_point = data[0]
        normalised_data = data - base_point

        #Save the data to file
        with open(self.data_config.data_save_path,'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([label, *normalised_data])
        