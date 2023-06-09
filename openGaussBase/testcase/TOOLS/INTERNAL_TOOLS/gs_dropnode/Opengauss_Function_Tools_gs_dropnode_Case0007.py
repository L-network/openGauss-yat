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
Case Type   : gs_dropnode
Case Name   : 3参，1主1备（出现输入提示后不输入） 期望:30min后输入yes减容操作成功。集群情况正常
Description :
        1.1主2备，执行减容 提示出现30min后输入yes
        2.恢复环境
Expect      :
        1.期望:操作成功，减容成功
        2.恢复环境
History     :
        修改单机环境不执行为非1+2环境不执行
"""
import unittest
import os

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 >= COMMONSH.get_node_num(), '单机环境不执行')
class Gstoolstestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info(f'-----{os.path.basename(__file__)} start-----')
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.pri_root_node = Node("PrimaryRoot")
        self.user_node = Node("PrimaryDbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.com_root = CommonSH("PrimaryRoot")
        self.s_com1 = CommonSH("Standby1DbUser")
        self.s_com2 = CommonSH("Standby2DbUser")
        self.com = Common()
        self.standby_ip_list = [self.s_node1.ssh_host, self.s_node2.ssh_host]
        self.ssh_file = '~/.ssh'

        num = COMMONSH.get_node_num()
        self.assertGreaterEqual(num, 3, "执行失败:节点数量异常，减容不执行")

        LOGGER.info("查询synchronous_standby_names默认值")
        result = COMMONSH.execut_db_sql("show synchronous_standby_names")
        LOGGER.info(f"primary synchronous_standby_names is {result}")
        self.synchronous_standby_names_p = result.strip().splitlines()[-2]
        result = self.s_com1.execut_db_sql("show synchronous_standby_names")
        LOGGER.info(f"s1 synchronous_standby_names is {result}")
        self.synchronous_standby_names_s1 = result.strip().splitlines()[-2]
        result = self.s_com2.execut_db_sql("show synchronous_standby_names")
        LOGGER.info(f"s2 synchronous_standby_names is {result}")
        self.synchronous_standby_names_s2 = result.strip().splitlines()[-2]
        self.host_tuple = (self.pri_root_node.ssh_host,
                           self.s_node1.ssh_host,
                           self.s_node2.ssh_host)
        self.params = {'-f': 'test_hosts'}

    def test_tool(self):
        LOGGER.info("步骤1：1主2备，执行减容 30min后根据减容和重启提示输入yes")
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("2", result.split("\n")[-2].strip())
        execute_cmd = f'''source {macro.DB_ENV_PATH};
                    expect <<EOF
                    set timeout 120
                    spawn gs_dropnode -U {self.user_node.ssh_user} \
                    -G {self.user_node.ssh_user} \
                    -h {self.s_node2.ssh_host}
                    sleep 1800
                    expect "*drop the target node (yes/no)?*" 
                    send "yes\\n" 
                    expect eof\n''' + '''EOF'''
        LOGGER.info(execute_cmd)
        result = self.user_node.sh(execute_cmd).result()
        LOGGER.info(result)
        self.assertIn("Success to drop the target nodes", result)

        LOGGER.info("核对减容成功 剩余1+1")
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        self.assertEqual("1", result.split("\n")[-2].strip())
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("步骤2:恢复环境 若用例失败 则检查节点 节点不为3时执行扩容")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        result = COMMONSH.execut_db_sql(
            "select count(*) from pg_stat_get_wal_senders();")
        LOGGER.info(result)
        if "2" != result.split("\n")[-2].strip():
            LOGGER.info("-----创建root互信-----")
            result = self.com.get_sh_result(self.pri_root_node,
                                            f"ls {macro.DB_SCRIPT_PATH}")
            if "gs_sshexkey" not in result:
                cmd = f"cd {macro.DB_SCRIPT_PATH}/../; " \
                      f"tar -zxvf openGauss-Package-bak*.tar.gz > /dev/null"
                result = self.pri_root_node.sh(cmd).result()
                LOGGER.info(result)
                result = self.com.get_sh_result(self.pri_root_node,
                                                f"ls {macro.DB_SCRIPT_PATH}")
                LOGGER.info(result)
                if "gs_sshexkey" not in result:
                    raise Exception("cat not find gs_sshexkey, Please check!")
            self.com_root.exec_gs_sshexkey(macro.DB_SCRIPT_PATH,
                                           *self.host_tuple,
                                           **self.params)
            result = self.com_root.exec_expension(f"{self.user_node.ssh_user}",
                                                  f"{self.user_node.ssh_user}",
                                                  f"{self.s_node2.ssh_host}",
                                                  f"{macro.DB_XML_PATH}")
            LOGGER.info(result)
            self.assertTrue(result)

        LOGGER.info("恢复各节点synchronous_standby_names")
        COMMONSH.execute_gsguc("reload",
                               self.constant.GSGUC_SUCCESS_MSG,
                               f"synchronous_standby_names="
                               f"'{self.synchronous_standby_names_p}'",
                               single=True)
        self.s_com1.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"synchronous_standby_names="
                                  f"'{self.synchronous_standby_names_s1}'",
                                  single=True)
        self.s_com2.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"synchronous_standby_names="
                                  f"'{self.synchronous_standby_names_s2}'",
                                  single=True)

        self.assertTrue("Normal" in status or "Degraded" in status)

        LOGGER.info("-----清理集群节点root互信-----")
        for i in self.standby_ip_list:
            LOGGER.info(f"-----清理备{i}节点互信文件-----")
            rm_cmd1 = f'''ssh {i} <<EOF rm -rf {self.ssh_file}/*\n''' + "EOF"
            LOGGER.info(rm_cmd1)
            rm_res1 = self.pri_root_node.sh(rm_cmd1).result()
            LOGGER.info(rm_res1)

        LOGGER.info(f"-----清理主节点互信文件-----")
        rm_cmd2 = f'''rm -rf {self.ssh_file}/*;ls {self.ssh_file}'''
        LOGGER.info(rm_cmd2)
        rm_res2 = self.pri_root_node.sh(rm_cmd2).result()
        LOGGER.info(rm_res2)
        self.assertEqual('', rm_res2, '清理互信文件失败')
        LOGGER.info(f'-----{os.path.basename(__file__)} end-----')

