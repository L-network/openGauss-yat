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
'''
--  @testpoint:analyze分析索引表，使用无效参数，合理报错
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0104开始执行-----------------------------')

    def test_analyze(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200) );''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建索引并对索引表执行analyze加无效参数，合理报错
        sql_cmd2 = commonsh.execut_db_sql('''drop index if exists WR_RETURNED_DATE_SK_uni cascade;
        create unique index WR_RETURNED_DATE_SK_uni on customer_info(WR_RETURNED_DATE_SK);
        analyze VERIFY COMPLETED WR_RETURNED_DATE_SK_uni;
        analyze VERIFY fasty WR_RETURNED_DATE_SK_uni;''')
        self.assertIn(constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd2)
        self.assertIn('ERROR:  syntax error', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0104执行结束--------------------------')
