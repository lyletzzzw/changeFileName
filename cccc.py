#! /usr/bin/env python
#coding=utf-8

arr=[]
try:
    f = open(ur'E:\tmp\test\1.txt')
    arr=f.readlines()
except IOError as err:
    print('file error->'+str(err))
finally:
    if f in locals():
        f.close()
print arr
out_file=open(ur'E:\tmp\test\2.txt','w')
print(arr,file=out_file)
