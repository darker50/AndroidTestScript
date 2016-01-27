#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

#截取设备上的屏幕，保存至当前目录下的screenshot目录

basePath = lambda p: os.path.abspath(p)
deviceList = []
deviceKeyValue = "device\n"
deviceSerial = ''
deviceName = ''
deviceMap = {}
path = basePath(os.getcwd() + "/screenshot")
timeStamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

#封闭基本的命令行代码
screenshotCMD = "adb -s %s shell screencap -p /data/local/tmp/tmp.png"
screenshotPATH = "adb -s %s pull /data/local/tmp/tmp.png "  + basePath(path + "/" + timeStamp + ".png")
screenshotRemove = "adb -s %s shell rm /data/local/tmp/tmp.png"
getDeviceModel = "adb -s %s shell getprop ro.product.model"
getDeviceManufacturer = "adb -s %s shell getprop ro.product.manufacturer"
# 使用字典的方式存放设备的序列号
# 只有一个设备，直接返回单个序列号
# 多个设备，输入对应数字后返回对应设备的序列号
def get_device():
    get_devices_list()
    if(len(deviceList)>1):
        i = 0
        #设备号存入字典中
        while(i< len(deviceList)):
            deviceMap[i] = deviceList[i]
            deviceName = get_device_name(deviceList[i])
            print  u"输入数字“"+str(i)+u"”给"+deviceName+ u"截图"
            i = i+1
        _status = True;
        while _status:
            try:
                a = input()
                return deviceMap[a]
            except:
                print u"输入的数字不存在设备号"
    else:
        return deviceList[0]

# 截图代码
def screenshot():
    deviceSerial = get_device()
    os.popen("adb wait-for-device")
    os.popen(screenshotCMD %deviceSerial)
    if not os.path.isdir(basePath(os.getcwd() + "/screenshot")):
        os.makedirs(path)
    os.popen(screenshotPATH %deviceSerial)
    os.popen(screenshotRemove %deviceSerial)
    print "success"

# 使用adb devices 获取设备列表，并把设备序列号存在数组返回
def get_devices_list():
    _deviceOut = os.popen("adb devices").readlines()
    for line in _deviceOut:
        a = line.split("\t")[0]
        if(deviceKeyValue in line.split("\t")):
            deviceList.append(line.split("\t")[0])
    return deviceList

# 获取手机设备的名字
def get_device_name(serial):
    try:
        _deviceModel = os.popen(getDeviceModel %serial).read().strip()
        _deviceManufacturer = os.popen(getDeviceManufacturer %serial).read().strip()
        _deviceName = _deviceManufacturer + " "+ _deviceModel
        return _deviceName
    except:
        print u"获取不到设备的名称"

    return _deviceName

if __name__ == "__main__":
    screenshot()
