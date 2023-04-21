# -*- coding:utf-8 -*-
# @FileName  :__init__.py.py
# @Time      :2023/3/19 01:38
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com

import importlib
import os
from pathlib import Path

from backend.config.Config import Config
from backend.utils.logger import logger

project_root_path = os.path.dirname(__file__)

# automatically import any Python files in the models/ directory
module_dir = Path(os.path.dirname(os.path.dirname(__file__)))


def import_models(module_dir, namespace):
    for file in Path(module_dir).rglob("*.py"):
        if not file.name.startswith("_"):
            file_path = str(file.absolute())
            module_name = file_path[
                file_path.find(namespace.replace(".", "/")) : file_path.find(".py")
            ]
            module_name = (
                module_name.replace("/", ".").replace(namespace, "").strip(".")
            )
            logger.debug("Importing module: {}".format(module_name))
            importlib.import_module(namespace + "." + module_name)


module_path = module_dir / Config.get_instance().get(
    "server.component.datasource"
).replace(".", "/").strip("/")
module_namespace = Config.get_instance().get("server.component.datasource")
if os.path.exists(module_path):
    import_models(module_path, module_namespace)
else:
    raise ValueError(
        f"{module_path} not exists, please check config of server.component.datasource"
    )


module_path = module_dir / Config.get_instance().get(
    "server.component.repository"
).replace(".", "/").strip("/")
module_namespace = Config.get_instance().get("server.component.repository")
if os.path.exists(module_path):
    import_models(module_path, module_namespace)
else:
    raise ValueError(
        f"{module_path} not exists, please check config of server.component.repository"
    )

module_path = module_dir / Config.get_instance().get(
    "server.component.service"
).replace(".", "/").strip("/")
module_namespace = Config.get_instance().get("server.component.service")
if os.path.exists(module_path):
    import_models(module_path, module_namespace)
else:
    raise ValueError(
        f"{module_path} not exists, please check config of server.component.service"
    )


module_path = module_dir / Config.get_instance().get(
    "server.component.controller"
).replace(".", "/").strip("/")
module_namespace = Config.get_instance().get("server.component.controller")
if os.path.exists(module_path):
    import_models(module_path, module_namespace)
else:
    raise ValueError(
        f"{module_path} not exists, please check config of server.component.controller"
    )
