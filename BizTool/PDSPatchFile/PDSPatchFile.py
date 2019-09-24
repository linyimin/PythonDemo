import os;
import hashlib;

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return "";
    myhash = hashlib.md5();
    f = open(filename, 'rb');
    while True:
        b = f.read(8096)
        if not b:
            break;
        myhash.update(b);
    f.close()
    return myhash.hexdigest()

def AnaysisDiff(strRootNew,strRootOld,strCurDir):
    list = os.listdir(strCurDir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(strCurDir, list[i]);
        if os.path.isfile(path):
            newMD5=GetFileMd5(path);
            strOldPath = path.replace(strRootNew,strRootOld);
            oldMD5 = GetFileMd5(strOldPath);
            #print(path + "--" + newMD5);
            #print(strOldPath);
            if newMD5!=oldMD5:
                #print(path);
                print(path.replace(strRootNew, ""));
        else:
            AnaysisDiff(strRootNew,strRootOld,path);

def MainProc():
    AnaysisDiff("2.7.0\\","2.6.0\\","2.7.0\\");




if __name__  =="__main__":
    MainProc();