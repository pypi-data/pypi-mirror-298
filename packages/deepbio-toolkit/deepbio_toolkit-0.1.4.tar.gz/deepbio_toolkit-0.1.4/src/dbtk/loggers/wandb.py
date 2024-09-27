from lightning.pytorch.loggers import WandbLogger as WandbLoggerBase
from typing_extensions import override

from .._utils import export

@export
class WandbLogger(WandbLoggerBase):
    @property
    @override
    def save_dir(self):
        """
        This method is not implemented correctly in Lightning.
        This implementation returns the correct save directory for logging.
        """
        return self.experiment.dir
