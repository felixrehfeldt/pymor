# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

import numpy as np
from scipy.sparse.linalg import bicg
from scipy.sparse import issparse

from pymor.core import BasicInterface, defaults
from pymor.core.cache import Cachable, cached, DEFAULT_DISK_CONFIG
from pymor.tools import dict_property, Named
from pymor.domaindescriptions import BoundaryType
from pymor.parameters import Parametric
from pymor.discreteoperators import LinearDiscreteOperatorInterface


class StationaryLinearDiscretization(BasicInterface, Parametric, Cachable, Named):
    '''Generic class for discretizations of stationary linear problems.

    This class describes discrete problems given by the equation ::

        L_h(μ) ⋅ u_h(μ) = f_h(μ)

    which is to be solved for u_h.

    Note that we do not make any distinction between detailed and reduced
    discretizations here.

    The results of solve() are cached by default so it is inexpensive to call solve
    repeatedly for the same parameter.

    Parameters
    ----------
    operator
        The operator L_h given as a `LinearDiscreteOperator`.
    rhs
        The functional f_h given as a `LinearDiscreteOperator` with `dim_range == 1`.
    solver
        A function solver(A, RHS), which solves the matrix equation A*x = RHS.
        If None, numpy.linalg.solve() or scipy.sparse.linalg.bicg are chosen as
        solvers depending on the sparsity of A.
    visualizer
        A function visualize(U) which visualizes the solution vectors. Can be None,
        in which case no visualization is availabe.
    name
        Name of the discretization.

    Attributes
    ----------
    disable_logging
        If True, no log message is displayed when calling solve. This is useful if
        we want to log solves of detailed discretization but not of reduced ones.
        In the future, this should be a feature of BasicInterface.
    operator
        The operator L_h. A synonym for operators['operator'].
    operators
        Dictionary of all operators contained in this discretization. The idea is
        that this attribute will be common to all discretizations such that it can
        be used for introspection. Compare the implementation of `GenericRBReductor`.
        For this class, operators has the keys 'operator' and 'rhs'.
    rhs
        The functional f_h. A synonym for operators['rhs'].

    Inherits
    --------
    BasicInterface, Parametric, Cachable, Named.
    '''

    disable_logging = False
    operator = dict_property('operators', 'operator')
    rhs = dict_property('operators', 'rhs')

    def __init__(self, operator, rhs, solver=None, visualizer=None, name=None):
        assert isinstance(operator, LinearDiscreteOperatorInterface)
        assert isinstance(rhs, LinearDiscreteOperatorInterface)
        assert operator.dim_source == operator.dim_range == rhs.dim_source
        assert rhs.dim_range == 1

        Cachable.__init__(self, config=DEFAULT_DISK_CONFIG)
        self.operators = {'operator': operator, 'rhs':rhs}
        self.build_parameter_type(inherits={'operator':operator, 'rhs':rhs})

        def default_solver(A, RHS):
            if issparse(A):
                U, _ = bicg(A, RHS, tol=defaults.bicg_tol, maxiter=defaults.bicg_maxiter)
            else:
                U = np.linalg.solve(A, RHS)
            return U
        self.solver = solver or default_solver

        if visualizer is not None:
            self.visualize = visualizer

        self.solution_dim = operator.dim_range
        self.name = name

    def copy(self):
        c = copy.copy(self)
        c.operators = c.operators.copy()
        Cachable.__init__(c)
        return c

    @cached
    def solve(self, mu={}):
        mu = self.parse_parameter(mu)
        A = self.operator.matrix(self.map_parameter(mu, 'operator'))

        if not self.disable_logging:
            sparse = 'sparse' if issparse(A) else 'dense'
            self.logger.info('Solving {} ({}) for {} ...'.format(self.name, sparse, mu))

        if A.size == 0:
            return np.zeros(0)
        RHS = np.squeeze(self.rhs.matrix(self.map_parameter(mu, 'rhs')))
        if RHS.ndim == 0:
            RHS = RHS[np.newaxis]

        return self.solver(A, RHS)

