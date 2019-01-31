import ftplib
import time
import os

from retry import retry


# from ftplib import FTP


class DownloadHimawari8:

    def __init__(self):
        self.address = 'ftp.ptree.jaxa.jp'
        self.uid = 'wanglei_cdsihan.com'
        self.pw = 'SP+wari8'

    def connectServer(self, address=None, uid=None, pw=None):
        if address is None:
            address, uid, pw = self.address, self.uid, self.pw
        try:
            ftp = ftplib.FTP(address)
            ftp.login(uid, pw)
            return ftp
        except ftplib.all_errors as e:
            print('FTP error:', e)

    @staticmethod
    def generateFileName(targetFile, date, hour, minute, level='L2'):
        """ 生成服务器文件名
        targetFile:
                'WLF': 'wildfire', {'L2': 10分钟分辨率；'L3':1小时和1天的分辨率}
                'grid': netcdf文件，每次下载两个文件，根据波段的分辨率的2个文件
                'hsd': Himawari标准数据，没有经过转换的原始数据，二进制文件
        date: 日期，'2019-01-01'
        hour: 小时， '01、02...24'
        mimute: 分钟， '00、10、20...50'
        level: 级别，{'L2'、'L3'}
        """
        year, month, day = date.split('-')
        if targetFile == 'WLF':
            remoteDir = ''.join(['/pub/himawari/', level, '/WLF/bet/', year + month, '/', day, '/'])
            remoteFileName = ''.join(
                ['H08_', year, month, day, '_', hour, minute, '_', level, 'WLFbet_FLDK.06001_06001.csv'])
            return os.path.join(remoteDir, remoteFileName)

        elif targetFile == 'grid':
            remoteDir = ''.join(['/jma/netcdf/', year + month + '/', day])
            remoteFileName1 = ''.join(['NC_H08_', year, month, day, '_', hour, minute, '_R21_FLDK.02401_02401.nc'])
            remoteFileName2 = ''.join(['NC_H08_', year, month, day, '_', hour, minute, '_R21_FLDK.06001_06001.nc'])
            return os.path.join(remoteDir, remoteFileName1), os.path.join(remoteDir, remoteFileName2)

    @retry([ConnectionAbortedError, TimeoutError], tries=3, delay=2, jitter=1)
    def downloadFile(self, remoteFile, localFile):
        ftp = self.connectServer()
        try:
            with open(localFile, "wb") as f:
                ftp.retrbinary("RETR {0}".format(remoteFile), f.write)
            return True
        except ConnectionAbortedError as e:
            pass
        except TimeoutError as e:
            time.sleep(3)
        except:
            raise ValueError("Failed to download data!")

    def downloadFolder(self, remoteFiler, localFiler):
        pass

    @staticmethod
    def closeServer(ftp):
        ftp.close()

    @staticmethod
    def quitServer(ftp):
        ftp.quit()


if __name__ == '__main__':

    from time import time
    _address = 'ftp.ptree.jaxa.jp'
    _uid = 'wanglei_cdsihan.com'
    _pw = 'SP+wari8'
    _localFile1 = 'F:/work/wildfire_doc/data/NC_H08_20190129_0720_R21_FLDK.02401_02401.nc'
    _remoteFile1 = '/jma/netcdf/201901/29/NC_H08_20190129_0720_R21_FLDK.02401_02401.nc'

    _localFile2 = 'F:/work/wildfire_doc/data/NC_H08_20190129_0720_R21_FLDK.06001_06001.nc'
    _remoteFile2 = '/jma/netcdf/201901/29/NC_H08_20190129_0720_R21_FLDK.06001_06001.nc'
    try:
        _ftp = ftplib.FTP(_address)
        _ftp.login(_uid, _pw)
        print('OK')
        print(_ftp.getwelcome())
        print(_ftp.dir())
        t1 = time()
        #with open(_localFile1, "wb") as f:
            #_ftp.retrbinary("RETR {0}".format(_remoteFile1), f.write)

        with open(_localFile2, "wb") as f:
            _ftp.retrbinary("RETR {0}".format(_remoteFile2), f.write)
        print('时间：',time() - t1)
        print('download successful')
    except:
        print('wrong')

