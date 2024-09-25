from pathlib import Path
from typing import Callable, Union

import numpy as np
from spinesUtils.asserts import raise_if

from ..configs.config import config
from ..storage_layer.storage import PersistentFileStorage
from ..core_components.kmeans import BatchKMeans
from ..core_components.ivf_index import IVFIndex
from ..core_components.locks import ThreadLock



class InvertedIndex:
    def __init__(self):
        pass