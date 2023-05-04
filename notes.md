 # 一些日常笔记：
### 1、移动端测试要点
#### 移动端-CPU\GPU\内存、流量、电量、启动和切换响应时间、渲染帧率\刷新率Fps、数据缓存（修改、类似）压力/负载-特定区域流量、最大连接数/storage、反复大get请求、大文件下载、反复大post写入；响应时间、硬件限制（CPU\RAM\IO)、吞吐量TPS、打开数据库连接、第三方内容
    adb shell dumpsys connectivity // 查看连接情况
    adb shell dumpsys package com.yude.jieyao
    adb shell am start com.viide.repair/.MainActivity filter eafbc70
    adb shell am start  com.android.settings/com.android.settings.Settings
    adb pull /data/data/... C:\Users\EDY\Desktop
    adb shell pm list packages -3

### 2、docker笔记
#### 