import numpy as np
import cv2
import os
import shutil
# i=0
# b=".jpg"
# # 复制结果图片到result文件夹
# for foldName, subfolders, filenames in os.walk("D:/video/old"):     #用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
#     for filename in filenames:                         #遍历列表下的所有文件名
#         if filename.endswith('.jpg'):                #当文件名以.jpg后缀结尾时
#             old_name=filename
#             name = str(i) + b
#             new_name=filename.replace(old_name,name)               #为文件赋予新名字
#             i = i + 1
#             shutil.copyfile(os.path.join(foldName,filename), os.path.join("D:/video/new",new_name))    #复制并重命名文件
#             print(filename,"copied as",new_name)           #输出提示
target_path = "D:/video/new"
target_image = os.listdir(target_path)
list = []
for file in target_image:
        list.append(file)
print("length:", len(target_image))
print("list:",list)
#读取一张图片
img = cv2.imread('D:/video/new/1.jpg')
imgInfo = img.shape
size = (imgInfo[1],imgInfo[0])
print(size)
videowrite = cv2.VideoWriter(r'D:\test.mp4',-1,20,size)#20是帧数，size是图片尺寸
img_array=[]
for filename in [r'D:/video/new/{0}.jpg'.format(i) for i in range(len(list))]:#这个循环是为了读取所有要用的图片文件
    img = cv2.imread(filename)
    if img is None:
        print(filename + " is error!")
        continue
    img_array.append(img)
for i in range(len(list)):#把读取的图片文件写进去
    videowrite.write(img_array[i])
videowrite.release()

print('end!')