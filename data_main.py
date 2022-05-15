from datetime import datetime, timedelta
from pickle import TRUE
import string
from time import monotonic
import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os
from PIL import Image
from pathlib import Path
import datetime

class DataMain(object):

    def __init__(self):
        pass

    @property
    def video_path(self):
        return self.__video_path
    @video_path.setter
    def video_path(self,value):
        if isinstance(value,str):
            self.__video_path = value
        else:
            print("error")

    @property
    def output_path(self):
        return self.__output_path
    @output_path.setter
    def output_path(self,value):
        if isinstance(value,str):
            self.__output_path = value
        else:
            print("error")
 
    @property
    def imgset_path(self):
        return self.__imgset_path
    @imgset_path.setter
    def imgset_path(self,value):
        if isinstance(value,str):
            self.__imgset_path = value
        else:
            print("error")

    @property
    def model(self):
        return self.__model
    @model.setter
    def model(self,value):
        if isinstance(value,str):
            self.__model = value
        else:
            print("error")

    @property
    def taget_img_path(self):
        return self.__taget_img_path
    @taget_img_path.setter
    def taget_img_path(self,value):
        if isinstance(value,str):
            self.__taget_img_path = value
        else:
            print("error")

    __location = ""
    __time = datetime.datetime.now()
    __video_name = ""

    #路径读取
    def path_breakdown(self):
        point = self.__video_name.find('_')
        if (point == -1):
            print("Wrong Video Name")
            return -1
        self.__location = self.__video_name[0:point]
        __timestr = self.__video_name[point+1:]
        self.__time = datetime.datetime.strptime(__timestr,"%Y%m%d%H%M%S")
        return 0

    #图片压缩及保存
    def img_compressing(self,image,order):
        #  待处理图片路径
        #img_path = Image.open('./images/1.png')
    	#  resize图片大小，入口参数为一个tuple，新的图片的大小
        compressed_image = image.resize((64, 128))
    	#  处理图片后存储路径，以及存储格式
        saved_path = self.__output_path+self.__location+"/"+self.__time.strftime("%Y%m%d%H%M%S")+".jpg"
        print(saved_path)
        compressed_image.save(saved_path, 'JPEG')
        self.__time+=datetime.timedelta(seconds = 1)

    #视频转图片
    def video_to_pic(self):
        
        #创建文件夹
        __order = 1;
        while os.path.exists(self.__output_path+self.__location+str(__order)+"/"):
            __order+=1
        self.__location += str(__order)
        os.mkdir(self.__output_path+self.__location+"/")

        #读取视频文件
        cap = cv2.VideoCapture(self.__video_path)
        cv2.waitKey(0)
        #print(self.__video_path)
        # if (~suc):
        #     print("Wrong video path")
        #     return
        fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取宽度
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取高度
        len = min(width,height//2)
        midx = width//2;
        midy = height//2;
        frame_count = 0
        img_count = 0
        flag =cap.isOpened()
        #按帧切割
        while flag:
            frame_count += 1
            flag,frame = cap.read()
            if not flag:
                break
            if frame_count%int(fps+1) == 0 :
                x0 = midx-len//2
                x1 = midx+len//2
                y0 = midy-len
                y1 = midy+len
                crop_img = frame[y0:y1,x0:x1] 
                img_count+=1
                #cv2.imwrite("C:\\VScode\\"+str(img_count)+".jpg", frame)
                image = Image.fromarray(cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB))
                self.img_compressing(image,img_count)
                
                
            cv2.waitKey(1)    
            #cv2.imwrite(imgPath + str(frame_count).zfill(4), frame)     
        cap.release()
        print("视频转图片结束！")

    def execute(self):
        self.__video_name = Path(self.__video_path).stem
        if(self.path_breakdown()==-1):
            return -1
        self.video_to_pic();
        return 0


 #交互端调用时，需修改 video_path(视频文件路径) 和 output_path(目标文件夹路径)，然后调用execute函数
 #该模块会生成一个文件夹，储存由视频导出的图片。
 #导出的用时和视频时长差不多，测试时建议使用较短的视频。
if __name__ == '__main__':
    data_class = DataMain()
    data_class.video_path = "C:/VScode/食堂_20220515085959.mp4"
    data_class.output_path = "C:/Vscode/"
    data_class.execute()
