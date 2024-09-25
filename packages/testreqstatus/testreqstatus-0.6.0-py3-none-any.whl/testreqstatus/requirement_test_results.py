import functools
import json
from pathlib import Path

from junitparser import JUnitXml

from testreqstatus.requirement_tests import RequirementTests


class RequirementTestResults:
    """
    specified requirements' test results
    """

    def __init__(
        self,
        test_requirements: dict[str, list[str]] | RequirementTests,
        test_results: str | JUnitXml,
    ):
        """
        parse test results and output status of requirements

        :param test_requirements: mapping of requirements to individual tests
        :param test_results: JUnit XML of test results
        """

        if isinstance(test_requirements, dict):
            test_requirements = RequirementTests(test_requirements)

        if isinstance(test_results, str):
            test_results = JUnitXml.fromstring(test_results)

        self.requirements = test_requirements
        self.results = test_results

    @property
    @functools.lru_cache(maxsize=None)
    def test_results_by_requirement(self) -> dict[str, dict[str, str]]:
        """
        mapping of tests (with result) to requirements
        """

        test_results_by_requirement: dict[str, dict[str, str]] = {
            requirement: {} for requirement in self.requirements
        }
        for suite in self.results:
            for case in suite:
                test = f"{case.classname}.{case.name}"
                for requirement in self.requirements.test_requirements(test):
                    test_results_by_requirement[requirement][test] = (
                        "PASS"
                        if case.is_passed
                        else "SKIP"
                        if case.is_skipped
                        else "FAIL"
                    )

        return test_results_by_requirement

    @property
    @functools.lru_cache(maxsize=None)
    def requirements_by_test_result(self):
        test_results_by_requirement = self.test_results_by_requirement

        requirements_by_test_result = {}
        for requirement, test_results in test_results_by_requirement.items():
            for test, result in test_results.items():
                if test not in requirements_by_test_result:
                    requirements_by_test_result[test] = {
                        "status": result,
                        "requirements": [],
                    }
                requirements_by_test_result[test]["requirements"].append(requirement)

        return requirements_by_test_result
