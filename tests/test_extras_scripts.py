import os
import subprocess


def run_script(script: str) -> tuple[str, str, int]:
    print("Starting the test of the following script: ", script)
    result = subprocess.run(
        [script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode(), result.stderr.decode(), result.returncode


def test_run_dayabay_plot_all_nodes():
    stdout, stderr, code = run_script(
        "./scripts/fit_dayabay_dgm.sh",
    )

    assert code == 0
    assert stderr == ""
