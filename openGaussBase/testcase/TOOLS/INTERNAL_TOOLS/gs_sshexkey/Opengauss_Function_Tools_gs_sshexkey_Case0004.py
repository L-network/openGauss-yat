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
Case Type   : 系统内部使用工具 gs_sshexkey
Case Name   : 普通用户下，执行gs_sshexkey --version 命令
Description :
    1、普通用户下，执行gs_sshexkey --version
    2、检查选项和用法
Expect      :
    1、命令执行成功
    2、版本信息描述正确
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_gs_sshexkey(self):
        logger.info("===Opengauss_Function_Tools_gs_sshexkey_Case0004开始执行===")
        logger.info("======普通用户下执行gs_sshexkey --version命令======")
        gs_cmd = f'''source {macro.DB_ENV_PATH}
            gs_sshexkey --version
            '''
        logger.info(gs_cmd)
        gs_res = self.user_node.sh(gs_cmd).result()
        logger.info(gs_res)

        logger.info("======提取结果，检查版本信息描述======")
        self.assertIn('openGauss', gs_res)

    def tearDown(self):
        logger.info("======No Need Clean && No Need Recovery======")
        logger.info("===Opengauss_Function_Tools_gs_sshexkey_Case0004执行结束===")
