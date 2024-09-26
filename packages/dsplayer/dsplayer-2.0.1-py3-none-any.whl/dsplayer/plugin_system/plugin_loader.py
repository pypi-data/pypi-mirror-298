import importlib
import importlib.metadata
import pkgutil
from dsplayer.plugin_system.plugin_interface import PluginInterface
from typing import List, Optional, Dict, Any, Type
from dsplayer.utils.debug import Debuger


class PluginLoader:
    def __init__(self, plugin_packages: List[str] = []):
        self.plugin_packages = plugin_packages.append('dsplayer.plugin_system')
        self.plugin_classes: List[Type[PluginInterface]] = []
        self.plugins: List[PluginInterface] = []
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self._load_plugins()

    def debug(self):
        self.debug_mode = True

    def load_plugins_from_classes(
            self, plugin_classes: List[Type[PluginInterface]]) -> None:
        self.plugin_classes = plugin_classes
        for plugin_class in self.plugin_classes:
            if issubclass(plugin_class, PluginInterface):
                plugin_instance = plugin_class()
                self.plugins.append(plugin_instance)
                plugin_instance.on_plugin_load()
        self.debug_print("Plugins loaded from classes!")

    def _load_plugins(self) -> None:
        for plugin_package in self.plugin_packages:
            package = importlib.import_module(plugin_package)
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                if not is_pkg and name.endswith('_plugin'):
                    module = importlib.import_module(
                        f"{plugin_package}.{name}")
                    for attr in dir(module):
                        cls = getattr(module, attr)
                        if isinstance(
                                cls, type) and issubclass(
                                cls, PluginInterface) and cls is not PluginInterface:
                            plugin_instance = cls()
                            self.plugins.append(plugin_instance)
                            plugin_instance.on_plugin_load()

        entry_points = importlib.metadata.entry_points()
        dsplayer_plugins = entry_points.select(group='dsplayer.plugins')
        for entry_point in dsplayer_plugins:
            plugin_class = entry_point.load()
            if issubclass(plugin_class, PluginInterface):
                plugin_instance = plugin_class()
                self.plugins.append(plugin_instance)
                plugin_instance.on_plugin_load()

        self.debug_print("All plugins are loaded!")

    def get_plugins(self) -> List[PluginInterface]:
        return self.plugins

    def get_plugin_by_name(
            self,
            plugin_name: str) -> Optional[PluginInterface]:
        for plugin in self.plugins:
            if plugin.get_plugin_name() == plugin_name:
                return plugin
        return None

    def update_plugin_settings(
            self, plugin_name: str, settings: Dict[str, Any]) -> bool:
        plugin = self.get_plugin_by_name(plugin_name)
        if plugin:
            plugin.update_settings(settings)
            return True
        return False
