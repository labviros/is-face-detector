import json
from is_wire.core import Logger
import argparse
import numpy as np
import cv2
from is_msgs.image_pb2 import Image, ObjectAnnotations, ObjectLabels
from google.protobuf.json_format import Parse
from options_pb2 import FaceDetectorOptions

def load_options():
    log = Logger(name='LoadOptions')
    parser = argparse.ArgumentParser('Load options for face detector!')
    parser.add_argument("-o", "--op", type=str, help="Load options")
    args = parser.parse_args()
    with open (args.op, 'r') as f:
        op = Parse(f.read(), FaceDetectorOptions())   
    return op

def get_np_image(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image

def get_pb_image(input_image, encode_format='.jpeg', compression_level=0.8):
    if isinstance(input_image, np.ndarray):
        if encode_format == '.jpeg':
            params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
        elif encode_format == '.png':
            params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format, img=input_image, params=params)
        return Image(data=cimage[1].tobytes())
    elif isinstance(input_image, Image):
        return input_image
    else:
        return Image()