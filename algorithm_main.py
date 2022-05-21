import os
import json
import shutil

class AlgorithmMain(object):

    def __init__(self):
        self.__target_path = None
        self.__all_path_list = []
        shutil.rmtree('./test/result')
        os.mkdir('./test/result')

    @property
    def target_path_test(self):
        return self.__target_path

    @target_path_test.setter
    def target_path_test(self, value):
        if isinstance(value, str):
            self.__target_path = value
        else:
            print("error")

    @property
    def all_path_test_list(self):
        return self.__all_path_list

    @all_path_test_list.setter
    def all_path_test_list(self, value):
        if isinstance(value, list):
            self.__all_path_list = value
        else:
            print("error")

    # 获取目标图片的id
    def get_target_pic(self, target_path):
        target_image = os.listdir(target_path)
        target_image_id = "0000"
        if(len(target_image) > 1):
            print("Error:There is more than one target image.")
        else:
            for file in target_image:
                print("target_path_test:",file)
                target_image_id = file[0:4:]
            print("target_image_id:", target_image_id)
        return target_image_id

    # 获取所有场景图片中与目标图片id相同的列表并输出到result文件夹
    def get_output_pic(self, all_path_list, target_id):
        result_path = "./test/result/"
        result_image_list = []
        for all_path in all_path_list:
            print("path:",all_path)
            output_image_list = os.listdir(all_path)
            for file in output_image_list:
                if(file[0:4:] == target_id):
                    result_image_list.append(file)
                    self.copy_files(all_path, file, result_path)

        return result_image_list

    # 复制结果图片到result文件夹
    def copy_files(self, path,name,result_path):
        for foldName, subfolders, filenames in os.walk(path):     #用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
               for filename in filenames:                         #遍历列表下的所有文件名
                  if filename == name:                            #当文件名为结果图片名时
                      if filename.endswith('.jpg'):                #当文件名以.jpg后缀结尾时
                         new_name=filename.replace('.jpg','_result.jpg')               #为文件赋予新名字
                         shutil.copyfile(os.path.join(foldName,filename), os.path.join(result_path,new_name))    #复制并重命名文件
                         print(filename,"copied as",new_name)           #输出提示

    def execute(self):
        target_id = self.get_target_pic(self.__target_path)
        result_list = self.get_output_pic(self.__all_path_list, target_id)
        print("共找到", len(result_list), "张相似图片")
        print("相似图片:", result_list)

if __name__ == '__main__':
    #shutil.rmtree('./test/result')
    #os.mkdir('./test/result')
    algorithm_class = AlgorithmMain()
    #algorithm_class.execute()
    algorithm_class.target_path_test = "./test/target/"
    algorithm_class.all_path_test_list = ["./test/output/食堂1/","./test/output/教室1/","./test/output/fake/"]
    algorithm_class.execute()