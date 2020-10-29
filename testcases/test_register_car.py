from pymysql.cursors import DictCursor

from middlerware.handler import Handler, MySqlHandlerWare, replace_data
from common.requset_handler import visit
import ddt
import unittest
import json
from common.mysql_handler import MysqlHandler

# 获取车辆信息
car_register_data = Handler.excel.read_sheet("车辆注册")

# 初始化logger
logger = Handler.logger


@ddt.ddt
class TestCarRegister(unittest.TestCase):
    @ddt.data(*car_register_data)
    def test_car_register(self, test_info):
        test_info["data"] = replace_data(Handler(), test_info["data"])
        resp = visit(method=test_info["method"],
                     url=Handler.host + test_info["url"],
                     json=json.loads(test_info["data"]))
        expected = json.loads(test_info["expected"])
        self.assertTrue(expected["code"] == resp["code"])
        self.assertTrue(expected["msg"] == resp["msg"])
        logger.info("第{}条测试用例通过".format(test_info["case_id"]))


if __name__ == '__main__':
    unittest.main()