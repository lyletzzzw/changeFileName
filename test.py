#! /usr/bin/env python
#coding=utf-8

writeMp3Header = {
        "SongName":"aaa",
        "SongPeople":"bbb",
        "ZhuanJi":"cccc",
        "Year":"1",
        "Bak":"222"
        }



def setMp3Header(mp3file):
    mp3Id3V1 = {       
        "SongName":-125,
        "SongPeople":-95,
        "ZhuanJi":-65,
        "Year":-35,
        "Bak":-31
        }
    tags = ['SongName','SongPeople','ZhuanJi','Bak']
    f = open(mp3file,'r+')
    try:
        f.seek(-128,2)
        try:
            tempstr = f.read(3)
            if tempstr == 'TAG':
                for tag,startPos in mp3Id3V1.items():
                    if writeMp3Header[tag] != '':
                        f.seek(startPos,2)
                        if tag in tags:
                            if len(writeMp3Header[tag]) > 30:
                                f.write(writeMp3Header[tag][:30])
                            else:
                                f.write(writeMp3Header[tag])
                            print startPos,tag,writeMp3Header[tag]
            else:
                print 'is not a mp3file'
        except IOError:
            print 'read error'
    finally:
        f.close()


if __name__=='__main__':
    writeMp3Header['SongName'] = ur'测试歌曲名称'
    writeMp3Header['SongPeople'] = ur'不得闲'
    writeMp3Header['ZhuanJi'] = ur'专辑'
    writeMp3Header['Year'] = ur'2009'
    writeMp3Header['Bak'] = ur'备注测试'
    setMp3Header(r'F:\pyWorkSpace\notes\reFileName\mp3\2.mp3')
    