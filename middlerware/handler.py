import os
import random
import re
from pymysql.cursors import DictCursor
from common.excel_handler import ExcelHandler
from common.mysql_handler import MysqlHandler
from common.yaml_handler import red_config
from config import config
from common.log_handler import get_logging


class Handler():
    # 环境地址
    host = "http://toro.buttonupup.com:8085"

    # 获取yaml文件内容
    yaml_data = red_config(config.CONF_PATH)
    # 初始化logger
    logger = get_logging(**yaml_data["log"], file_name=config.LOG_PATH)
    # 读取Excel表格
    excel = ExcelHandler(os.path.join(config.DATA_PATH, yaml_data["excel"]["file_name"]))

    # 发送邮件
    # send_mail = send_mail(**yaml_data["email_address"], file_name="")

    @property
    def plate(self):
        return random_plate()

    @property
    def no_bind_sn(self):
        return no_bind_sn()

    @property
    def bind_sn(self):
        return bind_sn()

    @property
    def self_bind_sn(self):
        return self_bind_sn(1)

    @property
    def self_bind_carid(self):
        return self_bind_carid(1)

    @property
    def attention_carid(self):
        return attention_carid(1)


def db_connet(idx, sql, bool):
    db_config = Handler().yaml_data["db"]
    db = MysqlHandler(host=db_config["host"],
                      port=3306,
                      user=db_config["user"],
                      password=db_config["password"],
                      charset="UTF8",
                      database=db_config["database"][idx],
                      cursorclass=DictCursor)
    return db.query(sql, one=bool)


def bind_sn():
    exist_device = db_connet(0, "SELECT sn FROM tb_device;", True)
    return exist_device["sn"]


def no_bind_sn():
    all_device = db_connet(1, "SELECT sn FROM tb_warehouse_detail;", False)
    exist_device = db_connet(0, "SELECT sn FROM tb_device;", False)
    exist_list = []
    for i in exist_device:
        exist_list.append(i["sn"])
    # print(exist_list)
    try:
        while True:
            for device_sn in all_device:
                if device_sn["sn"] not in exist_list:
                    return str(device_sn["sn"])
    except Exception as e:
        return e


def self_bind_sn(uid):
    sql = "select sn from tb_device where car_id in (select car_id from tb_user_managers where user_id = {});".format(uid)
    device_data = db_connet(0, sql, True)
    return device_data["sn"]


# 账号绑定的carId
def self_bind_carid(uid):
    sql = "select car_id from tb_user_managers where user_id = {}".format(uid)
    carId_data = db_connet(0, sql, True)
    return carId_data["car_id"]


def attention_carid(uid):
    sql = "select car_id from tb_user_attention where user_id = {};".format(uid)
    attention_data = db_connet(0, sql, True)
    return attention_data["car_id"]


def random_plate():
    end_num = "".join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 5))
    plate = "粤B" + end_num
    plate_data = db_connet(0, "SELECT plate FROM tb_car where plate ='{}';".format(plate), True)
    if not plate_data:
        return plate


class MySqlHandlerWare(MysqlHandler):
    """
    继承MysqlHandler,
    """
    def __init__(self):
        """
        初始化所有的配置项，从yaml中读取
        """
        db_config = Handler().yaml_data["db"]
        super().__init__(host=db_config["host"],
                         port=3306,
                         user=db_config["user"],
                         password=db_config["password"],
                         charset="UTF8",
                         database=db_config["database"][0],
                         cursorclass=DictCursor)


# 难点
def replace_data(object, data):
    patten = r"#(.*?)#"
    while re.search(patten, data):
        key = re.search(patten, data).group(1)
        value = getattr(object, key, "")
        data = re.sub(patten, str(value), data, 1)
    return data


if __name__ == '__main__':
    # print(random_plate())
    # print(bind_sn())
    print(no_bind_sn())
    # print(self_bind_sn(1))
    # print(attention_carid(1))

