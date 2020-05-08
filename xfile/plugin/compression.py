from xfile.base import File, Plugin, PluginResult, PluginResults
from rads2file.ads import AppException, AdsAnalyzer

class RarAdsPlugin(Plugin):
    name = 'rarads'
    def run(self, file: File, results: PluginResults) -> PluginResult:
        try:
            ads = AdsAnalyzer(file.as_posix())
            streams = ads.analyze()
            if len(streams) > 0:
                result = PluginResult(self.name)
                result.set('streams', len(streams))
                results.add(result)
        except AppException:
            return