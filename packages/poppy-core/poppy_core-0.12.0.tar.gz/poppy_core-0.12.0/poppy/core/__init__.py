#! /usr/bin/env python
# -*- coding: utf-8 -*-
from importlib.metadata import version

# interrogate version string of already-installed distribution
__version__ = version("poppy-core")

from poppy.core.tools.exceptions import *  # noqa: F403
from poppy.core.logger import *  # noqa: F403
