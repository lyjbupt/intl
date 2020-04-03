set db_path=%1

fastboot flash gpt %db_path%\gpt.bin
sleep -m 100
fastboot flash fwbl1 %db_path%\9630.sbl1.bin
sleep -m 100
fastboot flash epbl %db_path%\epbl.bin
sleep -m 100
fastboot flash bl2 %db_path%\ERD9630_bl2.bin
sleep -m 100
fastboot flash bootloader %db_path%\lk.bin
sleep -m 100
fastboot flash el3_mon %db_path%\el3_mon.bin
sleep -m 100
fastboot flash ldfw %db_path%\ldfw.bin
sleep -m 100
fastboot flash keystorage %db_path%\keystorage_exynos9630.bin
sleep -m 100
fastboot flash logo %db_path%\logo_1080_2220.bin
sleep -m 100
fastboot flash tzsw %db_path%\tzsw.img
sleep -m 100
fastboot flash vbmeta %db_path%\vbmeta.img
sleep -m 100
fastboot flash boot %db_path%\boot.img
sleep -m 100
fastboot flash recovery %db_path%\recovery.img
sleep -m 100
fastboot flash dtbo %db_path%\dtbo.img
sleep -m 100
fastboot flash dpm %db_path%\dpm.img
sleep -m 100
fastboot flash system %db_path%\system.img -S 512M
sleep -m 600
fastboot flash vendor %db_path%\vendor.img -S 128M
sleep -m 600
fastboot format persist
sleep -m 100
fastboot erase modem
sleep -m 100
fastboot flash modem %db_path%\modem.bin
sleep -m 100
fastboot -w reboot
sleep -m 200
rem sleep 60
