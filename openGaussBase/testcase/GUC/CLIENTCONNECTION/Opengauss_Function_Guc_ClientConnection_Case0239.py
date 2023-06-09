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
Case Type   : GUC
Case Name   : 使用gs_guc set方法设置参数IntervalStyle值为a，检查预期结果
Description :
        1.查询IntervalStyle默认值
        2.修改参数值为a并重启数据库
        3.查询修改后的值
        4.使用numtodsinterval函数查询SELECT numtodsinterval(100, 'HOUR');
        5.恢复参数默认值
Expect      :
        1.显示默认值为postgres
        2.修改成功
        3.显示a
        5.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0239start---')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_intervalstyle(self):
        self.log.info('--步骤一：查询默认值--')
        sql_cmd = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              "IntervalStyle=postgres")
        self.log.info(sql_cmd)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show IntervalStyle;')
        self.log.info(sql_cmd)
        self.assertEqual('postgres', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤二：修改参数值为a并重启数据库--')
        msg = self.commonsh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "IntervalStyle = 'a'")
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤三：查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql(f'''show IntervalStyle;''')
        self.log.info(sql_cmd)
        self.assertEqual('a', sql_cmd.split('\n')[2].strip())
        self.log.info('--步骤四：使用numtodsinterval函数查询--')
        sql_cmd = self.commonsh.execut_db_sql('''select numtodsinterval
            (100, 'hour');
             ''')
        self.log.info(sql_cmd)

    def tearDown(self):
        self.log.info('--步骤五：恢复参数默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show IntervalStyle;')
        self.log.info(sql_cmd)
        if "postgres" != sql_cmd.split('\n')[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              "IntervalStyle=postgres")
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show IntervalStyle;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0239执行完成----')
