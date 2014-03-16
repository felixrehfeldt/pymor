# This file is part of the pyMOR project (http://www.pymor.org).
# Copyright Holders: Felix Albrecht, Rene Milk, Stephan Rave
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

from pymor.core.interfaces import (BasicInterface, ImmutableInterface, abstractmethod, abstractclassmethod,
                                   abstractstaticmethod, abstractproperty, inject_sid, disable_sid_generation,
                                   enable_sid_generation)
from pymor.core.logger import getLogger



class Unpicklable(object):
    '''Mix me into classes you know cannot be pickled.
    Our test system won't try to pickle me then
    '''
    pass


