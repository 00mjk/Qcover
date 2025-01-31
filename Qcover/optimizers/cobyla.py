from typing import Optional
import logging
import numpy as np

from scipy import optimize as opt

logger = logging.getLogger(__name__)


class COBYLA:
    """
    COBYLA: a numerical optimization method for constrained problems

    based on scipy.optimize.minimize COBYLA.
    For further detail, please refer to
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    """

    # pylint: disable=unused-argument
    def __init__(self,
                 maxiter: int = 30,
                 initial_point: Optional[np.ndarray] = None,
                 disp: bool = False,
                 rhobeg: float = 1.0,
                 tol: Optional[float] = 1e-6) -> None:
        """
        Args:
            maxiter: Maximum number of function evaluations.
            disp: Set to True to print convergence messages.
            rhobeg: Reasonable initial changes to the variables.
            tol: Final accuracy in the optimization (not precisely guaranteed).
                 This is a lower bound on the size of the trust region.
        """
        self._p = None
        self._tol = tol
        self._options = {'rhobeg': rhobeg, 'maxiter': maxiter, 'disp': disp}
        self._initial_point = initial_point

    def optimize(self, objective_function, p):
        if self._initial_point is None:
            self._initial_point = np.array([np.random.random() for x in range(2 * p)])

        res = opt.minimize(objective_function,
                           x0=np.array(self._initial_point),
                           args=p,
                           method='COBYLA',
                           tol=self._tol,
                           jac=opt.rosen_der,
                           options=self._options)
        return res.x, res.fun, res.nfev