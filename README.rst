cid
==========

.. image:: https://img.shields.io/pypi/v/cid.svg
    :target: https://pypi.python.org/pypi/cid/

.. image:: https://img.shields.io/pypi/dm/cid.svg
    :target: https://pypi.python.org/pypi/cid/

Chinese Identity Parser

提取身份证号码中的生日、性别、办证区域, 校验身份证号码格式是否正确

Install
----------

::

    pip install cid


Usage
-----

::

    In [1]: from cid import IdParser

    In [2]: ip = IdParser()

    In [3]: ip.parse('360730198601011111')
    Out[3]:
    {'birthday': '1986-01-01',
     'gender': '男',
     'region': {'city': '赣州市', 'district': '宁都县', 'province': '江西省'}}

    # 校验身份证号码格式是否正确

    In [4]: ip.is_valid_cid('360730198601011111')
    Out[4]: False


    In [5]: ip.extract_gender('360730198601011111')
    Out[5]: '男'

    In [6]: ip.extract_birthday('360730198601011111')
    Out[6]: '1986-01-01'

    In [7]: ip.extract_region('360730198601011111')
    Out[7]: {'city': '赣州市', 'district': '宁都县', 'province': '江西省'}

    # 除了提取发证地，需要实例化 IdParser 外, 其他方法可直接使用

    In [8]: from cid import (is_valid_cid, extract_gender, extract_birthday)
