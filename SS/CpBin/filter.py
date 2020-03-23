import os
import re
import time
from ftplib import FTP

def ftp_connect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def filter_file(ftp, remotepath, pattern):
    old_path = ftp.pwd()
    ftp.cwd(remotepath)
    dir_list = ftp.nlst()
    ftp.cwd(old_path)
    return [i for i in dir_list if '_' in i and i.split('_')[1].startswith(pattern) and ('release' in i.lower() or 'hotfix' in i.lower())]

def download_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

def upload_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

if __name__ == "__main__":
    str_d = time.strftime("%y%m%d", time.localtime())
    #str_d = '200314'
    ftp = ftp_connect("12.36.211.78", "sqe", "sqe")
    proj = ['00_NeusERD', '01_Neus_Q_volcano']
    bin_root = r'F:\FactoryImage'
    print(str_d)

