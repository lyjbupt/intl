@echo off
set image=%1
set local_path=%2
rem set image=chnopen-userdebug-Electric_current
rem set local_path=neus
rem 指定FTP用户名
set ftpUser=ftp.50
rem 指定FTP密码
set ftpPass=ftp.50
rem 指定FTP服务器地址
set ftpIp=109.105.10.50
rem 指定待下载的文件位于FTP服务器的哪个目录
rem set ftpFolder=/home/shuang.gucas/temp/%image%
set ftpFolder=%image%
rem 指定从FTP下载下来的文件存放到本机哪个目录
rem set LocalFolder=F:\DailyBuild\neus\%local_path%\image
set LocalFolder=%local_path%

if exist %LocalFolder% (
rd /s/q %LocalFolder%
)
md %LocalFolder%

set OriFolder=%cd%

set d=%date:~0,10%
set t=%time:~0,8%
echo start ftp: %d% %t%

cd /d %LocalFolder%
echo open %ftpIp% > ftp.txt
echo user %ftpUser% %ftpPass% >> ftp.txt
echo cd %ftpFolder% >> ftp.txt
rem 更改本地计算机上的工作目录
echo lcd %LocalFolder% >>ftp.txt  
echo prompt off >>ftp.txt
rem 使用二进制文件传输方式
echo bin >> ftp.txt
rem 要下载的文件
echo mget * >> ftp.txt
echo bye >> ftp.txt
ftp -n -s:ftp.txt
del ftp.txt
rem  pause

set d=%date:~0,10%
set t=%time:~0,8%
echo end ftp: %d% %t%
cd /d %OriFolder%
@echo on