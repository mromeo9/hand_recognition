# Imports
import argparse

from src.components.camera_access import Camera

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", type=int, default=0)
    parser.add_argument("-l", "--label", type=int)

    args = parser.parse_args()

    return args

def main(parser):
    
    mode = parser.mode
    label = parser.label
    camera = Camera(label = label, mode = mode)
    camera(camera_path=1)

if __name__ == '__main__':
    parser = get_args()
    main(parser)

