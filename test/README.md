# ASE project CI (version 1.0)

## Tools involved
1. Chrome browser: all tests are based on the Chrome browser.
2. Chrome driver: help drive the Chrome pages.
3. Selenum 4: interacting with Chrome driver.
4. Pytest 8.3.3: provide module tests.
5. Allure: formate HTML report.
6. Jenkins: TBD

## Note for the tools
- You have to install Chrome and its driver manually
- Use version 130 and above is fine.

- Allure should be installed manually and its version
- should be above 2.32.0 version number.

## Testing types
- validation and function tests are supported.
- benchmark tests are not supported.

## Naming and annotation specifications
- File: test_<NUMBER>_<NAME>.py: <NUMBER> controls the test order,

## How to run test
- Test based on linux platforms using bash command: bash startup_selenium_tests.sh