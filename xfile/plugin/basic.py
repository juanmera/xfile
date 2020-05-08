import os
import magic
import string
import binwalk
from xfile.base import File, Plugin, PluginResult, PluginResults


class BasicPlugin(Plugin):
    name = 'basic'

    def run(self, file: File, results: PluginResults) -> PluginResult:
        filename = file.as_posix()
        result = PluginResult(self.name)
        result.set('file_size', os.path.getsize(filename))
        result.set('magic_desc', magic.from_file(filename))
        result.set('magic_type', magic.from_file(filename, True))
        results.add(result)

class StringsPlugin(Plugin):
    BUFFER_SIZE = 4096
    PRINTABLE_CHARS = set(string.printable.encode()) - {0xa, 0xd}
    name = 'strings'

    def __init__(self, min_len=5):
        self.min_len = min_len

    def run(self, file: File, results: PluginResults) -> PluginResult:
        lines = []
        line = bytearray()
        in_line = False
        result = PluginResult(self.name)
        with file.path.open('rb') as f:
            buf = f.read(self.BUFFER_SIZE)
            for c in buf:
                if c in self.PRINTABLE_CHARS:
                    in_line = True
                    line.append(c)
                elif in_line:
                    in_line = False
                    if len(line) >= self.min_len:
                        lines.append(line.decode())
                    line.clear()
        result.set('lines', lines)
        results.add(result)

class BinWalkPlugin(Plugin):
    name = 'binwalk'

    def run(self, file: File, results: PluginResults) -> PluginResult:
        result = PluginResult(self.name)
        for module in binwalk.scan(file.as_posix(), signature=True, quiet=True):
            lines = []
            for mr in module.results:
                lines.append(f'{mr.offset}: {mr.description}')
            result.set(module.name, lines)
        results.add(result)