import networkx as nx
from pyquil.api import QPUCompiler

from forest.benchmarking.entangled_states import create_graph_state as create_graph_state_good
from forest.benchmarking.entangled_states import measure_graph_state as measure_graph_state_good
from forest.benchmarking.entangled_states import compiled_parametric_graph_state as \
    compiled_parametric_graph_state_good

import warnings
import functools

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}. \r\n \r\n Use the graph state functions in "
                      "forest.benchmarking.entangled_states instead.\r\n".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func

@deprecated
def create_graph_state(graph: nx.Graph, use_pragmas=True):
    """Write a program to create a graph state according to the specified graph

    A graph state involves Hadamarding all your qubits and then applying a CZ for each
    edge in the graph. A graph state and the ability to measure it however you want gives
    you universal quantum computation. Some good references are

    [MBQC] A One-Way Quantum Computer
           Raussendorf et al.,
           Phys. Rev. Lett. 86, 5188 (2001)
           https://doi.org/10.1103/PhysRevLett.86.5188
           https://arxiv.org/abs/quant-ph/0010033

    [MBCS] Measurement-based quantum computation with cluster states
           Raussendorf et al.,
           Phys. Rev. A 68, 022312 (2003)
           https://dx.doi.org/10.1103/PhysRevA.68.022312
           https://arxiv.org/abs/quant-ph/0301052

    Similar to a Bell state / GHZ state, we can try to prepare a graph state and measure
    how well we've done according to expected parities.

    :param graph: The graph. Nodes are used as arguments to gates, so they should be qubit-like.
    :param use_pragmas: Use COMMUTING_BLOCKS pragmas to hint at the compiler
    :return: A program that constructs a graph state.
    """
    return create_graph_state_good(graph, use_pragmas)

@deprecated
def measure_graph_state(graph: nx.Graph, focal_node: int):
    """Given a graph state, measure a focal node and its neighbors with a particular measurement
    angle.

    :param prep_program: Probably the result of :py:func:`create_graph_state`.
    :param qs: List of qubits used in prep_program or anything that can be indexed by the nodes
        in the graph ``graph``.
    :param graph: The graph state graph. This is needed to figure out what the neighbors are
    :param focal_node: The node in the graph to serve as the focus. The focal node is measured
        at an angle and all its neighbors are measured in the Z basis
    :return Program, list of classical offsets into the ``ro`` register.
    """
    return measure_graph_state_good(graph, focal_node)

@deprecated
def compiled_parametric_graph_state(graph, focal_node, compiler: QPUCompiler, n_shots=1000):
    """
    Construct a program to create and measure a graph state, map it to qubits using ``addressing``,
    and compile to an ISA.

    Hackily implement a parameterized program by compiling a program with a particular angle,
    finding where that angle appears in the results, and replacing it with ``"{angle}"`` so
    the resulting compiled program can be run many times by using python's str.format method.

    :param graph: A networkx graph defining the graph state
    :param focal_node: The node of the graph to measure
    :param compiler: The compiler to do the compiling.
    :param n_shots: The number of shots to take when measuring the graph state.
    :return: an executable that constructs and measures a graph state.
    """
    return compiled_parametric_graph_state_good(graph, focal_node, compiler, n_shots)
