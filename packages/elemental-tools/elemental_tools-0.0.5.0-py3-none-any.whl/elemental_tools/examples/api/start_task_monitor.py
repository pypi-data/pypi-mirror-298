import os

from elemental_tools.system import LoadEnvironmentFile
from elemental_tools.task_monitor import Monitor
from elemental_tools.pydantic import generate_pydantic_model_from_path
from elemental_tools.scripts import internal_scripts

LoadEnvironmentFile.validate()

# load integration scripts
scripts_root_path = os.environ.get('SCRIPTS_ROOT', 'scripts')

# generate pydantic models from the scripts path
script_pydantic_models = generate_pydantic_model_from_path(scripts_root_path)

# run only task monitor
task_monitor = Monitor(script_pydantic_models, internal_scripts)
task_monitor.run()
