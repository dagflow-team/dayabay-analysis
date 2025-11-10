import subprocess


def _run_script(script: str) -> tuple[str, str, int]:
    print("Starting the test of the following script: ", script)
    result = subprocess.run(
        [script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout = result.stdout.decode()
    stderr = result.stderr.decode()

    if result.returncode != 0:
        print()
        print("stdout:")
        print(stdout, end="\n\n")
        print("stderr:")
        print(stderr, end="\n\n")
        print("Failed command:")
        print(script, end="\n\n")

    assert result.returncode == 0

    return (stdout, stderr, result.returncode)


def test_run_dayabay_plot_all_nodes():
    stdout, stderr, code = _run_script(
        "./scripts/fit_dayabay_dgm.sh",
    )

    assert code == 0
    assert stderr == ""
