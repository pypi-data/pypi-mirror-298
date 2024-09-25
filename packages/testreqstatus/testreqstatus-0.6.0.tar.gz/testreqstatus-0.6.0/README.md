# testreqstatus

[![PyPI - Version](https://img.shields.io/pypi/v/testreqstatus.svg)](https://pypi.org/project/testreqstatus)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/testreqstatus.svg)](https://pypi.org/project/testreqstatus)

-----

```console
pip install testreqstatus
```

## Usage

1. Establish a set of requirements corresponding to test names:

    ```json
    {
      "DMS356": [
        "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline"
      ],
      "DMS373": [
        "romancal.regtest.test_mos_pipeline.test_hlp_mosaic_pipeline"
      ],
      "DMS374": [
        "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline"
      ],
      "DMS400": [
        "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline"
      ]
    }
    ```

> [!TIP]
> To extract test requirements from existing tests 
> decorated with `@metrics_logger`, use `RequirementTests.from_test_directory()`:
> ```python
> from testreqstatus import RequirementTests
> 
> requirements = RequirementTests.from_test_directory("~/projects/romancal/")
> requirements.to_file("test_requirements.json")
> ``` 

2. Run tests and generate a JUnitXML results file:

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <testsuites>
      <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="2" time="2021.550" timestamp="2024-08-23T00:23:01.454354" hostname="spacetelescope-runner-2ls89-rrbf2">
        <testcase classname="romancal.regtest.test_mos_pipeline" name="test_level3_mos_pipeline" time="677.728">
        </testcase>
        <testcase classname="romancal.regtest.test_mos_pipeline" name="test_hlp_mosaic_pipeline" time="486.642">
        </testcase>
      </testsuite>
    </testsuites>
    ```

3. Use `RequirementTestResults.requirements_by_test_result` to retrieve the status of each test and its corresponding requirements:

    ```python
    from testreqstatus import RequirementTestResults

    results = RequirementTestResults(
        test_requirements="examples/test_requirements.json",
        test_results="examples/results.xml",
    )

    print(results.requirements_by_test_result)
    ```
    ```json
    {
      "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline": {
        "status": "PASS",
        "requirements": [
          "DMS356",
          "DMS374",
          "DMS400"
        ]
      },
      "romancal.regtest.test_mos_pipeline.test_hlp_mosaic_pipeline": {
        "status": "PASS",
        "requirements": [
          "DMS373"
        ]
      }
    }
    ```

> [!TIP]
> You can alternatively use `RequirementTestResults.test_results_by_requirement` to obtain the inverse mapping (requirements and their corresponding test statuses):
> ```python
> print(results.test_results_by_requirement)
> ```
> ```json
> {
>   "DMS356": {
>     "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline": "PASS"
>   },
>   "DMS373": {
>     "romancal.regtest.test_mos_pipeline.test_hlp_mosaic_pipeline": "PASS"
>   },
>   "DMS374": {
>     "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline": "PASS"
>   },
>   "DMS400": {
>     "romancal.regtest.test_mos_pipeline.test_level3_mos_pipeline": "PASS"
>   }
> }
> ```
