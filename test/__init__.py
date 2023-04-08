import os
from test.utils import ensure_project_root

os.environ["FIREFLY_CLI_CONFIG"] = "test/test_data/firefly-cli-test.ini"

# Ensure tests are being run from root
ensure_project_root()
