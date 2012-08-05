#! /usr/bin/env python
#coding=utf-8

'''
    重命名文件
'''
import sys
import getopt
import os
import re

from mutagen.mp3 import MP3
import mutagen.id3
from mutagen.easyid3 import EasyID3

from dict import Dict
from dict import DictMixin

class MP3FileInfo(Dict):
    
    def __init__(self,f):
        Dict.__init__(self)
        
        self.mp3File = MP3(f,ID3=EasyID3)
        
        self['fileName']=f
        self['srcName']=f
    
    def save(self):
        
        self.mp3File.save()
        
        print self['srcName']
        print self['fileName']
        
        os.rename(self['srcName'],self['fileName'])
        self['srcName']=self['fileName']
        
        
    
    

class MatchFileName(object):
    '''
        匹配文件名
    '''
    
    '''
        常用的元字符    
        代码  说明
        .     匹配除换行符以外的任意字符
        \w 	  匹配字母或数字或下划线或汉字
        \s 	  匹配任意的空白符
        \d 	  匹配数字
        \b 	  匹配单词的开始或结束
        ^ 	  匹配字符串的开始
        $ 	  匹配字符串的结束
    '''
    
    
    def replace(srcFormate,destFormate,originalStr):
        '''
            使用正则表达式进行替换字符串
            @param originalStr:待替换的字符串原型
            @param srcFormate:匹配模式
            @param destFormate:替换模式
                  
            @return 如果匹配成功返回替换后的字符串，否则返回None
        '''
        print srcFormate
        print destFormate
        print originalStr
    
        result = re.sub(srcFormate,destFormate,originalStr)
        if result==originalStr:
            return None
        else:
            return result
    replace=staticmethod(replace)




class FilterStr(object):
    '''
        过滤字符串
    '''
    
    #要过滤的字符串和对应的字符串值
    filterChar={r'[':r'\[',
                r']':r'\]',
                r'{':r'\{',
                r'}':r'\}',
                r'-':r'\-',
                r'^':r'\^',
                r'$':r'\$'
            }
    
    def handler(self,str):
        '''
            过滤字符串方法
            
            str：原字符串
            return：返回过滤有的字符串的值
        '''
        for elem in FilterStr.filterChar:
            str = str.replace(elem,FilterStr.filterChar[elem])
            
        return str

def getFileClass(fileName,module=sys.modules[MP3FileInfo.__module__]):
    '''
        获取Class
    '''
    
    subClass = '%sFileInfo' % os.path.splitext(fileName)[1].upper()[1:]
    obj = getattr(module,subClass)
    if callable(obj):
        return obj  
    else:
        return None

def replace(folderStr,srcStr,destStr):
    '''
        替换目录中文件的字符串
        folderStr:目录
        srcStr:原字符串
        destStr:目标字符串，默认为None，替换将成为空
    '''
    
    expandFlag = raw_input(u'是否进行深度修改:')

    li = os.listdir(folderStr)
    for elem in li:
        fileName = replaceStrforRE(elem,srcStr,destStr)
        if fileName!=None:
            f = os.path.join(folderStr,fileName)
            os.rename(os.path.join(folderStr,elem),f)
            
            if expandFlag=='y' or expandFlag=='Y':
                mp3File = getFileClass(fileName)(f,ID3=EasyID3)
                mp3File['title']=fileName.split('.')[0]
                mp3File.save()
                
            print f


def replaceFiles(dir,fileExtList,matchModelDict):
    '''
        修改文件名称
    '''
    
    fileList=[]
    for f in os.listdir(dir):
        if os.path.splitext(f)[1] in fileExtList:
            result = MatchFileName.replace(matchModelDict['srcFormate'],\
                    matchModelDict['destFormate'],f)
            mp3File = getFileClass(f)(os.path.join(dir,f))
            print dir
            print result
            result = os.path.join(dir,result)
            '''
            mp3File['fileName']=result
            mp3File['title']=result
            mp3File.save()
            fileList.append(mp3File)
            '''
    return fileList
    

def command(argv):
    
    opts,arg = getopt.getopt(argv,'hf:e:s:t:',['help','folder=','ext=','srcModel=','targetModel=']);
    print opts
    print arg
    
    dir = ''
    fileExtList = []
    matchModelDict = {}
    for opt,arg in opts:
        if opt in ('-f','-folder='):
            dir = opt
        elif opt in ('-e','-ext='):
            fileExtList.append(opt)
        elif opt in ('-s','srcModel='):
            matchModelDict['srcFormate']=opt
        elif opt in ('-t','targetModel='):
            matchModelDict['destFormate']=opt
    
    replaceFiles(dir,fileExtList,matchModelDict)    
    
def main():
    #输入必须的参数
    folderStr=raw_input(u'目录：')
    folderStr = os.path.normpath(folderStr)
    srcStr = raw_input(u'原字符串：')
    destStr = raw_input(u'目标字符串：')
    
    #处理表达式的特殊值
    srcStr = FilterStr().handler(srcStr)
    
    #重命名文件名称
    reFileName(folderStr,srcStr,destStr)    

if __name__=='__main__':
    #main()
    #command(sys.argv[1:])
    replaceFiles(ur'E:\tmp\有声小说\黄河鬼棺2[全35集]',['.mp3'],{'srcFormate':ur'AA_(\d+).mp3','destFormate':ur'AA_\1.mp3'})
    
    #replaceFiles(ur'E:\WorkSpace\Python\notes\API',['.mp3'],{'srcFormate':'','srcFormate':''})
