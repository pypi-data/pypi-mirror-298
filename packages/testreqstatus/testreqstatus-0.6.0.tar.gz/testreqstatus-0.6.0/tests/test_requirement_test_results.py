from pathlib import Path
from junitparser import JUnitXml

import json
import pytest

from testreqstatus import RequirementTestResults, RequirementTests

DATA_DIRECTORY = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    "test_requirements_filename,test_results_filename,reference_test_results_by_requirements_filename",
    [
        (
            DATA_DIRECTORY / "input" / "romancal_test_requirements.json",
            DATA_DIRECTORY / "input" / "results-Linux-x64-py3.11.xml",
            DATA_DIRECTORY
            / "output"
            / "romancal_requirements_status-Linux-x64-py3.11.json",
        ),
        (
            DATA_DIRECTORY / "input" / "romancal_test_requirements.json",
            DATA_DIRECTORY / "input" / "results-macOS-x86-py3.11.xml",
            DATA_DIRECTORY
            / "output"
            / "romancal_requirements_status-macOS-x86-py3.11.json",
        ),
        (
            DATA_DIRECTORY / "input" / "romancal_test_requirements.json",
            DATA_DIRECTORY / "input" / "results-macOS-ARM64-py3.11.xml",
            DATA_DIRECTORY
            / "output"
            / "romancal_requirements_status-macOS-ARM64-py3.11.json",
        ),
        (
            DATA_DIRECTORY / "input" / "romancal" / "dms_requirement_tests.json",
            DATA_DIRECTORY / "input" / "romancal" / "pytest_results.xml",
            DATA_DIRECTORY / "output" / "romancal" / "requirements_status.json",
        ),
        (
            DATA_DIRECTORY / "input" / "romanisim" / "dms_requirement_tests.json",
            DATA_DIRECTORY / "input" / "romanisim" / "pytest_results.xml",
            DATA_DIRECTORY
            / "output"
            / "romanisim"
            / "romanisim_requirements_status.json",
        ),
        (
            DATA_DIRECTORY / "input" / "crds" / "dms_requirement_tests.json",
            DATA_DIRECTORY / "input" / "crds" / "client_results.xml",
            DATA_DIRECTORY / "output" / "crds" / "crds_requirements_status.json",
        ),
    ],
)
def test_requirement_test_results(
    test_requirements_filename,
    test_results_filename,
    reference_test_results_by_requirements_filename,
):
    requirement_test_results = RequirementTestResults(
        RequirementTests.from_file(test_requirements_filename),
        JUnitXml.fromfile(test_results_filename),
    )

    with open(reference_test_results_by_requirements_filename) as reference_file:
        reference_test_results_by_requirement = json.load(reference_file)

    assert (
        requirement_test_results.test_results_by_requirement
        == reference_test_results_by_requirement
    )
