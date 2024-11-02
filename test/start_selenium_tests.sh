# this is the start up script of Pytest on Linux platforms

# pytest --cache-clear will not remove the cache folder
pytest --verbose --cache-clear -m "not dangerous" --alluredir=allure_report

# manually remove cache files, --cache-clear option does not delete folder
[ -d "./__pycache__" ] && rm -rf ./__pycache__
[ -d "./.pytest_cache" ] && rm -rf ./.pytest_cache

[ -d "./testcase/__pycache__" ] && rm -rf ./testcase/__pycache__
[ -d "./testcase/utils/__pycache__" ] && rm -rf ./testcase/utils/__pycache__
[ -d "./testcase/nqueens/__pycache__" ] && rm -rf ./testcase/nqueens/__pycache__
[ -d "./testcase/polysphere/__pycache__" ] && rm -rf ./testcase/polysphere/__pycache__

# call the allure report display menu
allure serve allure_report
