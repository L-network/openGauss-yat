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
Case Type   : 功能测试
Case Name   : has_directory_privilege函数，将directory对象的所有权限赋予指定的角色
Description :
    1. 创建用户，赋予权限
    2. 在将directory对象的所有权限赋予用户前后进行查询
    3. 删除用户及路径
Expect      :
    1. 创建成功，赋权成功
    2. 在赋权后具有所有权限
    3. 删除成功
History     : 
"""

import unittest
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.pwd = macro.COMMON_PASSWD
        self.log.info('''---
        Opengauss_Function_Innerfunc_Has_Directory_Privilege_Case0002开始---''')

    def test_privilege(self):
        self.log.info('''----------------创建用户及目录------------------''')
        cmd0 = f'''drop user if exists hong;
           drop directory if exists dir;
           create user hong password '{self.pwd}';
           create or replace directory dir as '/tmp/';
            '''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE ROLE') > -1)
        self.assertTrue(msg0.find('CREATE DIRECTORY') > -1)

        self.log.info('''---在将directory对象的读写权限赋予用户前后进行查询---''')
        cmd1 = '''select has_directory_privilege('hong', 'dir','read');
            select has_directory_privilege('hong', 'dir','write');
            grant all privileges on directory  dir to hong;
            select has_directory_privilege('hong', 'dir','read');
            select has_directory_privilege('hong', 'dir','write');
            '''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.count('GRANT') == 1)
        res = msg1.splitlines()
        self.assertTrue(res[:8].count(' f') == 2)
        self.assertTrue(res[-9:].count(' t') == 2)

    def tearDown(self):
        cmd = f'''drop user if exists hong cascade;
                  drop directory if exists dir;'''
        self.commonsh.execut_db_sql(cmd)
        self.log.info('''---
        Opengauss_Function_Innerfunc_Has_Directory_Privilege_Case0002结束---''')
