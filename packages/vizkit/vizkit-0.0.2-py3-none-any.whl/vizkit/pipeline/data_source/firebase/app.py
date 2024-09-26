import json, os, base64
from pathlib import Path
from firebase_admin import credentials, storage, firestore
import firebase_admin
import streamlit as st

__SERVICE_ACCOUNT_KEY_FILE = (
    Path(__file__).parent.parent.parent.parent.parent / "serviceAccountKey.json"
)

if __SERVICE_ACCOUNT_KEY_FILE.exists():
    with open(__SERVICE_ACCOUNT_KEY_FILE, "r") as f:
        cert = json.load(f)
    cred = credentials.Certificate(cert)
else:
    # Load from env-var
    if key_base64 := os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_BASE64"):
        cert_str = base64.b64decode(key_base64).decode("utf-8")
        cert = json.loads(cert_str)
        cred = credentials.Certificate(cert)
    else:
        raise FileNotFoundError(
            f"Service account key file not found: {__SERVICE_ACCOUNT_KEY_FILE.absolute()}"
        )


def __get_default_bucket_name():
    if bucket := os.environ.get("FIRESBASE_STORAGE_BUCKET"):
        if not bucket.startswith("gs://") or not bucket.endswith(".appspot.com"):
            raise ValueError(f"Invalid bucket name: {bucket}")
        bocket_url = f"{bucket}.appspot.com"
    project_id = cert["project_id"]
    bocket_url = f"gs://{project_id}.appspot.com"
    return bocket_url.removeprefix("gs://")


_DEFAULT_BUCKET_NAME = __get_default_bucket_name()


def get_app():
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()


def create_bucket():
    get_app()
    return storage.bucket(name=_DEFAULT_BUCKET_NAME)


def create_client():
    get_app()
    return firestore.client()


@st.cache_resource
def get_bucket():
    get_app()
    return storage.bucket(name=_DEFAULT_BUCKET_NAME)


@st.cache_resource
def get_store():
    get_app()
    return firestore.client()
