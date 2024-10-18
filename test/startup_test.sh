# This is the start up script of Pytest on Linux platforms

# Actually running command
pytest --verbose --cache-clear

# Manually remove cache files, --cache-clear option does not delete folder
[ -d "./__pycache__" ] && rm -rf ./__pycache__
[ -d "./.pytest_cache" ] && rm -rf ./.pytest_cache
[ -d "./testcase/__pycache__" ] && rm -rf ./testcase/__pycache__
[ -d "./testcase/nqueens/__pycache__" ] && rm -rf ./testcase/nqueens/__pycache__