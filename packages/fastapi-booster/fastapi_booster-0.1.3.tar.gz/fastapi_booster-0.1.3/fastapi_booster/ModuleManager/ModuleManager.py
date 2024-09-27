from fastapi import FastAPI
from fastapi_booster.LifeSpanManager import startup_function, shutdown_function
from fastapi_booster import logger
from typing import Dict
from fastapi_booster.Module import Module


class ModuleManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModuleManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.modules: Dict[str, Module] = {}

        @startup_function
        def module_db_init():
            for module in self.modules.values():
                logger.info(f"Module {module.name}:\tinitializing...")
                module.update_all_tables_schema()
                logger.info(f"Module {module.name}:\tinitialized")


module_manager = ModuleManager()
