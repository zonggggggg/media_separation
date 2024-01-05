import os
import cv2
# import numpy as np
from progress.bar import Bar


class Separation():

    def __init__(self, parts_number=3, output="output"):
        self.parts_number = parts_number
        self.output = output
        self.resolution = (16, 9)

    def rename_media(self, name):
        file_name = os.path.splitext(os.path.basename(name))
        name_left = file_name[0] + "_left" + file_name[1]
        name_middle = file_name[0] + "_middle" + file_name[1]
        name_right = file_name[0] + "_right" + file_name[1]
        return name_left, name_middle, name_right

    def fill_black(self, frame, vacant_width: int):
        left = right = int(vacant_width / 2)
        frame = cv2.copyMakeBorder(frame, 0, 0, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return frame

    def video_separation(self, video_name: str, show: bool = False):
        ratio = self.resolution[0] * 3 / self.resolution[1]
        vacant_width = 0
        video_left, video_middle, video_right = self.rename_media(video_name)
        cap = cv2.VideoCapture(video_name)
        frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if width / height <= ratio:  # fill black to left and right
            vacant_width = height * ratio - width
            width = int(height * ratio)  # update width

        writer_left = cv2.VideoWriter(os.path.join(self.output, video_left), cv2.VideoWriter_fourcc(*'H264'), fps,
                                      (int(width / self.parts_number), height))
        writer_middle = cv2.VideoWriter(os.path.join(self.output, video_middle), cv2.VideoWriter_fourcc(*'H264'), fps,
                                        (int(width / self.parts_number), height))
        writer_right = cv2.VideoWriter(os.path.join(self.output, video_right), cv2.VideoWriter_fourcc(*'H264'), fps,
                                       (int(width / self.parts_number), height))


        # test = cv2.VideoWriter(os.path.join(self.output, "test.mp4"), cv2.VideoWriter_fourcc(*'H264'), fps, (2000, 720))
        with Bar("Separating", fill="█", suffix="%(percent).1f%% - %(eta)ds", max=frame_number) as bar:
            while cap.isOpened():
                ret, frame = cap.read()
                bar.next()
                if ret:
                    if width / height <= ratio:
                        frame = self.fill_black(frame, vacant_width)
                    frame_left = frame[:, 0:int(width / self.parts_number)]
                    frame_middle = frame[:, int(width / self.parts_number):int(width / self.parts_number) * 2]
                    frame_right = frame[:, int(width / self.parts_number) * 2:width]
                    writer_left.write(frame_left)
                    writer_middle.write(frame_middle)
                    writer_right.write(frame_right)
                    # test.write(cv2.resize(frame_middle, (2000, 720), interpolation=cv2.INTER_AREA))
                    
                    if show:
                        cv2.imshow(video_left, frame_left)
                        cv2.imshow(video_middle, frame_middle)
                        cv2.imshow(video_right, frame_right)
                        cv2.waitKey(1)
                else:
                    break

        cap.release()
        writer_left.release()
        writer_middle.release()
        writer_right.release()

    def image_separation(self, image_name: str, show: bool = False):
        ratio = self.resolution[0] * 3 / self.resolution[1]
        vacant_width = 0
        image_left, image_middle, image_right = self.rename_media(image_name)
        with Bar("Separating", fill="█", suffix="%(percent).1f%% - %(eta)ds", max=1) as bar:
            bar.next()
        frame = cv2.imread(image_name)

        width = int(frame.shape[1])
        height = int(frame.shape[0])
        if width / height <= ratio:  # fill black to left and right
            vacant_width = height * ratio - width
            width = int(height * ratio)  # update width
            frame = self.fill_black(frame, vacant_width)

        frame_left = frame[:, 0:int(width / self.parts_number)]
        frame_middle = frame[:, int(width / self.parts_number):int(width / self.parts_number) * 2]
        frame_right = frame[:, int(width / self.parts_number) * 2:width]
        cv2.imwrite(os.path.join(self.output, image_left), frame_left)
        cv2.imwrite(os.path.join(self.output, image_middle), frame_middle)
        cv2.imwrite(os.path.join(self.output, image_right), frame_right)
        if show:
            cv2.imshow(image_left, frame_left)
            cv2.imshow(image_middle, frame_middle)
            cv2.imshow(image_right, frame_right)
            cv2.waitKey(1000)

    def separation(self, args: any):
        # separate video into three parts

        if not os.path.isdir(self.output):
            os.mkdir(self.output)

        if args.video:
            self.video_separation(args.video, args.show)
        elif args.image:
            self.image_separation(args.image, args.show)
