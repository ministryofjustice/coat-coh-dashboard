import logging
import os
import secrets
from urllib.parse import quote_plus, urlencode

from authlib.integrations.requests_client import OAuth2Session

# -----------------------------
# Auth0 authentication
# -----------------------------

logger = logging.getLogger(__name__)

AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = (os.getenv("AUTH0_DOMAIN") or "").strip().rstrip("/")

# Optional local-development bypass:
# AUTH_DISABLED=true streamlit run app.py
AUTH_DISABLED = (os.getenv("AUTH_DISABLED") or "").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

AUTH0_SCOPE = "openid profile email"


def get_application_url() -> str:
    """Return the public URL used for the Auth0 callback.

    APP_BASE_URL should normally be injected by Helm, for example:

        https://coat-coh-dashboard-dev.cloud-platform.service.justice.gov.uk

    When APP_BASE_URL is not set, the URL is derived from forwarded headers.
    """
    configured_url = os.getenv("APP_BASE_URL")
    if configured_url:
        return configured_url.rstrip("/")

    try:
        headers = st.context.headers
        forwarded_proto = headers.get("X-Forwarded-Proto", "https")
        forwarded_host = headers.get("X-Forwarded-Host") or headers.get("Host")

        if forwarded_host:
            return f"{forwarded_proto.split(',')[0].strip()}://{forwarded_host}"
    except Exception:
        logger.exception("Unable to determine the application URL")

    # This fallback is useful for local development only.
    return "http://localhost:8501"


def get_auth0_redirect_uri() -> str:
    """Auth0 callback URL.

    Streamlit receives the OAuth callback on the application root and exposes
    the authorization code through st.query_params.
    """
    return f"{get_application_url()}/"


def validate_auth0_configuration() -> None:
    """Fail clearly if Auth0 configuration is incomplete."""
    missing = [
        name
        for name, value in {
            "AUTH0_CLIENT_ID": AUTH0_CLIENT_ID,
            "AUTH0_CLIENT_SECRET": AUTH0_CLIENT_SECRET,
            "AUTH0_DOMAIN": AUTH0_DOMAIN,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing required Auth0 configuration: " + ", ".join(missing)
        )


def create_auth0_session(state=None) -> OAuth2Session:
    return OAuth2Session(
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        scope=AUTH0_SCOPE,
        redirect_uri=get_auth0_redirect_uri(),
        state=state,
    )


def create_auth0_login_url() -> str:
    validate_auth0_configuration()

    oauth = create_auth0_session()

    authorization_url, state = oauth.create_authorization_url(
        f"https://{AUTH0_DOMAIN}/authorize",
        nonce=secrets.token_urlsafe(32),
    )

    # Store the state server-side to protect against CSRF.
    st.session_state["auth0_state"] = state

    return authorization_url


def exchange_auth0_code(code: str, returned_state: str | None) -> None:
    """Exchange the authorization code and load the authenticated user."""
    expected_state = st.session_state.pop("auth0_state", None)

    if not expected_state or not returned_state:
        raise ValueError("Missing Auth0 OAuth state")

    if not secrets.compare_digest(expected_state, returned_state):
        raise ValueError("Invalid Auth0 OAuth state")

    oauth = create_auth0_session(state=expected_state)

    token = oauth.fetch_token(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        code=code,
        grant_type="authorization_code",
        redirect_uri=get_auth0_redirect_uri(),
    )

    userinfo_response = oauth.get(f"https://{AUTH0_DOMAIN}/userinfo")
    userinfo_response.raise_for_status()

    st.session_state["auth0_user"] = userinfo_response.json()
    st.session_state["auth0_token"] = token


def process_auth0_callback() -> None:
    """Process the Auth0 callback query parameters once."""
    code = st.query_params.get("code")
    returned_state = st.query_params.get("state")
    error = st.query_params.get("error")

    if error:
        error_description = st.query_params.get(
            "error_description",
            "Auth0 authentication failed.",
        )
        st.query_params.clear()
        raise RuntimeError(f"{error}: {error_description}")

    if not code:
        return

    try:
        exchange_auth0_code(code, returned_state)
    except Exception:
        logger.exception("Auth0 callback failed")
        st.query_params.clear()
        raise RuntimeError("Unable to complete Auth0 login.") from None

    # Remove code and state from the browser URL after successful login.
    st.query_params.clear()


def get_auth0_logout_url() -> str:
    validate_auth0_configuration()

    query_parameters = urlencode(
        {
            "client_id": AUTH0_CLIENT_ID,
            "returnTo": get_application_url(),
        },
        quote_via=quote_plus,
    )

    return f"https://{AUTH0_DOMAIN}/v2/logout?{query_parameters}"


def require_auth0_login() -> None:
    """Require a valid Auth0 login before rendering the dashboard."""
    if AUTH_DISABLED:
        return

    validate_auth0_configuration()
    process_auth0_callback()

    if "auth0_user" not in st.session_state:
        st.title("AWS Cost Optimization Hub Dashboard")
        st.info("Please log in to continue.")
        st.link_button(
            "Log in with Auth0",
            create_auth0_login_url(),
            type="primary",
        )
        st.stop()

    userinfo = st.session_state["auth0_user"]

    with st.sidebar:
        display_name = (
            userinfo.get("name")
            or userinfo.get("email")
            or userinfo.get("nickname")
            or "Authenticated user"
        )

        st.caption(f"Signed in as **{display_name}**")
        st.link_button("Log out", get_auth0_logout_url())

        if st.button("Clear local session", key="clear_auth0_session"):
            st.session_state.pop("auth0_user", None)
            st.session_state.pop("auth0_token", None)
            st.rerun()