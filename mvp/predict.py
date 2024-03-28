import io
import time
import threading

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from torch.autograd import Variable
from realtime.model import generate_model

from hw import is_raspberry_pi

RECORDING_BUFFER_PATH = "/tmp/recording.h264"

MODEL_PATH = 'realtime/trained_models/Pretrained models/egogesture_resnetl_10_RGB_8.pth'
MODEL_TYPE = 'resnetl'


class GestureService:
    def __init__(self, opt):
        self.opt = opt
        self.model = generate_model(opt)
        # self.recordingBuffer = io.BytesIO()
        self.recordingBufferFileIO = FileOutput(RECORDING_BUFFER_PATH)
        self.stop_semaphore = threading.Event()
        self.camera = None

    def __start_recording__(self):
        self.camera = Picamera2()
        video_configuration = self.camera.create_video_configuration()
        self.camera.configure(video_configuration)
        encoder = H264Encoder(bitrate=30000)
        self.camera.start_recording(encoder, self.recordingBufferFileIO)

    # Non-blocking method in a separate thread
    def start_recording(self):
        def wrapper():
            self.__start_recording__()
            self.stop_semaphore.clear()
            while not self.stop_semaphore.is_set():
                time.sleep(1)
            self.camera.stop_recording()

        threading.Thread(target=wrapper).start()

        return self.stop_semaphore.set

    def test(self):
        print('predict')

        # self.model.eval()

        stop_recording = self.start_recording()
        time.sleep(5)
        stop_recording()

        video = cv2.VideoCapture(RECORDING_BUFFER_PATH)
        # video = cv2.VideoCapture(self.recordingBufferFileIO)
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            inputs = torch.from_numpy(np.array(frame)).float()
            with torch.no_grad():
                inputs = Variable(inputs)
                outputs = self.model(inputs)
            if not self.opt.no_softmax_in_test:
                outputs = F.softmax(outputs, dim=1)

            print(f"Current output: {outputs}")

        video.release()

    def predict_with_camera(self):
        assert is_raspberry_pi(), "This method is only available on Raspberry Pi"

        # return self.model(inputs)
