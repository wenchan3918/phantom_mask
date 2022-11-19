import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_PERMISSIONS = lambda user: user.is_superuser
# clean up using cron job
# SILKY_MAX_RECORDED_REQUESTS = 10 ** 4
# SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 50
SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
SILKY_META = True
SILKY_INTERCEPT_PERCENT = 50  # log only 50% of requests
SILKY_MAX_RECORDED_REQUESTS = 10 ** 4
SILKY_ANALYZE_QUERIES = True
SILKY_EXPLAIN_FLAGS = {'format': 'JSON', 'costs': True}

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, 'silky_logs')
# print("=SILKY_PYTHON_PROFILER_RESULT_PATH\n", SILKY_PYTHON_PROFILER_RESULT_PATH)
