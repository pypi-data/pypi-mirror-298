import os
from elemental_tools.system import LoadEnvironmentFile
from elemental_tools import API
from elemental_tools.pydantic import generate_pydantic_model_from_path
from elemental_tools.scripts import internal_scripts
from elemental_tools.api.config import app_name, host, port

LoadEnvironmentFile.validate()
scripts_root_path = os.environ.get('SCRIPTS_ROOT', 'scripts')

# generate pydantic models from the scripts path
script_pydantic_models = generate_pydantic_model_from_path(scripts_root_path)

# start the scriptize api
api = API(script_pydantic_models, internal_scripts, app_name=app_name, host=host, port=port)
api.run()
