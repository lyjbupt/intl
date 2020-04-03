@echo off


::1
echo start PowerMonitor output
F:\git-prj\powercontrol-4-autodown_flash\powercontrol-4-autodown_flash\powercontrol-4-autodown_flash\bin\Debug\powercontrol-4-autodown_flash.exe ConfigFileF:\\develop_res\\SqePowerVerify4DB\\caseConfig.xml
F:\git-prj\powercontrol-4-autodown_flash\powercontrol-4-autodown_flash\powercontrol-4-autodown_flash\bin\Debug\powercontrol-4-autodown_flash.exe ResultFileF:\\develop_res\\SqePowerVerify4DB\\output\\result.xls
F:\git-prj\powercontrol-4-autodown_flash\powercontrol-4-autodown_flash\powercontrol-4-autodown_flash\bin\Debug\powercontrol-4-autodown_flash.exe startpowermonitor
echo end PowerMonitor output

sleep 1
::-------------------------------only for debuging-------------------------------
::goto endingfordebug



::2
echo start getDBpath ......
call E:\workspace\AutoDownloadFlash\test\getDBpath.bat
echo ------
set /p line=<dbPath_tmp.txt
set dbPath=/home/shuang.gucas/FactoryImage/%line%
echo %line%
echo %dbPath%
echo end getDBpath

sleep 1
::-------------------------------only for debuging-------------------------------
::goto endingfordebug



echo start ftp download ......
rem sleep 5
call E:\workspace\AutoDownloadFlash\toolset\script\ftpdownload.bat %dbPath% E:\workspace\AutoDownloadFlash\test\image_neus\%line%
echo end ftp download ......

sleep 1
::-------------------------------only for debuging-------------------------------
::goto endingfordebug



echo start enter fastboot ......
rem sleep 5
rem E:\workspace\AutoDownloadFlash\toolset\script\plc_controller.bat fastboot
call E:\workspace\AutoDownloadFlash\toolset\ext-exe\plc-exe\Modbus_Test.exe COM3 0 0x10 1
call E:\workspace\AutoDownloadFlash\toolset\ext-exe\plc-exe\Modbus_Test.exe COM3 1 0x17 9000
call E:\workspace\AutoDownloadFlash\toolset\ext-exe\plc-exe\Modbus_Test.exe COM3 0 0x10 0
echo end enter fastboot ......

sleep 1
::-------------------------------only for debuging-------------------------------
::goto endingfordebug



echo start flash image ......
E:\workspace\AutoDownloadFlash\mptool\flashall.bat E:\workspace\AutoDownloadFlash\test\image_neus\full_erd9630-userdebug-201911051135
echo end flash image ......

:endingfordebug
echo endingfordebug directory
pause
