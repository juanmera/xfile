import pathlib
from functools import reduce
from pkgutil import iter_modules
from importlib import import_module
from itertools import chain
from inspect import isclass, getmembers

class AppException(Exception):
    pass


class File:
    def __init__(self, filename):
        self.path = pathlib.Path(filename)

    def as_posix(self):
        return self.path.as_posix()


class PluginResult:
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.properties = {}

    def get(self, name):
        if name in self.properties:
            return self.properties[name]
        return None

    def set(self, name, value):
        self.properties[name] = value

    def show(self):
        print(f'PLUGIN: {self.plugin_name}')
        for k, v in self.properties.items():
            print(f'{k}: {v}')
        print()

class PluginResults():
    def __init__(self):
        self.items = []

    def add(self, item: PluginResult):
        self.items.append(item)

    def property(self, name):
        for item in self.items:
            value = item.get(name)
            if value is not None:
                return value
        return None

    def show(self):
        for item in self.items:
            item.show()

    def __iter__(self):
        return iter(self.items)


class Plugin:
    def run(self, file: File, prev_results: PluginResults) -> PluginResult:
        pass


class Engine:
    def __init__(self, plugins=None):
        self.plugins = plugins or self.plugins()

    @staticmethod
    def plugins():
        ns_pkg = import_module('xfile.plugin')
        plugins = iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")
        modules = [import_module(name) for _, name, _ in plugins]
        return [c() for n, c in chain(*map(getmembers, modules)) if isclass(c) and issubclass(c, Plugin) and c!=Plugin]

    def run(self, file: File):
        results = PluginResults()
        for plugin in self.plugins:
            plugin.run(file, results)
        return results
