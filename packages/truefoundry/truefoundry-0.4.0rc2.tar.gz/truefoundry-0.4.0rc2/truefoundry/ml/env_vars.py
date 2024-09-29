"""
Define all the env variable names that users
can use
"""

# NOTE: These are shared between servicefoundry and mlfoundry
TRACKING_HOST_GLOBAL = "TFY_HOST"
API_KEY_GLOBAL = "TFY_API_KEY"
DISABLE_MULTIPART_UPLOAD = "MLF_DISABLE_MULTIPART_UPLOAD"
INTERNAL_ENV_VARS = [
    "TFY_INTERNAL_APPLICATION_ID",
    "TFY_INTERNAL_JOB_RUN_NAME",
]
