# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path
import logging
import csv
from six import next

log = logging.getLogger(__name__)


def is_valid_cid(cid):
    """ 验证身份证号码格式是否有效
    原来的是 15 位，构成如下：
    1. 1-6 位：地址码。采用的是行政区划代码，可以去统计局的网站查。
    2. 7-12 位：生日期码。构成为 `yymmdd`。
    3. 13-15 位：顺序码。每个地区出生人口按顺序递增，最后一位奇数分给男的，
       偶数分给女的，也就是说 15 的没有校验码

    18 位则有 2 点改动：
    1.生日期码变为 8 位，构成为 `yyyymmdd`。
    2.增加校验码，即第 18 位。按照 ISO 7064:1983.MOD 11-2 校验码计算。

    计算方法很无聊：
    1. 将身份证号码的前17位数分别乘以不同的系数。从第一位到第十七位的系数
       分别为：`7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2`
    2. 将这 17 位数字和系数相乘的结果相加。
    3. 用加出来和除以 11 ，得到余数。
    4. 余数的结果只可能为 `0 1 2 3 4 5 6 7 8 9 10` 这11种，
       分别对应的最后一位身份证的号码为 `1 0 X 9 8 7 6 5 4 3 2`。

    .. code-block:: python

        In [1]: from cid import is_valid_cid
        In [2]: is_valid_cid('360730198601011111')
        In [2]: False

    :param cid: a string type chinese identity.
    :returns: Boolean indicating whether the cid valid or not.
    """
    if len(cid) < 18:
        log.warning("old version id have not check_code")
        return True
    salt = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code = '10X98765432'
    idx = sum(map(lambda x: int(x[0]) * x[1], zip(cid[:17], salt))) % 11
    return check_code[idx] == cid[17]


def extract_gender(cid):
    """extract gender from cid

    .. code-block:: python

        In [1]: from cid import extract_gender
        In [2]: extract_gender('360730198601011111')
        In [2]: '男'

    :param cid: a string type chinese identity.
    :returns: '男' or '女'.
    """
    g_code = cid[16] if len(cid) == 18 else cid[14]
    return '男' if int(g_code) % 2 else '女'


def extract_birthday(cid):
    """extract gender from birthday

    .. code-block:: python

        In [1]: from cid import extract_birthday
        In [2]: extract_birthday('360730198601011111')
        In [2]: '1986-01-01'

    :param cid: a string type chinese identity.
    :returns: a string type date representing by `%Y-%m-%d`, like '1986-01-01'.
    """
    return '{}-{}-{}'.format(
        cid[6:10], cid[10:12], cid[12:14]) if len(cid) == 18 \
        else '19{}-{}-{}'.format(cid['6:8'], cid[8:10], cid[10:12])


class IdParserError(Exception):
    pass


class IdParser(object):

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'data.csv')

    def __init__(self, data_path=data_path):
        """ initialize region mapping
        """
        reader = csv.reader(open(data_path))
        keys = next(reader)
        self.info_dict = {
            values[0]: dict(zip(keys, values)) for values in reader}

    extract_gender = staticmethod(extract_gender)
    extract_birthday = staticmethod(extract_birthday)
    is_valid_cid = staticmethod(is_valid_cid)

    def extract_region(self, cid):
        """extract gender from birthday

        .. code-block:: python

            In [1]: from cid import IdParser
            In [2]: ip = IdParser()
            In [3]: ip.extract_region('360730198601011111')
            Out[3]: {'city': '赣州市', 'district': '宁都县',
                     'province': '江西省'}

        :param cid: a string type chinese identity.
        :returns: a dict of region data (province,
            city and district).
        """
        try:
            d = self.info_dict[cid[:6]].copy()
        except KeyError:
            raise IdParserError('ID Error')
        d.pop('id')
        return d

    def parse(self, cid):
        """parse cid, extract gender, birthday and regions

        .. code-block:: python

            In [1]: from cid import IdParser
            In [2]: ip = IdParser()
            In [3]: ip.parse('360730198601011111')
            Out[3]:
            {'birthday': '1986-01-01',
             'gender': '男',
             'region': {'city': '赣州市', 'district': '宁都县',
                        'province': '江西省'}}

        :param cid: a string type chinese identity.
        :returns: a dict of gender, birthday and regions data
        """
        return {'gender': self.extract_gender(cid),
                'birthday': self.extract_birthday(cid),
                'region': self.extract_region(cid)}
