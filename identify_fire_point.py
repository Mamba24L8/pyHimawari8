"""
purpos: 火点识别
reference: 《Himawari-8静止气象卫星草原火检测分析_陈洁》
           《利用 Himawari-8 数据监测森林火情初探_杜品》

"""
from netCDF4 import Dataset


# import numpy as np


def loadNcData(filePath):
    """ 加载数据"""
    return Dataset(filePath)


class IdentifyFirePoint:
    """
    Himawari-8火点提取，0.02°*0.02°分辨率, 6001*6001, 纬度lat[-60, 60], 经度lon[80, 200]
    Parameters
    ----------
    data: netCDF, data.variables.keys = ['latitude', 'longitude', 'band_id', 'start_time', 'end_time',
        'geometry_parameters', 'albedo_01', 'albedo_02', 'albedo_03', 'sd_albedo_03', 'albedo_04',
        'albedo_05', 'albedo_06', 'tbb_07', 'tbb_08','tbb_09', 'tbb_10', 'tbb_11', 'tbb_12', 'tbb_13',
        'tbb_14', 'tbb_15', 'tbb_16', 'SAZ', 'SAA', 'SOZ', 'SOA', 'Hour']
    bbox: list, [minlon, minlat, maxlon, maxlat]
        研究区域格网范围
    """

    def __init__(self, data, bbox):
        self.data = data
        self.box = bbox

    def getStudyAreaData(self):
        """
        获取研究区域数据, 后面计算需要， 要在bbox的范围扩大15个格点
        """
        pass

    def preIdentfyFirePoint(self, soz, b07, b14):
        """ 火点初步识别, 每个像元进行识别"""
        if soz > 90:
            # soz 太阳高度角
            c11, c12, c21, c22 = 0, 280, 0, 1
        else:
            c11, c12, c21, c22 = -0.3, 310.5, -0.0049, 1.75

        if b07 > c11 * soz + c12 and b07 - b14 > c21 * soz + c22:
            # b07: 07通道的亮温; b14: 14通道的亮温
            return True
        else:
            return False

    def identfySolarFlare(self):
        """ 识别太阳耀斑"""
        pass

    def identfyCloud(self):
        pass

    def identfyWater(self):
        """识别水体"""
        pass


if __name__ == '__main__':
    pass
