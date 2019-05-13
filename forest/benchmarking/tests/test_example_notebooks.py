import os
import pytest
from subprocess import PIPE, run

EXAMPLES_PATH = '../../../examples/'

# from https://stackoverflow.com/a/36058256
def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

# change directory to
os.chdir(EXAMPLES_PATH)


# NOTE: We are skipping any test that is longer than 30 seconds.
#       Also each test function has a print, if the test fails then you can see where from stdout.

# ~ 6 min; passed 2019/05/13
@pytest.mark.slow
def test_direct_fidelity_estimation_nb():
    #print(out('ls'))
    output_str = out('pytest --nbval-lax direct_fidelity_estimation.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_distance_measures_nb():
    output_str = out('pytest --nbval-lax distance_measures.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_direct_entangled_states_nb():
    output_str = out('pytest --nbval-lax entangled_states.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_Hinton_Plots_nb():
    output_str = out('pytest --nbval-lax Hinton-Plots.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~17 min; passed 2019/05/13
@pytest.mark.slow
def test_quantum_volume_nb():
    output_str = out('pytest --nbval-lax quantum_volume.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_qubit_spectroscopy_cz_ramsey_nb():
    output_str = out('pytest --nbval-lax qubit_spectroscopy_cz_ramsey.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_qubit_spectroscopy_rabi_nb():
    output_str = out('pytest --nbval-lax qubit_spectroscopy_rabi.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_qubit_spectroscopy_t1_nb():
    output_str = out('pytest --nbval-lax qubit_spectroscopy_t1.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_qubit_spectroscopy_t2_nb():
    output_str = out('pytest --nbval-lax qubit_spectroscopy_t2.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 sec
def test_random_operators_nb():
    output_str = out('pytest --nbval-lax random_operators.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~5 min; passed 2019/05/13
@pytest.mark.slow
def test_randomized_benchmarking_interleaved_nb():
    output_str = out('pytest --nbval-lax randomized_benchmarking_interleaved.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~14 sec
def test_randomized_benchmarking_simultaneous_nb():
    output_str = out('pytest --nbval-lax randomized_benchmarking_simultaneous.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~7 min; passed 2019/05/13
@pytest.mark.slow
def test_randomized_benchmarking_unitarity_nb():
    output_str = out('pytest --nbval-lax randomized_benchmarking_unitarity.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~3 sec
def test_readout_fidelity_nb():
    output_str = out('pytest --nbval-lax readout_fidelity.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~4 sec
def test_ripple_adder_benchmark_nb():
    output_str = out('pytest --nbval-lax ripple_adder_benchmark.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~40 sec; passed 2019/05/13
@pytest.mark.slow
def test_robust_phase_estimation_nb():
    output_str = out('pytest --nbval-lax robust_phase_estimation.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~10 sec
def test_state_and_process_plots_nb():
    output_str = out('pytest --nbval-lax state_and_process_plots.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# ~4 sec
def test_superoperator_tools_nb():
    output_str = out('pytest --nbval-lax superoperator_tools.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1

# Notebook fails at the moment
# def test_tomography_process_nb():
#     output_str = out('py.test --nbval-lax tomography_process.ipynb')
#     print(output_str)
#     assert output_str.find('failed') is -1

# ~4 sec
def test_tomography_state_nb():
    output_str = out('pytest --nbval-lax tomography_state.ipynb')
    print(output_str)
    assert output_str.find('failed') is -1