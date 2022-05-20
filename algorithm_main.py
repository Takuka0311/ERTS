import os
import json
import shutil

# class AlgorithmMain(object):

def __init__(self):
    self.__target_path = None
    self.__all_path = None
    shutil.rmtree('./test/result')
    os.mkdir('./test/result')

# 获取目标图片的id
def get_target_pic(target_path):
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
def get_output_pic(all_path_list,target_id):
    result_path = "./test/result/"
    result_image_list = []
    for all_path in all_path_list:
        print("path:",all_path)
        output_image_list = os.listdir(all_path)
        for file in output_image_list:
            if(file[0:4:] == target_id):
                result_image_list.append(file)
                copy_files(all_path, file, result_path)
    print("共找到", len(result_image_list),"张相似图片")
    print("相似图片:",result_image_list)

    return result_image_list

# 复制结果图片到result文件夹
def copy_files(path,name,result_path):
    for foldName, subfolders, filenames in os.walk(path):     #用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
           for filename in filenames:                         #遍历列表下的所有文件名
              if filename == name:                            #当文件名为结果图片名时
                  if filename.endswith('.jpg'):                #当文件名以.jpg后缀结尾时
                     new_name=filename.replace('.jpg','_result.jpg')               #为文件赋予新名字
                     shutil.copyfile(os.path.join(foldName,filename), os.path.join(result_path,new_name))    #复制并重命名文件
                     print(filename,"copied as",new_name)           #输出提示

if __name__ == '__main__':
    shutil.rmtree('./test/result')
    os.mkdir('./test/result')
    target_path_test = "./test/target/"
    target_id = get_target_pic(target_path_test)
    all_path_test_list = ["./test/output/食堂1/",
                          "./test/output/教室1/"]
    result_list = get_output_pic(all_path_test_list,target_id)