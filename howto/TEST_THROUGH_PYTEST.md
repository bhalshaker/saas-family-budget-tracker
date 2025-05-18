# How to Run Tests with Pytest

After installing the required packages from `requirements.txt`, you can run tests using [pytest](https://docs.pytest.org/):

## Running All Tests

From the project main folder, run:
```bash
pytest
```

## Running Specific Test Files

To run a specific test file, for example `test_account.py`, use:
```bash
pytest test/test_account.py
```

## Configuring Pytest Output

- You can configure pytest output by editing the `pytest.ini` file in the main project folder.
- Test logs are saved in the `logs/` folder when debugging is activated.

## Generating an HTML Report

To generate an HTML report of the test results, run:
```bash
pytest --html=report.html --self-contained-html
```

You can then open `report.html` in your browser to view the results.
