import os
import shutil

def main():
    userTest('./localPicture/testPic2.png')


def mycopyfile(srcfile,dstpath):                       # 复制函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.copy(srcfile, dstpath + fname)          # 复制文件
        print ("copy %s -> %s"%(srcfile, dstpath + fname))

def userTest(filepath):
    data_path = './minicity/leftImg8bit/user_test/'
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    else:
        try:
            clear_user_test(data_path) # 清空user_test文件夹
        except Exception:
            print("删除失效")
    mycopyfile(filepath,data_path) # 复制文件到目标文件夹
    _,filename = os.path.split(filepath)
    filename,sufix = filename.split('.') # 分离文件名和后缀 后缀必须是png
    os.system('python baseline.py --save_path resnet50 --batch_size 4 --predict  --num_workers 0') # 进行模型预测
    result_path = './resnet50/results_color_user_test/'
    filename = filename+"_prediction.png"
    result_file = os.path.join(result_path, filename)
    print("The result path: "+result_file)
    return filename
  
def clear_user_test(path):
    shutil.rmtree(path)  
    os.mkdir(path)  

if __name__ == '__main__':
    main()
