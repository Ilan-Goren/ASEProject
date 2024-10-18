import pytest
import shutil
import os

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    # After tests done, remove cache folder
    cache_dir = ".pytest_cache"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)