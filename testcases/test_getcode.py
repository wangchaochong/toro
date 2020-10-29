import unittest
from time import sleep

import ddt
import json
from middlerware.handler import Handler
from common.requset_handler import visit


logger = Handler.logger

getcode_data = Handler.excel.read_sheet("发送验证码")


@ddt.ddt
class TestGetcode(unittest.TestCase):

    @ddt.data(*getcode_data)
    def test_getcode(self, test_info):
        url = Handler.host + test_info["url"]

        resp = visit(method=test_info["method"],
                     url=url,
                     json=json.loads(test_info["data"]))

        try:
            expected = json.loads(test_info["expected"])
            self.assertTrue(expected["code"] == resp["code"])
            self.assertTrue(expected["msg"] == resp["msg"])

            logger.info("第{}条测试用例通过".format(test_info["case_id"]))

        except Exception as e:
            # logger.error("请求不是json格式")
            raise e


if __name__ == '__main__':
    unittest.main()
