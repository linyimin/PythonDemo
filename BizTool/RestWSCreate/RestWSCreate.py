import os
import re
import configparser
import requests
import shutil
import subprocess
from xml.dom.minidom import parse
import xml.dom.minidom

def GetConfigValue(group, name):
	"""
	读取ini文件中的值
	group 组名
	name  对应这个组下面的的值
	"""
	config = configparser.ConfigParser()
	config.read('config.ini')
	path = config.get(group, name)
	return path

def DelDir(delDir):
    delList = os.listdir(delDir)
    for f in delList:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)

#获取文件后缀
def file_extension(path):
  return os.path.splitext(path)[1];

def GetFileBySuffix(strDir,strSuffix):
    lstOutFile=[];
    lstFile = os.listdir(strDir);
    for file in lstFile:
        if file_extension(file)==strSuffix:
            lstOutFile.append(file);
    return  lstOutFile;

def copyFiles(sourceDir, targetDir):
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
        if os.path.exists(targetFile):
            os.remove(targetFile);
        open(targetFile, "wb").write(open(sourceFile, "rb").read())

       # if os.path.isdir(sourceFile):
        #    copyFiles(sourceFile, targetFile)

def CallBat(batFile):
    print(batFile);
    print("testddddd");
    #cmd = 'cmd.exe c:\\sam.bat'
    p = subprocess.Popen("cmd.exe /c" + batFile,stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
    print(batFile);
    p.wait()



def SaveRestURLJson():
    # 读取指定rest接口网页数据
    resturl = GetConfigValue("Web", "Url");
    res = requests.get(resturl);
    res.encoding = 'utf-8';
    webContext = res.text;
    # 进行字符串替换
    webContext = webContext.replace(",s", "s");
    webContext = webContext.replace("«", "");
    webContext = webContext.replace("»", "");
    webContext = webContext.replace('"required":false', '"required":true');
    # 删除json文件
    jsonfile = GetConfigValue("Web", "jsonfile");
    print(jsonfile);
    if os._exists(jsonfile):
        os.remove(jsonfile);

    outfile = open(jsonfile, "w", encoding='utf-8')
    outfile.write(webContext);
    print("write restjson end");
    # print(webContext);

def GetURLContext():
    # 删除自动生成代码目录
    curDir= os.getcwd();
    tempCodeDir =curDir +"\\cpprest-clientnt\\";
    print(tempCodeDir);
    if os.path.exists(tempCodeDir):
        DelDir(tempCodeDir);
    print("删除自动生成代码目录");
    #调用批处理,生成代码
    os.system("ls")
    cmdDir = curDir+ "\\cmd.bat";
    print(cmdDir);
    #runAdmin(cmdDir);
    os.system(cmdDir);
   #CallBat(cmdDir);
    print("call bat 完成");

    #把api和model 把生成的文件，自动复制相关目录
    codeDir = GetConfigValue("Web", "codeDir");
    fileDir = GetConfigValue("Web", "fileDir");
    codeDir +=fileDir;
    copyFiles(tempCodeDir+"api\\",codeDir+"\\api\\");
    copyFiles(tempCodeDir + "model\\", codeDir + "\\model\\");

def GetXMLNode(collection,strNode):
    ItemGroups = collection.getElementsByTagName("ItemGroup");
    for itemGroup in ItemGroups:
        ClCompile = itemGroup.getElementsByTagName(strNode);
        if len(ClCompile) != 0:
            #print(ClCompile[0].nodeName);
            return itemGroup;

def CreateVCProjx(strFileDir,strSuffix,xmlPar,mapData,strNodeName,dom):
    codeDir = GetConfigValue("Web", "codeDir");
    fileDir = GetConfigValue("Web", "fileDir");#webservices
    dirTemp=codeDir + fileDir +"\\" + strFileDir+"\\";
    #print(dirTemp);
    #print(mapData);
    lstFile = GetFileBySuffix(dirTemp,strSuffix);
    for file in lstFile:
        val=fileDir+strFileDir+file;
        val =val.strip();
        val = val.lower();
        strRet=mapData.get(val,0);
        if (strRet==0):
            xmlData = dom.createElement(strNodeName);
            xmlData.setAttribute("Include", fileDir+"\\"+strFileDir+"\\"+file);
            xmlPar.appendChild(xmlData);
            print(val + "需要添加文件 ");

        else:
            # print("test"+val);
            i = 10;

def GetComplieMapData(pItemGroup,strNodeName):
    lstClCompile = pItemGroup.getElementsByTagName(strNodeName);
    mapClData = {'a': 1};
    for data in lstClCompile:
        vardata = data.getAttribute("Include");
        vardata = vardata.replace("\\", "");
        vardata = vardata.strip();
        vardata = vardata.lower();
        mapClData[vardata] = 1;
    # print(mapClData);
    """
    finddata = mapClData.get("webservicesJsonBody.cpp", 0);
    print(finddata);
    if finddata == 0:
        print("fail");
    else:
        print("success");
    """
    return  mapClData;


def AdjustVCProxj():
    codeDir = GetConfigValue("Web", "codeDir");
    #print(codeDir);
    #获取指定后缀文件
    lstVCFilter =GetFileBySuffix(codeDir,".vcxproj");
    if len(lstVCFilter)==0:
        return ;
    strVCXProj=codeDir +lstVCFilter[0];
    #print(strVCXProj);
    DOMTree = xml.dom.minidom.parse(strVCXProj);
    collection = DOMTree.documentElement;

    #获取编译cpp文件列表
    pCLItemGroup =GetXMLNode(collection,"ClCompile");
    mapClData=GetComplieMapData(pCLItemGroup,"ClCompile");
    CreateVCProjx("model",".cpp",pCLItemGroup,mapClData,"ClCompile",DOMTree);
    CreateVCProjx("api", ".cpp", pCLItemGroup, mapClData, "ClCompile",DOMTree);

    pIncItemGroup = GetXMLNode(collection, "ClInclude");
    mapIncData = GetComplieMapData(pIncItemGroup,"ClInclude");
    CreateVCProjx("model",".h",pIncItemGroup,mapIncData,"ClInclude",DOMTree);
    CreateVCProjx("api", ".h", pIncItemGroup, mapIncData, "ClInclude",DOMTree);

    f = open(strVCXProj, 'w')
    DOMTree.writexml(f, addindent=' ', newl='\n', encoding='utf-8')
    f.close()


def CreateFilterXML(strFileDir,strSuffix,xmlPar,mapData,strNodeName,dom):
    codeDir = GetConfigValue("Web", "codeDir");
    fileDir = GetConfigValue("Web", "fileDir");#webservices
    dirTemp=codeDir + fileDir +"\\" + strFileDir+"\\";
    #print(dirTemp);
    lstFile = GetFileBySuffix(dirTemp,strSuffix);
    for file in lstFile:
        val=fileDir+strFileDir+file;
        val = val.strip();
        val = val.lower();
        if (mapData.get(val,0)==0):
            xmlData = dom.createElement(strNodeName);
            xmlData.setAttribute("Include", fileDir+"\\"+strFileDir+"\\"+file);
            xmlPar.appendChild(xmlData);
            xmlChild = dom.createElement("Filter");
            name_text = dom.createTextNode(fileDir+ "\\" + strFileDir)
            xmlChild.appendChild(name_text)
            xmlData.appendChild(xmlChild);
            print(val + "需要添加文件 ");
            #print(val);

def AdjustFilter():
    codeDir = GetConfigValue("Web", "codeDir");
    # print(codeDir);
    # 获取指定后缀文件
    lstFilter = GetFileBySuffix(codeDir, ".filters");
    if len(lstFilter) == 0:
        return;
    strFilterFile = codeDir + lstFilter[0];
    print(strFilterFile);
    DOMTree = xml.dom.minidom.parse(strFilterFile);
    collection = DOMTree.documentElement;

    # 获取编译cpp文件列表
    pCLItemGroup = GetXMLNode(collection, "ClCompile");
    mapClData = GetComplieMapData(pCLItemGroup, "ClCompile");
    CreateFilterXML("model", ".cpp", pCLItemGroup, mapClData, "ClCompile", DOMTree);
    CreateFilterXML("api", ".cpp", pCLItemGroup, mapClData, "ClCompile", DOMTree);
    # print(str(mapClData));

    pIncItemGroup = GetXMLNode(collection, "ClInclude");
    mapIncData=GetComplieMapData(pIncItemGroup,"ClInclude");
    CreateFilterXML("model", ".h", pIncItemGroup, mapIncData, "ClInclude", DOMTree);
    CreateFilterXML("api", ".h", pIncItemGroup, mapIncData, "ClInclude", DOMTree);
    f = open(strFilterFile, 'w')
    DOMTree.writexml(f, addindent=' ', newl='\n', encoding='utf-8')
    f.close()


def main():
    print("Hello, World 接口封装开始!");
    SaveRestURLJson();
    GetURLContext();
    AdjustVCProxj();
    AdjustFilter();
    print("Hello, World 接口封装结束!");
if __name__ == '__main__':
	main()