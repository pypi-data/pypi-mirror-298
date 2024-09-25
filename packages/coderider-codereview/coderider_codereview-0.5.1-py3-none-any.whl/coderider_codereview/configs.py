import json
import os

from decouple import config, UndefinedValueError

from coderider_codereview.exceptions import ConfigError

CR_DEBUG = config("CR_DEBUG", default=False, cast=bool)
LITELLM_LOG = config("LITELLM_LOG", default=None)
if CR_DEBUG and not LITELLM_LOG:
    os.environ["LITELLM_LOG"] = "DEBUG"

### CodeRider Server ###

CR_SERVER_HOST = config("CR_SERVER_HOST", default="https://coderider.jihulab.com")
try:
    CR_AI_BOT_TOKEN = config("CR_AI_BOT_TOKEN")
except UndefinedValueError:
    raise ConfigError("CR_AI_BOT_TOKEN")

### MR ###

CR_GITLAB_HOST = config("CR_GITLAB_HOST", config("CI_SERVER_URL", default="https://jihulab.com"))

try:
    CR_MR_PROJECT_PATH = config("CR_MR_PROJECT_PATH", default=None) or config("CI_MERGE_REQUEST_PROJECT_PATH")
except UndefinedValueError:
    raise ConfigError("CR_MR_PROJECT_PATH")

try:
    CR_MR_IID = config("CR_MR_IID", default=None) or config("CI_MERGE_REQUEST_IID")
except UndefinedValueError:
    raise ConfigError("CR_MR_IID")

### LLM ###

CR_LLM_MODEL = config("CR_LLM_MODEL", default="coderider/maas-chat-model")
CR_LLM_API_KEY = config("CR_LLM_API_KEY", default=None)
CR_LLM_BASEURL = config("CR_LLM_BASEURL", default=None)
CR_LLM_OPTIONS = config("CR_LLM_OPTIONS", default="{}", cast=lambda v: json.loads(v))
CR_LLM_TIMEOUT = config("CR_LLM_TIMEOUT", default=60 * 5, cast=int)

### Features ###
CR_ARTIFACT_SAST_REPORT_FILE_PATH = config(
    "CR_ARTIFACT_SAST_REPORT_FILE_PATH",
    default="gl-sast-report.json"
)
CR_ARTIFACT_SECRET_DETECTION_REPORT_FILE_PATH = config(
    "CR_ARTIFACT_SECRET_DETECTION_REPORT_FILE_PATH",
    default="gl-secret-detection-report.json"
)
