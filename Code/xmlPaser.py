import os;
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def GetCurDir():
    return  os.getcwd();

def read_xml(xml_path):
    tree = ET.parse(xml_path);
    return tree;

def create_dict(root):
    """
    :param root:
    :return:
    """
    dict_new={};
    print(root.tag);
    print(len(root));
    #print(root.attrib["name"]);
    for key,val in enumerate(root):
        dict_init={};#是字典，map
        list_init=[];#数组list
        #print(val.tag);
        print(val.attrib);
        for k,v in enumerate(val.attrib):
            print(v);
            print(val.attrib[v]);
            print(val.attrib.get(v));
            print(val.attrib.get(v));

        return ;

        #遍历属性
        for attr in val.attrib:
            print(attr);

        return ;
        for item in val:
            list_init.append([item.tag,item.text]);#数组里面放了数组
        #print(list_init);
        for lists in list_init:#lists是数组
            dict_init[lists[0]]=lists[1];

        dict_new[key]=dict_init;
        #print(dict_new);
    return  dict_new;

def MainFunc():
    print(GetCurDir());
    xmpPaht = GetCurDir()+"\\config\\xmlPaserIn.xml";
    xmlroot = read_xml(xmpPaht);
    create_dict(xmlroot.getroot());

if __name__ == '__main__':
    MainFunc();
