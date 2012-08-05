#! /usr/bin/env python
#coding=utf-8


def stripnulls(data):
    "strip whitespace and nulls"
    return data.replace('\00', ' ').strip()


def sizeFunc(size):
    
    '''
        获取Mp3的标签大小
    '''
    
    import binascii
    ID3V2_frame_size = int(int('0x'+binascii.b2a_hex(size[0]),16) & 0x7F) << 21 \
                    | int(int('0x'+binascii.b2a_hex(size[1]),16) & 0x7F) << 14 \
                    | int(int('0x'+binascii.b2a_hex(size[2]),16) & 0x7F) << 7 \
                    | int(int('0x'+binascii.b2a_hex(size[3]),16) & 0x7F) + 10
    
    return ID3V2_frame_size


def int16(size):
    
    import binascii
    return int('0x'+binascii.b2a_hex(size),16)

def bin(str):
    import binascii
    return binascii.b2a_hex(str)


class MP3id3v1(object):
    
    tagDataMap={'title' : (3, 33, stripnulls),#标题
                'artist'  : (33, 63, stripnulls),#艺术家
                'album'   : (63, 93, stripnulls),#专辑
                'year'    : (93, 97, stripnulls),#年份
                'comment' : (97, 127, stripnulls),#描述
                'genre'   : (127, 128, ord)#类型
                }

    def __init__(self,filename):
        self.filename=filename
        self.dictTag={}

    def parse(self):
        fsock = open(self.filename, 'ab+', 0)
        try:
            fsock.seek(-128, 2)
            tagdata = fsock.read(128)
        finally:
            fsock.close()
        if tagdata[:3] == 'TAG':
            for tag, (start, end,parseFunc) in self.tagDataMap.items():
                self.dictTag[tag]=parseFunc(tagdata[start:end])
            
    def update(self,key,val):
        
        (start,end,parseFunc) = self.tagDataMap[key]
        
        if len(val)>(end-start):
            return False
        
        f = open(self.filename,'rb+')
        try:
            f.seek(-128+start,2)
            val = '%-*s' % ((end-start),val)
            f.write(val.replace(' ','\00'))
            f.flush()
        finally:
            f.close()
        
        return True
    
class MP3id3v2(object):
    '''
        Mp3文件的ID3v2标签
    '''
    
    tagMap=[
            #标签头
            ('header',(0,3,stripnulls)),#头字符串一般为ID3
            ('version',(3,4,ord)),#版本号
            ('revision',(4,5,ord)),#副版本号
            ('flag',(5,6,stripnulls)),#标志位，暂时忽略
            ('size',(6,10,sizeFunc)),#标签大小，除了标签头的10 个字节的标签帧的大小 
        ]
        
    frameMap=[
            ('frameID',(10,14,stripnulls)),#用四个字符标识一个帧
            ('frameSize',(14,18,int16)),#帧内容的大小，不包括帧头，不得小于1
            ('frameflag',(18,20,bin)),#存放标志，只定义了6 位
            
            ('content',(20,'frameSize',stripnulls))
        ]
        
    '''
        TIT2：标题
        TPE1：作者
        TALB：专辑
        TRCK： 音轨，格式：N/M，N表示专辑中第几首，M为专辑中歌曲总数
        TYER：年份
        TCON：类型
        COMM：备注，格式：“eng\0备注内容”，其中eng表示所使用的语言
    '''
    dictFrame={'TIT2':(),'TPE1':(),'TALB':(),
                'TRCK':(),'TYER':(),'TCON':(),'COMM':()}
    
    def __init__(self,filename):
        self.filename = filename
        self.dictTag={}
        self.frame={}
        
    def parse(self):
            
        f = open(self.filename,'rb+')
        try:
            f.seek(0)
            data = f.read(10)
            
            #标签头
            for tag,(start,end,parseFunc) in self.tagMap:
                self.dictTag[tag] = parseFunc(data[start:end])
        finally:
            f.close()
            
    
    def delete(self):
        f = open(self.filename,'rb+')
        try:
            f.write('\00\00\00')
        finally:
            f.close()


def changeMp3Info(file,key,val):
    #除去ID3头，让mp3识别使用ID3v1
    f = MP3id3v2(file)
    f.delete()
    
    f = MP3id3v1(file)
    f.update(key,val)
    

def main(file):
    #除去ID3头，让mp3识别使用ID3v1
    f = MP3id3v2(file)
    f.delete()
    
    f = MP3id3v1(file)
    
    f.update('title',u'我的歌曲')
    f.update('album','ccc')
    f.update('comment','sdfsRR')
    f.update('artist','RRR')
    
    f.parse()
    print f.dictTag

if __name__ =='__main__':
    
    changeMp3Info(ur'F:\pyWorkSpace\notes\reFileName\mp3\138.mp3','title',u'bbbccc')
    
    #main(ur'F:\pyWorkSpace\notes\reFileName\mp3\138.mp3')
    #o = MP3id3v1(ur'F:\pyWorkSpace\notes\reFileName\mp3\101_old1.mp3')
    #print '\n'.join(['%s->%s' % (k,v) for k,v in o.dictTag.items()])
