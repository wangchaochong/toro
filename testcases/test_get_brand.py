from middlerware.handler import Handlerfrom common.requset_handler import visitimport ddtimport unittestimport jsonfrom jsonpath import jsonpath# 获取品牌get_brand_data = Handler.excel.read_sheet("获取品牌")# 初始化loggerlogger = Handler.logger@ddt.ddtclass TestGetBrand(unittest.TestCase):    @ddt.data(*get_brand_data)    def test_get_brand(self, test_info):        resp = visit(method=test_info["method"],                     url=Handler.host + test_info["url"],                     json=json.loads(test_info["data"]))        expected = json.loads(test_info["expected"])        if test_info["case_id"] == 2:            self.assertTrue(expected["brand"] == jsonpath(resp, "$..brand")[0])        self.assertTrue(expected["code"] == resp["code"])        self.assertTrue(expected["msg"] == resp["msg"])        # self.assertTrue(expected["data"][0]["series"] == resp["data"][0]["series"])        logger.info("第{}条测试用例通过".format(test_info["case_id"]))if __name__ == '__main__':    unittest.main()