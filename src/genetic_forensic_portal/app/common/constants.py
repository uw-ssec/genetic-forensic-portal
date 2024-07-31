"""Contains constants used throughout the application.

Types of constants found in this module:
- Authentication session state keys
- Sample, canned analysis \"UUID\"s used for testing
"""

# Authentication

AUTHENTICATED = "authenticated"
USERNAME = "username"
ROLES = "roles"
TOKEN = "token"


# Analyses

SAMPLE_UUID = "this-is-a-uuid"
NO_METADATA_UUID = "this-is-a-differentuuid"
NOT_FOUND_UUID = "not-found-uuid"
NOT_AUTHORIZED_UUID = "not-authorized-uuid"
IN_PROGRESS_UUID = "in-progress-uuid"
ANALYSIS_FAILED_UUID = "failed-uuid"
FAMILIAL_FILE_PARSE_ERROR_UUID = "familial-parse-error-uuid"
