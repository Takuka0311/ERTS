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
import random
# from algorithm_main import AlgorithmMain
from algorithm_reID import reid

class DataMain(object):

    def __init__(self):
        super().__init__()
        self.__video_path_list = []
        self.__target_image_path = None
        self.__model = None
        self.__image_set_path = None
        self.__video_path = None
        self.__output_path = None
        self.__video_path = None
        self.__recognition = list(list())

    @property
    def video_path_list(self):
        return self.__video_path_list

    @video_path_list.setter
    def video_path_list(self, value):
        if isinstance(value, list):
            self.__video_path_list = value
        else:
            print("error")

    @property
    def output_path(self):
        return self.__output_path

    @output_path.setter
    def output_path(self, value):
        if isinstance(value, str):
            self.__output_path = value
        else:
            print("error")

    @property
    def image_set_path(self):
        return self.__image_set_path

    @image_set_path.setter
    def image_set_path(self, value):
        if isinstance(value, str):
            self.__image_set_path = value
        else:
            print("error")

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        if isinstance(value, str):
            self.__model = value
        else:
            print("error")

    def get_recognition_result(self):
        return self.__recognition;

    @property
    def target_img_path(self):
        return self.__target_image_path

    @target_img_path.setter
    def target_img_path(self, value):
        if isinstance(value, str):
            self.__target_image_path = value
        else:
            print("error")

    __location = ""
    __time = datetime.datetime.now()
    __video_name = ""

    # ????????????
    def path_breakdown(self):
        point = self.__video_name.find('_')
        if point == -1:
            print("Wrong Video Name")
            return -1
        self.__location = self.__video_name[0:point]
        __time_str = self.__video_name[point + 1:]
        self.__time = datetime.datetime.strptime(__time_str, "%Y%m%d%H%M%S")

        return 0

    # ?????????????????????
    def img_compressing(self, image):
        # ?????????????????????
        # img_path = Image.open('./images/1.png')
        # resize????????????????????????????????????tuple????????????????????????
        compressed_image = image.resize((64, 128))
        # ????????????????????????????????????????????????
        saved_path = self.__output_path + self.__location + "/" +"0001_"+ self.__time.strftime("%Y%m%d%H%M%S") + ".jpg"
        print(saved_path)
        compressed_image.save(saved_path, 'JPEG')
        #rand = random.randint(0, 5)
        #if rand == 0:
        
        self.__time += datetime.timedelta(seconds=1)

    def path_init(self,line,time):
        result_path = "./test/result/"
        self.__recognition.append([datetime.datetime.strptime(time, "%Y%m%d%H%M%S"), self.__location, result_path+line+".jpg"])

    # ???????????????
    def video_to_pic(self):

        # ???????????????
        __order = 1
        while os.path.exists(self.__output_path + self.__location + str(__order) + "/"):
            __order += 1
        self.__location += str(__order)
        os.mkdir(self.__output_path + self.__location + "/")

        # ??????????????????
        cap = cv2.VideoCapture(self.__video_path)
        cv2.waitKey(0)
        # print(self.__video_path)
        # if (~suc):
        #     print("Wrong video path")
        #     return
        fps = cap.get(cv2.CAP_PROP_FPS)  # ????????????
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # ????????????
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # ????????????
        pic_len = min(width, height // 2)
        mid_x = width // 2
        mid_y = height // 2
        frame_count = 0
        img_count = 0
        flag = cap.isOpened()
        # ????????????
        while flag:
            frame_count += 1
            flag, frame = cap.read()
            if not flag:
                break
            if frame_count % int(fps + 1) == 0:
                
                x0 = mid_x - pic_len // 2
                x1 = mid_x + pic_len // 2
                y0 = mid_y - pic_len
                y1 = mid_y + pic_len
                crop_img = frame[y0:y1, x0:x1]
                img_count += 1
                # cv2.imwrite("C:\\VScode\\"+str(img_count)+".jpg", frame)
                image = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
                self.img_compressing(image)

            cv2.waitKey(1)
            # cv2.imwrite(imgPath + str(frame_count).zfill(4), frame)
        cap.release()
        print("????????????????????????")

    def execute(self):
        self.__recognition = []
        file=open('path', encoding='UTF-8')
        loca = file.readline().strip()
        self.__location = loca
        for line in file:
            line = line.strip()
            _time = file.readline().strip()
            self.path_init(line,_time)
        
        for self.__video_path in self.__video_path_list:
            self.__video_name = Path(self.__video_path).stem
            if self.path_breakdown() == -1:
                return -1
            self.video_to_pic()
        # shutil.rmtree('./test/result')
        # os.mkdir('./test/result')
        # algorithm_class = AlgorithmMain()
        # algorithm_class.execute()
        # algorithm_class.target_path_test = "./test/target/"
        # algorithm_class.all_path_test_list = ["./test/output/??????1/", "./test/output/??????1/", "./test/output/??????1/"]
        # algorithm_class.execute()
        reid()
        return 0


# ?????????????????????????????? video_path(??????????????????) ??? output_path(?????????????????????)???????????????execute??????
# ?????????????????????????????????????????????????????????????????????
# recognition_result????????????????????????????????????datetime,string???string
# ?????????????????????????????????????????????????????????????????????????????????
if __name__ == '__main__':
    print(os.getcwd())
    data_class = DataMain()
    data_class.video_path_list = ["./test/??????_20220520230123.mp4"]
    data_class.output_path = "./test/output/"
    data_class.execute()
    print(data_class.get_recognition_result())
