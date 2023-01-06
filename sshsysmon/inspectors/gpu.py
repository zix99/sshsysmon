from lib.plugins import Inspector
from lib.util import ByteSize

"""
Description:
    GPUMemory executes `nvidia-smi` to discover how much gpu memory is remaining

Constructor:
    device: The gpu id (eg 0 or 1) (Default: 0)
    vendor: The GPU vendor (eg NVIDIA) (Default: NVIDIA)

Metrics:
    size: ByteSize of the device
    used: ByteSize of used memory
    available: ByteSize of the available memory
    percentage_full: The integer percentage of how full the memory is
"""
class GPUMemory(Inspector):
    def __init__(self, driver, device = 0, vendor = 'NVIDIA'):
        self._driver = driver
        self._device = device
        self._vendor = vendor

    def getMetrics(self):
        if self._vendor == 'NVIDIA':
            df = self._driver.sh('nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv')

            #Parse and find matching metric
            line = df['stdout'].splitlines()[1 + self._device]
            segs = line.replace('MiB', '').split(', ')
            metric = list(map(int, segs))

        else:
            raise NotImplementedError(f"No implementation found for vendor '{self._vendor}'!")

        if not metric:
            return {}

        return {
            "size" : ByteSize(metric[0], "mb"),
            "used" : ByteSize(metric[1], "mb"),
            "available" : ByteSize(metric[2], "mb"),
            "percent_full" : int(round(metric[1] / metric[0]))
        }

    def getName(self):
        return "GPU Memory: %s" % (self._device)

    def getSummary(self):
        metrics = self.getMetrics()
        return "%s: %s total, %s used, %s free (%s%%)\n" % (self._device, metrics['size'], metrics['used'], metrics['available'], metrics['percent_full'])

def create(driver, args):
    return GPUMemory(driver, **args)
