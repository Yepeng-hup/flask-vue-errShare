import os
import sys

from core.svclog import svc_log_err

def check_file() -> str:
    yaml_file_path = "errshare.yaml"
    if os.path.exists(yaml_file_path):
        return yaml_file_path
    else:
        svc_log_err(f"not is file [{yaml_file_path}]")
        sys.exit(1)
