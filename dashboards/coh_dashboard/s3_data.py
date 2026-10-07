import io
import os
from urllib.parse import urlparse

import boto3
import streamlit as st


def get_csv_s3_uri() -> str:
    """Return the configured S3 URI for the dashboard CSV."""
    return os.getenv("COH_REPORT_S3_URI")

def parse_s3_uri(s3_uri: str) -> tuple[str, str]:
    """Parse an s3://bucket/key URI into its bucket and object key."""
    parsed_uri = urlparse(s3_uri)

    if parsed_uri.scheme != "s3" or not parsed_uri.netloc or not parsed_uri.path:
        raise ValueError(
            f"Invalid S3 URI: {s3_uri!r}. "
            "Expected a URI in the form s3://bucket/key."
        )

    return parsed_uri.netloc, parsed_uri.path.lstrip("/")

@st.cache_data(ttl=300)
def download_csv_from_s3(s3_uri: str | None = None) -> io.BytesIO:
    """Download a CSV object from S3 and return it as a file-like object.

    boto3 uses the pod's AWS credential chain. In EKS this should normally be
    provided through the IAM role associated with the Kubernetes service account.
    """
    uri = s3_uri or get_csv_s3_uri()
    bucket, key = parse_s3_uri(uri)

    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket, Key=key)

    return io.BytesIO(response["Body"].read())