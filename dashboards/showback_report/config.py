import os

AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

AUTH0_DOMAIN = (os.getenv("AUTH0_DOMAIN") or "").strip().rstrip("/")

APP_ENV = os.getenv("APP_ENV")

AUTH_DISABLED = (os.getenv("AUTH_DISABLED") or "").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

APP_BASE_URL = os.getenv("APP_BASE_URL")

# Athena config

ATHENA_REGION = os.getenv("ATHENA_REGION")

ATHENA_ROLE = os.getenv("ATHENA_ROLE")

ATHENA_OUTPUT_LOCATION = os.getenv("ATHENA_OUTPUT_LOCATION")

ATHENA_WORKGROUP = os.getenv("ATHENA_WORKGROUP")
