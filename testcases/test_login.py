import json
import unittest
import ddt
from common.requset_handler import visit
from middlerware.handler import Handler

# 初始化logger
logger = Handler.logger

# 读取登录Excel表格
login_data = Handler.excel.read_sheet("登录")
logger.info("已读取表格文件")


@ddt.ddt
class TestLogin(unittest.TestCase):
    @ddt.data(*login_data)
    def test_login(self, test_info):
        expected = json.loads(test_info["expected"])
        url = Handler().host + test_info["url"]
        resp = visit(test_info["method"],
                     url=url,
                     json=json.loads(test_info["data"]),
                     )
        try:
            self.assertEqual(expected["code"], resp["code"])
            self.assertEqual(expected["msg"], resp["msg"])
            Handler.excel.write("登录", test_info["case_id"] + 1, 9, "通过")
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))
        except Exception as e:
            # logger.info("第{}条测试用例失败".format(test_info["case_id"]))
            print(f"返回的不是json格式：{e}")
            Handler.excel.write("登录", test_info["case_id"] + 1, 9, "失败")
            raise e


if __name__ == '__main__':
    unittest.main()


