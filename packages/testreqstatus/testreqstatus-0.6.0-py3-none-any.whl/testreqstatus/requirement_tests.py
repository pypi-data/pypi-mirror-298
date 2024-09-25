from pathlib import Path
import re
import json
from collections.abc import MutableMapping


class RequirementTests(MutableMapping):
    """
    mapping of requirements to individual tests
    """

    def __init__(self, requirements: dict[str, list[str]]):
        self.requirements = requirements

    @classmethod
    def from_file(cls, filename: Path | str) -> "RequirementTests":
        """
        :param filename: JSON file mapping requirements to individual tests
        """

        with open(filename) as file:
            requirements = json.load(file)
        return cls(requirements)

    @classmethod
    def from_test_directory(cls, directory: Path) -> "RequirementTests":
        """
        extract requirements (decorated as `@metrics_logger("DMS408")`) from tests in the given directory

        :param directory: directory containing `pytest` tests decorated with `@metrics_logger`
        """

        if not isinstance(directory, Path):
            directory = Path(directory)

        directory = directory.expanduser()

        requirements: dict[str, list[str]] = {}
        for test_filename in directory.glob("**/test_*.py"):
            with open(test_filename) as test_file:
                test_file_contents = test_file.read()

            for match in re.finditer(
                r'@metrics_logger\(("DMS.+")\)[\S\s]*?def ([^\(]+)\(.*\):',
                test_file_contents,
            ):
                test_module = f"{str(test_filename.parent.relative_to(directory)).replace('/', '.')}.{test_filename.stem}"
                test_name = f"{match.group(2)}"
                for requirement in (
                    requirement.strip('" ') for requirement in match.group(1).split(",")
                ):
                    if requirement not in requirements:
                        requirements[requirement] = []
                    requirements[requirement].append(f"{test_module}.{test_name}")

        return cls(requirements)

    def test_requirements(self, test: str) -> list[str]:
        """
        get requirements corresponding to the given test
        """

        return [
            requirement
            for requirement, tests in self.items()
            if any(existing_test in test for existing_test in tests)
        ]

    def __getitem__(self, requirement: str) -> list[str]:
        return self.requirements[requirement]

    def __setitem__(self, requirement: str, tests: list[str]):
        self.requirements[requirement] = tests

    def __delitem__(self, requirement: str):
        del self.requirements[requirement]

    def __iter__(self):
        return iter(self.requirements)

    def __len__(self) -> int:
        return len(self.requirements)

    def __str__(self) -> str:
        return str(self.requirements)

    def to_file(self, filename: Path, indent: str = "  "):
        with open(filename, "w") as file:
            json.dump(self.requirements, file, indent=indent)
