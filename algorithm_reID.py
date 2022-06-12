import argparse
import scipy.io
import torch
import numpy as np
import os
import shutil
from torchvision import datasets

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def reid():
    shutil.rmtree('./test/result')
    os.mkdir('./test/result')

    file_path = 'test/pytorch'
    result_path = "./test/result/"
    gallery_path = 'test/pytorch/gallery'

    # 导入目标图片序号和所有图片路径
    parser = argparse.ArgumentParser(description='algorithm_reID')
    parser.add_argument('--query_index', default=0, type=int, help='test_image_index')
    parser.add_argument('--test_dir', default=file_path, type=str, help='./test_data')
    opts = parser.parse_args()
    # print("opts:",opts)
    data_dir = opts.test_dir
    # print("data_dir:",data_dir)
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x)) for x in ['gallery', 'query']}

    # 从mat文件中读取所有图片的特征值
    result = scipy.io.loadmat('pytorch_result.mat')
    query_feature = torch.FloatTensor(result['query_f'])
    query_cam = result['query_cam'][0]
    query_label = result['query_label'][0]
    gallery_feature = torch.FloatTensor(result['gallery_f'])
    gallery_cam = result['gallery_cam'][0]
    gallery_label = result['gallery_label'][0]
    query_feature = query_feature.cuda()
    gallery_feature = gallery_feature.cuda()

    # 找到目标图片的特征值，和与目标图片特征值相似的前十张图片
    i = opts.query_index
    # print("i=",i)
    index = sort_img(query_feature[i], query_label[i], query_cam[i], gallery_feature, gallery_label, gallery_cam)
    # print("index=",index)

    # 结果可视化
    # Visualize the rank result
    query_path, _ = image_datasets['query'].imgs[i]
    query_label = query_label[i]
    # print("目标图片为", query_path)
    print('Top 10 images are as follow:')
    try:  # Visualize Ranking Result
        # Graphical User Interface is needed
        for i in range(10):
            img_path, _ = image_datasets['gallery'].imgs[index[i]]
            temp = img_path.rfind('\\')
            fig_name = img_path[temp + 1:]
            print(fig_name)
            copy_files(gallery_path, fig_name, result_path)
    except RuntimeError:
        for i in range(10):
            img_path = image_datasets.imgs[index[i]]
            print(img_path[0])
        print('Algorithm Error')

#####################################################################
# Show result
def imshow(path, title=None):
    """Imshow for Tensor."""
    im = plt.imread(path)
    plt.imshow(im)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


######################################################################

#######################################################################
# sort the images
def sort_img(qf, ql, qc, gf, gl, gc):
    query = qf.view(-1, 1)
    # print(query.shape)
    score = torch.mm(gf, query)
    score = score.squeeze(1).cpu()
    score = score.numpy()
    # predict index
    index = np.argsort(score)  # from small to large
    index = index[::-1]
    # index = index[0:2000]
    # good index
    query_index = np.argwhere(gl == ql)
    # same camera
    camera_index = np.argwhere(gc == qc)

    # good_index = np.setdiff1d(query_index, camera_index, assume_unique=True)
    junk_index1 = np.argwhere(gl == -1)
    junk_index2 = np.intersect1d(query_index, camera_index)
    junk_index = np.append(junk_index2, junk_index1)

    mask = np.in1d(index, junk_index, invert=True)
    index = index[mask]
    return index

########################################################################

# 复制结果图片到result文件夹
def copy_files(path, name, result_path):
    for foldName, subfolders, filenames in os.walk(path):  # 用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
        for filename in filenames:  # 遍历列表下的所有文件名
            if filename == name:  # 当文件名为结果图片名时
                if filename.endswith('.jpg'):  # 当文件名以.jpg后缀结尾时
                    new_name = filename.replace('.jpg', '_result.jpg')  # 为文件赋予新名字
                    shutil.copyfile(os.path.join(foldName, filename),
                                    os.path.join(result_path, new_name))  # 复制并重命名文件
                    # print(filename, "copied as", new_name)  # 输出提示

if __name__ == '__main__':
    shutil.rmtree('./test/result')
    os.mkdir('./test/result')

    file_path = 'test/pytorch'
    result_path = "./test/result/"
    gallery_path = 'test/pytorch/gallery'

    # 导入目标图片序号和所有图片路径
    parser = argparse.ArgumentParser(description='algorithm_reID')
    parser.add_argument('--query_index', default=0, type=int, help='test_image_index')
    parser.add_argument('--test_dir', default=file_path, type=str, help='./test_data')
    opts = parser.parse_args()
    # print("opts:",opts)
    data_dir = opts.test_dir
    # print("data_dir:",data_dir)
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x)) for x in ['gallery', 'query']}

    # 从mat文件中读取所有图片的特征值
    result = scipy.io.loadmat('pytorch_result.mat')
    query_feature = torch.FloatTensor(result['query_f'])
    query_cam = result['query_cam'][0]
    query_label = result['query_label'][0]
    gallery_feature = torch.FloatTensor(result['gallery_f'])
    gallery_cam = result['gallery_cam'][0]
    gallery_label = result['gallery_label'][0]
    query_feature = query_feature.cuda()
    gallery_feature = gallery_feature.cuda()

    # 找到目标图片的特征值，和与目标图片特征值相似的前十张图片
    i = opts.query_index
    # print("i=",i)
    index = sort_img(query_feature[i], query_label[i], query_cam[i], gallery_feature, gallery_label, gallery_cam)
    # print("index=",index)

    # 结果可视化
    # Visualize the rank result
    query_path, _ = image_datasets['query'].imgs[i]
    query_label = query_label[i]
    print("目标图片为", query_path)
    print('Top 10 images are as follow:')
    try:  # Visualize Ranking Result
        # Graphical User Interface is needed
        fig_result = plt.figure(figsize=(16, 4))
        ax = plt.subplot(1, 11, 1)
        ax.axis('off')
        imshow(query_path, 'query')
        for i in range(10):
            ax = plt.subplot(1, 11, i + 2)
            ax.axis('off')
            img_path, _ = image_datasets['gallery'].imgs[index[i]]
            imshow(img_path)
            temp = img_path.rfind('\\')
            fig_name = img_path[temp + 1:]
            print(img_path)
            copy_files(gallery_path, fig_name, result_path)
    except RuntimeError:
        for i in range(10):
            img_path = image_datasets.imgs[index[i]]
            print(img_path[0])
        print('Algorithm Error')

    fig_result.savefig("test/result/result.png")
    plt.close('all')  # 关闭所有 figure windows