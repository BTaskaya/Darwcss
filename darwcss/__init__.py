# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = "1"
except DistributionNotFound:
    __version__ = "1"
finally:
    del get_distribution, DistributionNotFound
