# ASE project CI (version 0.1)

## Technologies used

1. Selenum 4: interacting with Chrome driver, working on Chrome pages.
2. Pytest 8.3.3: Module test organizer, also gives reports.
3. Jenkins: TBD

## Testing method

- From top to buttom.
- First validation then function.

## Naming and annotation specifications

- File: test_<NUMBER>_<NAME>_<NAME>.py: <NUMBER> controls the test order,
- <NAME>_<NAME> to help tester distinguish the targets.

- Test cases: See pytest.ini for more information

## How to run test

- On linux platforms using: bash startup_test.sh
- On Windows platforms using: TBD