import os
from dataclasses import dataclass

import yaml

BASE_DIR = os.path.expanduser('~/.zyplib')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.yaml')


@dataclass
class Config:
    DISK_CACHE_DIR: str = '~/.zyplib/cache'


def _write_config(config: Config):
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    config_path = os.path.expanduser(CONFIG_PATH)
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file)


def _load_config() -> Config:
    # 获取配置文件路径
    config_path = os.path.expanduser(CONFIG_PATH)

    # 如果配置文件存在，则加载配置文件
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)

        # 覆盖默认配置
        return Config(**config_data)
    else:
        # 如果配置文件不存在，返回默认配置
        config = Config()
        _write_config(config)
        return config


# 实例化配置，在模块导入时加载
config = _load_config()
