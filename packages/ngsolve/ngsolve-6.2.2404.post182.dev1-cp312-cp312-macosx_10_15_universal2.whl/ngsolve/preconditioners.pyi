from __future__ import annotations
from ngsolve.comp import BDDCPreconditioner as BDDC
from ngsolve.comp import HCurlAMG
from ngsolve.comp import LocalPreconditioner as Local
from ngsolve.comp import MultiGridPreconditioner as MultiGrid
__all__ = ['BDDC', 'HCurlAMG', 'Local', 'MultiGrid']
