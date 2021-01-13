from PIL import Image
import numpy as np
import json
def imageHandle(file):
    class_dict=dict()
    with open("./class_config.json",'r') as f:
        class_dict=json.load(f)
    # 第一次load之后还是str类型，再loads一次 变成dict类型
    class_dict=json.loads(class_dict)
    # 读取图片 通过PIL 模块
    im = Image.open(file)
    im = im.convert('RGB') # 指定图片为RGP格式
    # print(im.format, im.size, im.mode)
    arr = np.array(im) # 转换为numpy数组
    # print(arr.shape, arr.dtype)
    color_dict={}
    for i in arr:
        for j in i: # RGB 3个元素的np.array
            for k, v in class_dict.items():
                if list(j)==v: # 与json字典进行匹配
                    color_dict[k]=color_dict.get(k,0)+1
                    break
            # color_dict[j]=color_dict.get(j,0)+1
    # print(color_dict)
    # 换算为百分比并且进行排序
    sum=0
    for k in color_dict:
        sum+=color_dict[k]
    # print("sum:",sum)
    for k,v in color_dict.items():
        color_dict[k]=round(v/sum*100,2)
    return sorted(color_dict.items(),key=lambda x:x[1],reverse=True)

# new_im = Image.fromarray(arr)
# new_im.show()

# im2 = Image.open("testPic3.png")
# im2 = im2.convert('RGB') # L RGB
# arr2 = np.array(im2)
# im2.show()
# print(arr2.shape, arr2.dtype)
# print(arr2)
# new_im = Image.fromarray(arr2)
# new_im.show()