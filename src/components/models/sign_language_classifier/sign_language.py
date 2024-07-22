# Importing modules
import csv
import tensorflow as tf
import keras
from dataclasses import dataclass
import numpy as np

# File imports
from src.logger import logging
from src.exceptions import CustomException

@dataclass
class SignLanguageConfig:
    path_to_model = 'src/components/models/sign_language_classifier/sign_language_model.keras'
    path_to_labels = 'src/components/models/sign_language_classifier/sign_language_labels.csv'

class SignLanguageClassifier:

    def __init__(self, confidence = 0.6):
        self.config = SignLanguageConfig()
        self.model = keras.models.load_model(self.config.path_to_model)
        self.labels = self._get_labels()

        # Prediction confidence
        self.confidence = confidence

    def __call__(self, input):
        
        # Make prediction
        output = self.model(input)

        #Find the label
        output = tf.nn.softmax(output)
        lab = np.argmax(output)

        # Make prediction only when over the confidence threshold 
        if output[0][lab] > self.confidence:
            return self.labels[lab]
        
        else: return 'None'

    def _get_labels(self):
        
        with open(self.config.path_to_labels, encoding='utf-8-sig') as file_obj:
            sign_language_labels = csv.reader(file_obj)
            sign_language_labels = [row[0] for row in sign_language_labels]

        return sign_language_labels