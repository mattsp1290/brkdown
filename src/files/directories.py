import os
from pathlib import Path

from ..config.config import Config


def get_or_create_base(output_path):
    base_name = os.path.basename(Config().get_value("CURRENT_DIRECTORY"))
    output_base = f"{output_path}/{base_name}"

    if not os.path.exists(output_base):
        os.makedirs(output_base)

    return output_base
    

    