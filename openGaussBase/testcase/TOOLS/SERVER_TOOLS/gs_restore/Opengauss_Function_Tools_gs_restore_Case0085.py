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
Case Type   : 服务端工具
Case Name   : 导入时参数-a和-e的使用
Description :
    1.创建数据库
    1.创建数据
    3.导出tar格式文件
    4.导入之前导出的数据
    5.查看数据是否导入
    6.清理环境
Expect      :
    1.创建数据库成功
    1.创建数据成功
    3.导出tar格式文件成功
    4.导入之前导出的数据成功
    5.查看成功，数据已导入
    6.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_server_tools1(self):
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0085开始执行--")
        self.log.info("---------------步骤1.创建数据库--------------")
        sql_cmd = self.commonsh.execut_db_sql(f'''create database test;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)

        self.log.info("---------------步骤2.创建数据--------------")
        sql_cmd = f"create table test1 (id int,name char(20));" \
            f"insert into test1 values(1,'xixi'),(2,'haha'),(3,'hehe');" \
            f"create table test2 (id  int,name char(20));" \
            f"insert into test2 values(12,'xixi'),(22,'haha'),(33,'hehe');" \
            f"create table test3(id  int,name char(20));" \
            f"insert into test3 values(123,'xiyxi'),(212,'hayha')," \
            f"(313,'heyhe');create table test4(id  int,name char(20));" \
            f"insert into test4 values(33,'xiao'),(296,'bai'),(783,'cai');" \
            f"create table test5(id  int,name char(20));" \
            f"insert into test5 values(7,'yang'),(29886,'bai'),(9,'lao');" \
            f"  select * from test5;"
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gsql -d test -p {self.dbuser_node.db_port} -c \"{sql_cmd}\""
        self.log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)
        self.assertIn('3 rows', msg)

        self.log.info("--------------步骤3.导出sql格式文件-----------------")
        dump_cmd = f"source {macro.DB_ENV_PATH} ; " \
            f"gs_dump -p {self.dbuser_node.db_port}  " \
            f"test -f " \
            f"{macro.DB_INSTANCE_PATH}/test.sql -F c"
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg)

        self.log.info("------------步骤4.导入之前导出的数据----------------")
        restore_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_restore -p {self.dbuser_node.db_port} " \
            f"-d test  {macro.DB_INSTANCE_PATH}/test.sql -a -e;"
        self.log.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        self.log.info(restore_msg)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG, restore_msg)

        self.log.info("----------步骤5.查看数据是否导入----------------")
        sql_cmd = f"select * from test5"
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gsql -d test -p {self.dbuser_node.db_port} -c \"{sql_cmd}\""
        self.log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('6 rows', msg)

    def tearDown(self):
        self.log.info("------------------步骤6.清理环境------------------")
        clean_cmd = self.commonsh.execut_db_sql(f'''drop database test ;''')
        self.log.info(clean_cmd)
        rm_cmd = f"rm -rf {macro.DB_INSTANCE_PATH}/test.sql"
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0085执行结束-")
