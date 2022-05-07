from asyncio.windows_events import NULL
from pickle import TRUE
import string
from time import monotonic
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os
from PIL import Image
 
class DataMain(object):

    test_mode = True

    @property
    def video_path(self):
        return self.video_path
    @video_path.setter
    def video_path(self,value):
        if isinstance(value,string):
            self.video_path = value
        else:
            print("error")

    @property
    def imgset_path(self):
        return self.imgset_path
    @imgset_path.setter
    def imgset_path(self,value):
        if isinstance(value,string):
            self.imgset_path = value
        else:
            print("error")

    @property
    def model(self):
        return self.model
    @model.setter
    def model(self,value):
        if isinstance(value,string):
            self.model = value
        else:
            print("error")

    @property
    def taget_img_path(self):
        return self.img_set_path
    @taget_img_path.setter
    def taget_img_path(self,value):
        if isinstance(value,string):
            self.img_set_path = value
        else:
            print("error")





    #图片压缩
    def image_processing(self):
        #  待处理图片路径
        img_path = Image.open('./images/1.png')
    	#  resize图片大小，入口参数为一个tuple，新的图片的大小
        img_size = img_path.resize((520, 520))
    	#  处理图片后存储路径，以及存储格式
        img_size.save('./images_1/i.jpg', 'JPEG')

    #视频转图片
    def video_to_pic(self):
        cap = cv2.VideoCapture(self.videoPath)
        if (cap==NULL):
            print("Wrong video path")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取宽度
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取高度
        suc = cap.isOpened()  # 是否成功打开
        frame_count = 0
        while suc:
            frame_count += 1
            suc, frame = cap.read()
            if ~suc:
                return
            if frame_count%int(fps+1) == 0 :
                cv2.imwrite(self.imgPath + "%d.jpg" %frame_count, frame)
                cv2.waitKey(1)
            #cv2.imwrite(imgPath + str(frame_count).zfill(4), frame)     
        cap.release()
        print("视频转图片结束！")


    def __init__(self):
        pass

if __name__ == '__main__':
    data_class = DataMain()
    data_class.image_processing()