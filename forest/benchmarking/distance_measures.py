"""A module for computing distances (and other properites) between quantum states or
processes"""
import numpy as np
from scipy.linalg import sqrtm
from scipy.linalg import fractional_matrix_power
from scipy.optimize import minimize_scalar


# ===================================================================================================
# Functions for quantum states
# ===================================================================================================

def purity(rho, dim_renorm=False):
    """
    Calculates the purity P = tr[ρ**2] of a quantum state ρ.

    As stated above lower value of the purity depends on the dimension of ρ's Hilbert space. For
    some applications this can be undesirable. For this reason we introduce an optional dimensional
    renormalization flag with the following behavior

    If the dimensional renormalization flag is FALSE (default) then  1/dim ≤ P ≤ 1.
    If the dimensional renormalization flag is TRUE then 0 ≤ P ≤ 1.

    where dim is the dimension of ρ's Hilbert space.

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param dim_renorm: Boolean, default False.
    :return: P the purity of the state.
    """
    if dim_renorm:
        dim = np.shape(rho)[0]
        Ptemp = np.trace(np.matmul(rho, rho))
        P = (dim / (dim - 1.0)) * (Ptemp - 1.0 / dim)
    else:
        P = np.trace(np.matmul(rho, rho))
    return P


def fidelity(rho, sigma):
    """
    Computes the fidelity F(rho,sigma) between two quantum states rho and sigma.

    If the states are pure the expression reduces to F(|psi>,|phi>) = |<psi|phi>|^2.

    The fidelity obeys 0 ≤ F(rho,sigma) ≤ 1, where F(rho,sigma)=1 iff rho = sigma and
    F(rho,sigma)= 0 iff

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param sigma: Is a dim by dim positive matrix with unit trace.
    :return: Fidelity which is a scalar.
    """
    return (np.trace(sqrtm(np.matmul(np.matmul(sqrtm(rho), sigma), sqrtm(rho))))) ** 2


def trace_distance(rho, sigma):
    """
    Computes the trace distance between two states rho and sigma i.e.
    T(rho,sigma) = (1/2)||rho-sigma||_1 , where ||X||_1 denotes the 1 norm of X.

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param sigma: Is a dim by dim positive matrix with unit trace.
    :return: Trace distance which is a scalar.
    """
    return (0.5) * np.linalg.norm(rho - sigma, 1)


def bures_distance(rho, sigma):
    """
    Computes the Bures distance between two states rho and sigma i.e.
    D_B(rho,sigma)^2 = 2(1- sqrt[F(rho,sigma)]) , where F(rho,sigma) is the fidelity.

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param sigma: Is a dim by dim positive matrix with unit trace.
    :return: Bures distance which is a scalar.
    """
    return np.sqrt(2 * (1 - np.sqrt(fidelity(rho, sigma))))


def bures_angle(rho, sigma):
    """
    Computes the Bures angle (AKA Bures arc or Bures length) between two states rho and sigma i.e.
    D_A(rho,sigma) = arccos(sqrt[F(rho,sigma)]) , where F(rho,sigma) is the fidelity.
    The Bures angle is a measure of statistical distance between quantum states.

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param sigma: Is a dim by dim positive matrix with unit trace.
    :return: Bures angle which is a scalar.
    """
    return np.arccos(np.sqrt(fidelity(rho, sigma)))


def quantum_chernoff_bound(rho, sigma):
    """
    Computes the quantum Chernoff bound between rho and sigma. It is defined as

    ξ_{QCB}(rho,sigma) = - log[ min_{0\le s\le 1} tr(rho**s sigma**{1-s} ].

    It is also common to study the non-logarithmic variety of the quantum Chernoff bound denoted as

    Q_{QCB}(rho,sigma) = min_{0\le s\le 1} tr(rho**s sigma**{1-s}.

    The quantum Chernoff bound has many nice properties, see [QCB]. Importantly it is
    operationally important in the following context. Given n copies of rho or sigma the minimum
    error probability for discriminating for rho from sigma is P_{e,min,n} ~ exp[-n ξ_{QCB}].
    
    [QCB] The Quantum Chernoff Bound
          Audenaert et al.,
          Phys. Rev. Lett. 98, 160501 (2007)
          https://dx.doi.org/10.1103/PhysRevLett.98.160501
          https://arxiv.org/abs/quant-ph/0610027

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param sigma: Is a dim by dim positive matrix with unit trace.
    :return: the non-logarithmic quantum Chernoff bound and the s achieving the minimum.
    """
    def f(s):
        s = np.real_if_close(s)
        return np.trace(
            np.matmul(fractional_matrix_power(rho, s), fractional_matrix_power(sigma, 1 - s)))

    f_min = minimize_scalar(f, bounds=(0, 1), method='bounded')
    s_opt = f_min.x
    qcb = f_min.fun
    return qcb, s_opt


def hilbert_schmidt_ip(A, B):
    r"""
    Computes the Hilbert-Schmidt (HS) inner product between two operators A and B as
        HS = (A|B) = Tr[A^\dagger B]
    where |B) = vec(B) and (A| is the dual vector to |A).

    :param A: Is a dim by dim positive matrix with unit trace.
    :param B: Is a dim by dim positive matrix with unit trace.
    :return: HS inner product which is a scalar.
    """
    return np.trace(np.matmul(np.transpose(np.conj(A)), B))


def smith_fidelity(rho, sigma, power):
    """
    Computes the Smith fidelity F_S(rho,sigma,power) between two quantum states rho and sigma.

    The Smith fidelity is  defined as F_S = sqrt(F)^power, where F is  standard fidelity
    F = fidelity(rho, sigma). As the power is only defined for values less than 2, F_S > F.
    At present there is no known operational interpretation of the Smith fidelity for an arbitrary
    power.

    :param rho: Is a dim by dim positive matrix with unit trace.
    :param sigma: Is a dim by dim positive matrix with unit trace.
    :param power: Is a positive scalar less than 2.
    :return: Smith Fidelity which is a scalar.
    """
    if power < 0:
        raise ValueError("Power must be positive")
    if power >= 2:
        raise ValueError("Power must be less than 2")
    return np.sqrt(fidelity(rho, sigma)) ** power


def total_variation_distance(P, Q):
    r"""
    Computes the total variation distance between two probability measures P(x) and Q(x).

    When x is a finite alphabet then the definition is

    tvd(P,Q) = (1/2) \sum_x |P(x) - Q(x)|

    where tvd(P,Q) is in [0,1]. There is an alternate definition for non-finite alphabet measures
    involving a supremum.

    :param P: Is a numpy array of length dim.
    :param Q: Is a numpy array of length dim.
    :return: total variation distance which is a scalar.
    """
    if len(P) != len(Q):
        raise ValueError("Arrays must be the same length")

    return (np.sum( np.abs(P - Q) ) / 2)


# ============================================================================
# Functions for quantum processes
# ============================================================================
def entanglement_fidelity(pauli_lio0: np.ndarray, pauli_lio1: np.ndarray) -> float:
    """Returns the entanglement fidelity (F_e) between two channels, E and F, represented as Pauli
    Liouville matrix. The expression is

            F_e(E,F) = Tr[E^\dagger F] / (dim ** 2),

    where dim is the dimension of the Hilbert space associated with E and F.

    See the following references for more information:

    [GRAPTN] referenced in the superoperator_tools module. In particular section V subsection G.

    [H**3] General teleportation channel, singlet fraction and quasi-distillation
           Horodecki et al.,
           PRA 60, 1888 (1999).
           https://doi.org/10.1103/PhysRevA.60.1888
           https://arxiv.org/abs/quant-ph/9807091

    [GFID] A simple formula for the average gate fidelity of a quantum dynamical operation
           M. Nielsen,
           Physics Letters A 303, 249 (2002)
           https://doi.org/10.1016/S0375-9601(02)01272-0
           https://arxiv.org/abs/quant-ph/0205035

    :param pauli_lio0: A dim**2 by dim**2 Pauli-Liouville matrix
    :param pauli_lio1: A dim**2 by dim**2 Pauli-Liouville matrix
    :return: Returns the entanglement fidelity between pauli_lio0 and pauli_lio1 which is a scalar.
    """
    assert pauli_lio0.shape == pauli_lio1.shape
    assert pauli_lio0.shape[0] == pauli_lio1.shape[1]
    dim_squared = pauli_lio0.shape[0]
    dim = int(np.sqrt(dim_squared))
    return np.trace(np.matmul(np.transpose(np.conj(pauli_lio0)), pauli_lio1)) / (dim ** 2)


def process_fidelity(pauli_lio0: np.ndarray, pauli_lio1: np.ndarray) -> float:
    r"""Returns the fidelity between two channels, E and F, represented as Pauli Liouville matrix.

    The expression is

             F_process(E,F) = ( Tr[E^\dagger F] + dim ) / (dim^2 + dim),

    which is sometimes written as

            F_process(E,F) = ( dim F_e + 1 ) / (dim + 1)

    where dim is the dimension of the Hilbert space asociated with E and F, and F_e is the
    entanglement fidelity see https://arxiv.org/abs/quant-ph/9807091 .

    NOTE: F_process is sometimes "gate fidelity" and F_e is sometimes called "process fidelity".

    If E is the ideal process, e.g. a perfect gate, and F is an experimental estimate of the
    actual process then the corresponding infidelity 1−F_process(E,F) can be seen as a
    measure of gate error, but it is not a proper metric.

    For more information see:

    [GFID] A simple formula for the average gate fidelity of a quantum dynamical operation
           M. Nielsen,
           Physics Letters A 303, 249 (2002)
           https://doi.org/10.1016/S0375-9601(02)01272-0
           https://arxiv.org/abs/quant-ph/0205035

    :param pauli_lio0: A dim**2 by dim**2 Pauli-Liouville matrix
    :param pauli_lio1: A dim**2 by dim**2 Pauli-Liouville matrix
    :return: The process fidelity between pauli_lio0 and pauli_lio1 which is a scalar.
    """
    assert pauli_lio0.shape == pauli_lio1.shape
    assert pauli_lio0.shape[0] == pauli_lio1.shape[1]
    dim_squared = pauli_lio0.shape[0]
    dim = int(np.sqrt(dim_squared))

    Fe = entanglement_fidelity(pauli_lio0, pauli_lio1)

    return (dim * Fe + 1) / (dim + 1)


def diamond_norm_distance(choi0: np.ndarray, choi1: np.ndarray) -> float:
    """
    Return the diamond norm distance between two completely positive
    trace-preserving (CPTP) superoperators, represented as Choi matrices.

    The calculation uses the simplified semidefinite program of Watrous

    [CBN] Semidefinite programs for completely bounded norms
          J. Watrous
          Theory of Computing 5, 11, pp. 217-238 (2009)
          http://theoryofcomputing.org/articles/v005a011
          http://arxiv.org/abs/0901.4709

    This calculation becomes very slow for 4 or more qubits.

    :param choi0: A 4**N by 4**N matrix (where N is the number of qubits)
    :param choi1: A 4**N by 4**N matrix (where N is the number of qubits)

    """
    # Kudos: Based on MatLab code written by Marcus P. da Silva
    # (https://github.com/BBN-Q/matlab-diamond-norm/)
    import cvxpy as cvx
    assert choi0.shape == choi1.shape
    assert choi0.shape[0] == choi1.shape[1]
    dim_squared = choi0.shape[0]
    dim = int(np.sqrt(dim_squared))

    delta_choi = choi0 - choi1
    delta_choi = (delta_choi.conj().T + delta_choi) / 2  # Enforce Hermiticity

    # Density matrix must be Hermitian, positive semidefinite, trace 1
    rho = cvx.Variable([dim, dim], complex=True)
    constraints = [rho == rho.H]
    constraints += [rho >> 0]
    constraints += [cvx.trace(rho) == 1]

    # W must be Hermitian, positive semidefinite
    W = cvx.Variable([dim_squared, dim_squared], complex=True)
    constraints += [W == W.H]
    constraints += [W >> 0]

    constraints += [(W - cvx.kron(np.eye(dim), rho)) << 0]

    J = cvx.Parameter([dim_squared, dim_squared], complex=True)
    objective = cvx.Maximize(cvx.real(cvx.trace(J.H * W)))

    prob = cvx.Problem(objective, constraints)

    J.value = delta_choi
    prob.solve()

    dnorm = prob.value * 2

    return dnorm


def _is_square(n):
    return n == np.round(np.sqrt(n))**2


def watrous_bounds(choi: np.ndarray) -> float:
    """Return the Watrous bounds for the diamond norm of a superoperator in
    the Choi representation. If this is applied to the difference of two Choi 
    representations, it yields bounds to the diamond norm distance.

    The bound can be found in [this](https://cstheory.stackexchange.com/a/4920)
    StackOverflow answer, although the results can also be found scattered in 
    the literature.

    :param choi: dim1 by dim2 matrix (for qubits, dimi = 4**Ni, where Ni is a number of qubits)
    """

    if len(choi.shape) != 2:
        raise ValueError("Watrous bounds only defined for matrices")

    if not(_is_square(choi.shape[0]) and _is_square(choi.shape[1])):
        raise ValueError("Choi matrix must have dimensions that are perfect squares")
    
    _,s,_ = np.linalg.svd(choi)
    nuclear_norm = np.sum(s)
    
    return (nuclear_norm, choi.shape[0]*nuclear_norm)
