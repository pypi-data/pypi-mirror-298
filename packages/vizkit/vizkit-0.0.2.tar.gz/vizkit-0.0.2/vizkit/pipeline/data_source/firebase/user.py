from firebase_admin import auth as fb_auth
from firebase_admin._auth_utils import UserNotFoundError
from google.cloud.firestore_v1 import DocumentSnapshot
from vizkit.pipeline.data_source.firebase import app as fb_app
import streamlit as st

_STORE = fb_app.get_store()


def __get_user_name_cache() -> dict[str, str]:
    return st.session_state.setdefault("user_name_cache", {})


def get_user_name_by_uid(uid: str) -> str:
    cache = __get_user_name_cache()
    if uid in cache:
        return cache[uid]
    try:
        user = fb_auth.get_user(uid=uid)
        cache[uid] = user.display_name
    except UserNotFoundError:
        user = None
    return user.display_name if user else "<unknown>"


def get_or_create_user(email: str, name: str, avatar: str) -> str:
    try:
        user = fb_auth.get_user_by_email(email)
    except UserNotFoundError:
        user = None
    if not user:
        user = fb_auth.create_user(
            email=email, display_name=name, email_verified=True, photo_url=avatar
        )
    doc: DocumentSnapshot = _STORE.document("users", user.uid).get()
    if not doc.exists:
        _STORE.document("users", user.uid).set({"uid": user.uid})
    return user.uid


def get_user_auth_info(key: str) -> dict | None:
    doc = _STORE.document("auth-cache", key).get()
    if not doc.exists:
        return None
    return doc.to_dict()


def set_user_auth_info(key: str, uid: str, token: dict):
    _STORE.document("auth-cache", key).set({"uid": uid, "token": token})


def delete_user_auth_info(key: str):
    _STORE.document("auth-cache", key).delete()
