import os

if ENV := bool(os.environ.get("ENV", False)):
    from heroku_config import Var as Config
else:
    from sample_config import Development as Config


Var = Config
