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
Case Type   : 统计信息函数
Case Name   : DBE_PERF.get_summary_user_login()描述：统计openGauss各节点用户
    登入登出次数信息，查询该函数必须具有sysadmin权限。
Description :
    1.统计openGauss各节点用户登入登出次数信息，以系统用户执行
    1.统计openGauss各节点用户登入登出次数信息，以非系统用户执行
Expect      :
    1.统计openGauss各节点用户登入登出次数信息，以系统用户执行
    1.统计openGauss各节点用户登入登出次数信息，以非系统用户执行，合理报错
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0015开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.统计openGauss各节点用户登入登出次数信息，以系统用户执行-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select DBE_PERF.get_summary_user_login();')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            str_info = sql_cmd.split('\n')[-2]
            self.log.info(f'str_info = {str_info}')
            num = len(str_info.split(','))
            self.log.info(f'num = {num}')
            if num == 5:
                self.log.info('统计openGauss各节点用户登入登出次数信息成功')
            else:
                raise Exception('函数执行异常，请检查')
        else:
            raise Exception('执行结果异常，请检查')

        self.log.info("-----步骤2.统计openGauss各节点用户登入登出次数信息，以非系统用户执行-----")
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d ' \
            f'{self.dbuser.db_name} -U ' \
            f'{self.dbuser.db_user} -W {self.dbuser.db_password}' \
            f' -c "select DBE_PERF.get_summary_user_login();" '
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR:  permission denied for schema dbe_perf', msg)

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0015结束')
