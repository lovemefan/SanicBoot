# -*- coding:utf-8 -*-
# @FileName  :__init__.py.py
# @Time      :2023/3/19 01:38
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com

import importlib
import os
from pathlib import Path

from backend.utils.logger import logger

project_root_path = os.path.dirname(__file__)

# automatically import any Python files in the models/ directory
module_dir = Path(os.path.dirname(__file__))


def import_models(module_dir, namespace):
    for file in Path(module_dir).rglob("*.py"):
        if not file.name.startswith("_"):
            file_path = str(file.absolute())
            datasource_name = file_path[
                file_path.find(namespace.replace(".", "/")) : file_path.find(".py")
            ]
            datasource_name = (
                datasource_name.replace("/", ".").replace(namespace, "").strip(".")
            )
            logger.debug("Importing datasource: {}".format(datasource_name))
            importlib.import_module(namespace + "." + datasource_name)


import_models(module_dir / "core/datasource", "backend.core.datasource")
import_models(module_dir / "repository", "backend.repository")
import_models(module_dir / "services", "backend.services")
import_models(module_dir / "controllers", "backend.controllers")
