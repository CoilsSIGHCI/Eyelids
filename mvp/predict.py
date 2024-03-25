import io
import json
import os

import cv2
import numpy as np
import torch
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from torch.autograd import Variable
import torch.nn.functional as F

from hw import is_raspberry_pi

MODEL_PATH = './trained_models/Pretrained models/egogesture_resnetl_10_RGB_8.pth'
class Model:
    def __init__(self):
        self.model = torch.load(MODEL_PATH)
        self.recordingBuffer = io.BytesIO()
        self.recordingBufferFileIO = FileOutput(self.recordingBuffer)

    def test(self, opt, class_names):
        print('predict')

        self.model.eval()

        with Picamera2() as camera:
            video_configuration = camera.create_video_configuration()
            camera.configure(video_configuration)
            encoder = H264Encoder(bitrate=3000)
            camera.start_recording(encoder, self.recordingBufferFileIO)
            time.sleep(opt.record_time)  # record for a certain duration
            camera.stop_recording()

        # Load the recorded video and process it frame by frame
        video = cv2.VideoCapture(self.recordingBufferFileIO)
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            inputs = torch.from_numpy(np.array(frame)).float()
            with torch.no_grad():
                inputs = Variable(inputs)
                outputs = self.model(inputs)
            if not opt.no_softmax_in_test:
                outputs = F.softmax(outputs, dim=1)

            print(f"Current output: {outputs}")

        video.release()

    def predict(self, inputs):
        return self.model(inputs)

    def predict_with_camera(self):
        from picamera2 import Picamera2
        assert is_raspberry_pi(), "This method is only available on Raspberry Pi"

        # return self.model(inputs)