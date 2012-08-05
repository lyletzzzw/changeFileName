#! /usr/bin/env python
#coding=utf-8

'''
    重命名文件
'''
import os
import re

from mutagen.mp3 import MP3
import sys
import mutagen.id3
from mutagen.easyid3 import EasyID3

def getFileClass(fileName,module=sys.modules[MP3.__module__]):
    subClass = '%s' % os.path.splitext(fileName)[1].upper()[1:]
    return getattr(module,subClass)

def reFileName(folderStr,srcStr,destStr):
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
        

def replaceStr(originalStr,srcStr,destStr):
    '''
        将protoStr中的srcStr字符串替换为destStr字符串
        originalStr:原始的字符串
        srcStr：为源字符串
        destStr:为目标字符串
    '''
    return originalStr.replace(srcStr,destStr)

def replaceStrforRE(originalStr,srcFormate,destFormate):
    '''
        使用正则表达式进行替换字符串
        
        originalStr:待替换的字符串原型
            
        other:
        re:r'^\s*[_]*(\d+)\s*$'
        format:r'\1点'
        
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
    
    
    result = re.sub(srcFormate,destFormate,originalStr)
    if result==originalStr:
        return None
    else:
        return result


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
    main()
