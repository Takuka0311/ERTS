import os
import shutil
reid = "6543_"
i=0
b=".jpg"
# 复制结果图片到result文件夹
for foldName, subfolders, filenames in os.walk("D:/video/old"):     #用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
    for filename in filenames:                         #遍历列表下的所有文件名
        if filename.endswith('.jpg'):                #当文件名以.jpg后缀结尾时
            old_name=filename
            name = reid + str(i) + b
            new_name=filename.replace(old_name,name)               #为文件赋予新名字
            i = i + 1
            shutil.copyfile(os.path.join(foldName,filename), os.path.join("D:/video/output",new_name))    #复制并重命名文件
            print(filename,"copied as",new_name)           #输出提示


print('end!')