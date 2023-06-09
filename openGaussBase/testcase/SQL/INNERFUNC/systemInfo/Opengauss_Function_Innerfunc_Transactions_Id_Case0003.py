"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : 系统信息函数
Case Name   : 函数skeys(hstore) ，返回hstore的所有键构成的集合
Description :
    1.函数skeys(hstore) ，返回hstore的所有键构成的集合
Expect      :
    2.返回hstore的所有键构成的集合成功
History     : 
"""

import unittest
import time
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_Transactions_Id'
                      '_Case0003开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        self.log.info(f'-步骤1.函数skeys(hstore) ，返回hstore的所有键构成的集合-')
        sql_cmd = self.commonsh.execut_db_sql(f'select skeys(\'a=>1,b=>2\');')
        self.log.info(sql_cmd)
        self.assertIn('a', sql_cmd)
        self.assertIn('b', sql_cmd)

    def tearDown(self):
        self.log.info('-------无需清理环境-------')
        self.log.info('-Opengauss_Function_Innerfunc_Transactions_Id'
                      '_Case0003结束-')
