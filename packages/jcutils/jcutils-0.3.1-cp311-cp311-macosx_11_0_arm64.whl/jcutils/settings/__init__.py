import json
import os
import sys
import tempfile
from pathlib import Path

import toml
from datamodel_code_generator import InputFileType, generate

from ..utils.platform_ import get_hostname, is_linux, is_mac, is_windows, is_wsl


class ConfigLoader:
    def __init__(self):
        self.HOSTNAME = get_hostname()
        self.MODE = os.environ.get("ENV", "")
        if self.MODE:
            pass
        elif is_windows() or is_mac() or is_wsl():
            self.MODE = "local"
        elif "dev" in self.HOSTNAME:
            self.MODE = "dev"
        elif "test" in self.HOSTNAME:
            self.MODE = "test"
        elif "prod" in self.HOSTNAME or is_linux:
            self.MODE = "prod"
        # 获取项目根目录
        self.PROJECT_DIR = os.getcwd()
        # 获取当前脚本所在的目录
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

        # 公共配置文件
        self.common_file_path = os.path.join(self.SCRIPT_DIR, "config.toml")
        # 加载公共配置
        self.config_dict = toml.load(self.common_file_path)

        # 获取项目配置文件目录
        self.CONF_DIR = self.config_dict["dirs"]["conf_dir"]
        if self.config_dict["app"]["name"] == "jcutils":  # jcutils项目的项目配置文件在它处
            self.env_file_path = os.path.join(self.CONF_DIR, f"config_{self.MODE}.toml")
        else:  # 非jcutils项目的项目配置文件在settings目录下
            self.env_file_path = os.path.join(self.SCRIPT_DIR, f"config_{self.MODE}.toml")

        self._init_common_config()
        # 加载环境配置
        env_config = toml.load(self.env_file_path)
        self._merge_configs(env_config)

        # 更新配置文件数据模型
        msg = self._init_model()

        print(f"环境初始化: load {self.MODE}, {msg}")

    def _merge_configs(self, env_config):
        for section, settings in env_config.items():
            if section in self.config_dict:
                self.config_dict[section].update(settings)
            else:
                self.config_dict[section] = settings

    def _init_common_config(self):
        # 公共配置
        self.APP_NAME = self.config_dict["app"]["name"]
        # 获取用户目录
        self.HOME_DIR = os.path.expanduser("~")
        self.DATA_DIR_DICT = {
            "win32": os.path.join("d:\\data\\appdata", self.APP_NAME),
            "darwin": os.path.join(f"{self.HOME_DIR}/data/appdata", self.APP_NAME),  # mac无法创建/data
            "default": os.path.join("/data/appdata", self.APP_NAME),
        }
        self.DATA_DIR = self.DATA_DIR_DICT.get(sys.platform, self.DATA_DIR_DICT["default"])

        # 拼接路径
        self.LOGS_DIR = os.path.join(self.DATA_DIR, self.config_dict["dirs"]["logs_dir"])
        self.TEMP_DIR = os.path.join(self.DATA_DIR, self.config_dict["dirs"]["temp_dir"])
        self.OUT_DIR = os.path.join(self.DATA_DIR, self.config_dict["dirs"]["out_dir"])
        self.MAIL_DIR = os.path.join(self.DATA_DIR, self.config_dict["dirs"]["mail_dir"])
        self.APP_LOG_PATH = os.path.join(self.DATA_DIR, self.config_dict["common"]["app_log_path"])

        self.config_dict["dirs"]["logs_path"] = self.LOGS_DIR
        self.config_dict["dirs"]["temp_path"] = self.TEMP_DIR
        self.config_dict["dirs"]["out_path"] = self.OUT_DIR
        self.config_dict["dirs"]["mail_path"] = self.MAIL_DIR
        self.config_dict["dirs"]["app_log_path"] = self.APP_LOG_PATH

        os.makedirs(self.LOGS_DIR, exist_ok=True)
        for dir_name in [self.LOGS_DIR, self.TEMP_DIR, self.OUT_DIR, self.MAIL_DIR]:
            os.makedirs(dir_name, exist_ok=True)

    def _init_model(self):
        json_str = json.dumps(self.config_dict, indent=4)
        output_file = os.path.join(self.SCRIPT_DIR, "model.py")
        with tempfile.NamedTemporaryFile("w", delete=True) as temp_file:
            temp_file_path = temp_file.name
            generate(
                input_=json_str,
                input_file_type=InputFileType.Json,  # 使用 'Json' 作为输入文件类型
                output=Path(temp_file_path),  # 输出到临时文件路径
                disable_timestamp=True,
            )

            with open(output_file, "r") as f:
                existing_code = f.read()

            with open(temp_file_path, "r") as temp_f:
                generated_code = temp_f.read()

            if existing_code != generated_code:
                # 如果代码有变化，则覆盖写入
                with open(output_file, "w") as f:
                    f.write(generated_code)
                msg = "配置已更新"
            else:
                msg = "配置无更新"
        return msg


config_loader = ConfigLoader()

# 导入配置数据模型(不要提到顶部导入)
from .model import Model  # noqa: E402, F811

config = Model.parse_obj(config_loader.config_dict)
