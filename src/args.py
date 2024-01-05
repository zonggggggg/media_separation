import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", type=str, help="input video path")
    parser.add_argument("-i", "--image", type=str, help="input image path")
    parser.add_argument("-s", "--show", action="store_true", help="show video")
    args = parser.parse_args()
    return args
