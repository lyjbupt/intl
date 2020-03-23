
from ftplib import FTP
import os,sys,string,datetime,time
import socket

class MYFTP:
    def __init__(self, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.port     = port
        self.ftp      = FTP()
        self.file_list = []
        # self.ftp.set_debuglevel(2)
    def __del__(self):
        self.ftp.close()
        # self.ftp.set_debuglevel(0)
    def login(self):
        ftp = self.ftp
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            ftp.connect(self.hostaddr, self.port)
            ftp.login(self.username, self.password)
            debug_print(ftp.getwelcome())
        except Exception:
            deal_error("Login failed")
        try:
            ftp.cwd(self.remotedir)
        except(Exception):
            deal_error('Change dir failed')

    def is_same_size(self, localfile, remotefile):
        try:
            remotefile_size = self.ftp.size(remotefile)
        except:
            remotefile_size = -1
        try:
            localfile_size = os.path.getsize(localfile)
        except:
            localfile_size = -1
        debug_print('lo:%d  re:%d' %(localfile_size, remotefile_size),)
        if remotefile_size == localfile_size:
            return 1
        else:
            return 0
    def download_file(self, localfile, remotefile):
        if self.is_same_size(localfile, remotefile):
            debug_print('%s file size same, no need download' %localfile)
            return
        else:
            debug_print('>>>>>>>>>>>>Downloading %s ... ...' %localfile)
        #return
        file_handler = open(localfile, 'wb')
        self.ftp.retrbinary('RETR %s'%(remotefile), file_handler.write)
        file_handler.close()

    def download_files(self, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            debug_print('Dir %s not exist, continue...' %remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        debug_print('Change dir %s' %self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list
        #print(remotenames)
        #return
        for item in remotenames:
            filetype = item[0]
            filename = item[1]
            local = os.path.join(localdir, filename)
            if filetype == 'd':
                self.download_files(local, filename)
            elif filetype == '-':
                self.download_file(local, filename)
        self.ftp.cwd('..')
        debug_print('Return to upper level %s' %self.ftp.pwd())

    def sync_files_filter(self, folder_filter, file_filter, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            debug_print('Dir %s not exist, continue...' %remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        debug_print('Change dir %s' %self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list
        #print(remotenames)
        #return
        for item in remotenames:
            filetype = item[0]
            filename = item[1]
            local = os.path.join(localdir, filename)
            if filetype == 'd' and pattern_good(filename, folder_filter):
                self.sync_files_filter(folder_filter, file_filter, local, filename)
            elif filetype == '-' and pattern_good(filename, file_filter):
                self.download_file(local, filename)
        self.ftp.cwd('..')
        debug_print('Return to upper level %s' %self.ftp.pwd())

    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        if self.is_same_size(localfile, remotefile):
            debug_print('Skip[same]: %s' %localfile)
            return
        file_handler = open(localfile, 'rb')
        self.ftp.storbinary('STOR %s' %remotefile, file_handler)
        file_handler.close()
        debug_print('Uploaded: %s' %localfile)

    def upload_files(self, localdir='./', remotedir = './'):
        if not os.path.isdir(localdir):
            return
        localnames = os.listdir(localdir)
        self.ftp.cwd(remotedir)
        for item in localnames:
            src = os.path.join(localdir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    debug_print('Folder %s exist' %item)
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)
        self.ftp.cwd('..')

    def get_file_list(self, line):
        ret_arr = []
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_filename(self, line):
        pos = line.rfind(':')
        while(line[pos] != ' '):
            pos += 1
        while(line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr

    def filter_file(self, remotepath, pattern):
        old_path = self.ftp.pwd()
        self.ftp.cwd(remotepath)
        dir_list = self.ftp.nlst()
        self.ftp.cwd(old_path)
        return [i for i in dir_list if '_' in i and i.split('_')[1].startswith(pattern) and ('release' in i.lower() or 'hotfix' in i.lower())]

def debug_print(s):
    print (s)

def deal_error(e):
    timenow  = time.localtime()
    datenow  = time.strftime('%Y-%m-%d', timenow)
    logstr = '%s Error happen: %s' %(datenow, e)
    debug_print(logstr)
    file.write(logstr)
    sys.exit()

def pattern_good(filename, pattern_list):
    for i in pattern_list:
        if filename.endswith(i):
            return True

if __name__ == '__main__':
    str_d = time.strftime("%y%m%d", time.localtime())
    #str_d = '200313'
    proj = ['00_NeusERD', '01_Neus_Q_volcano']
    folder_pattern = ['user','userdebug', 'chnopen']
    file_pattern = ['.7z','.img','.bin']
    bin_root = r'/home/shuang.gucas/FactoryImage'

    # FTP config
    hostaddr = '12.36.211.78' # Address
    username = 'sqe' #User
    password = 'sqe' #Pass
    port  =  21   # Port
    rootdir_remote = './'          # Remote dir
    f = MYFTP(hostaddr, username, password, rootdir_remote, port)
    f.login()

    for i in proj:
        local_store = os.path.join(bin_root, i)
        if not os.path.exists(local_store):
            os.makedirs(local_store, exist_ok=True)
        src_dirs = f.filter_file(i, str_d)
        for j in src_dirs:
            print("Downloading %s of project %s"%(j, i))
            old_path = f.ftp.pwd()
            rootdir_svr =  i + '/' + j
            f.sync_files_filter(folder_pattern, file_pattern, os.path.join(local_store, j), rootdir_svr)
            f.ftp.cwd(old_path)
