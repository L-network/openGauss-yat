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
Case Type   : Separation_rights
Case Name   : 三权分立后管理员用户对表空间有所有权限
Description :
    1.初始用户执行：CREATE USER sysadmin01 WITH SYSADMIN password '$PASSWORD';
                CREATE USER wf WITH password '$PASSWORD';
    2.sysadmin01 用户执行：CREATE TABLESPACE tablespace01 RELATIVE LOCATION
    'tablespace/tablespace_3';
    GRANT CREATE ON TABLESPACE tablespace01 TO wf;
    SELECT PG_TABLESPACE_SIZE('tablespace01');
    ALTER TABLESPACE tablespace01 RENAME TO new_tablespace01;
    REVOKE CREATE ON TABLESPACE new_tablespace01 FROM wf;
    DROP TABLESPACE new_tablespace01;
Expect      :
    1.CREATE ROLE
    CREATE ROLE
    2.CREATE TABLESPACE
    查询到tablespace的相关信息
    ALTER TABLESPACE
    REVOKE
    DROP TABLESPACE
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_Security_Separation_Case0018 start----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('----------create user -----------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH}' \
                      f' -c "enableSeparationOfDuty=on";' \
                      f'gs_om -t stop && gs_om -t start'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = f'CREATE USER sysadmin01 WITH SYSADMIN password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'CREATE USER wf WITH password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        sql_cmd2 = 'CREATE TABLESPACE tablespace01 RELATIVE LOCATION ' \
                   '\'tablespace/tablespace_3\';' \
                   'GRANT CREATE ON TABLESPACE tablespace01 TO wf;' \
                   'SELECT PG_TABLESPACE_SIZE(\'tablespace01\');' \
                   'ALTER TABLESPACE tablespace01 RENAME TO ' \
                   'new_tablespace01;' \
                   'REVOKE CREATE ON TABLESPACE new_tablespace01 FROM wf;' \
                   'DROP TABLESPACE new_tablespace01;'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U sysadmin01 -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.TABLESPCE_CREATE_SUCCESS, msg2)
        self.assertTrue(msg2.find('GRANT') > -1)
        self.assertTrue(msg2.find('pg_tablespace_size') > -1)
        self.assertIn(self.Constant.TABLESPCE_ALTER_SUCCESS, msg2)
        self.assertTrue(msg2.find('REVOKE') > -1)
        self.assertIn(self.Constant.TABLESPCE_DROP_SUCCESS, msg2)

    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH}' \
                      f' -c "enableSeparationOfDuty=off";' \
                      f'gs_om -t stop && gs_om -t start'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = f'drop user if exists wf CASCADE;' \
                   f'DROP USER IF EXISTS sysadmin01 CASCADE;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Separation_Case0018 finish----')
