import base64
from dataclasses import dataclass
import os
import time
from typing import TYPE_CHECKING, Any
import uuid
import streamlit as st
import vizkit.pipeline.data_source.firebase.user as user_utils
import json
from vizkit import Options
import streamlit_js_eval as js

if TYPE_CHECKING:
    from streamlit_oauth import OAuth2Component


_SESSION_ID_KEY = "vizkit.session-id"


@dataclass
class AuthUser:
    _uid: str | None
    token: Any

    @property
    def uid(self) -> str:
        assert self._uid is not None
        return self._uid

    def id_token(self) -> Any:
        id_token = self.token["id_token"]
        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        return payload

    @property
    def name(self) -> str | None:
        id_token = self.id_token()
        return id_token.get("name")

    @property
    def email(self) -> str | None:
        id_token = self.id_token()
        return id_token.get("email")

    @property
    def avatar(self) -> str | None:
        id_token = self.id_token()
        return id_token.get("picture")


def get_user(refresh=False) -> AuthUser | None:
    # st.write(f"session_id: {sid}")
    if "auth" in st.session_state:
        uid = st.session_state["auth"]["uid"]
        token = st.session_state["auth"]["token"]
        return AuthUser(_uid=uid, token=token)
    sid = st.context.cookies.get(_SESSION_ID_KEY)
    if not sid or sid == "":
        return None
    payload = user_utils.get_user_auth_info(sid)
    if payload is None:
        return None
    # try refresh token
    if refresh:
        oauth2 = _GoogleOAuth2Client.get()
        try:
            oauth2.refresh_token(sid, payload["uid"], payload["token"])
        except Exception as e:
            return None
    st.session_state["auth"] = {"uid": payload["uid"], "token": payload["token"]}
    st.session_state.pop("user_data_files", None)
    return AuthUser(_uid=payload["uid"], token=payload["token"])


def logout():
    sid = st.context.cookies.get(_SESSION_ID_KEY)
    if not sid or sid == "":
        return
    js.set_cookie(_SESSION_ID_KEY, "", -1)
    user_utils.delete_user_auth_info(sid)
    del st.session_state["auth"]
    st.session_state.pop("user_data_files", None)
    st.rerun()


@st.dialog("Login")  # type: ignore
def __login_dialog():
    oauth2 = _GoogleOAuth2Client.get()
    token = oauth2.login_button(
        title="Login with Google",
        icon="https://google.com/favicon.ico",
        scope="openid email profile",
    )
    if token:
        with st.spinner("Loading ..."):
            user = AuthUser(_uid="", token=token)
            session_id = str(uuid.uuid4())
            js.set_cookie(
                _SESSION_ID_KEY, session_id, 7, component_key=str(uuid.uuid4())
            )
            uid = user_utils.get_or_create_user(
                email=user.email or "", name=user.name or "", avatar=user.avatar or ""
            )
            user_utils.set_user_auth_info(session_id, uid, token)
            st.session_state["auth"] = {"uid": uid, "token": token}
            st.rerun()


def google_login_button(title: str):
    if st.button(title, use_container_width=True):
        __login_dialog()


class _GoogleOAuth2Client:
    def __init__(self, client: "OAuth2Component"):
        self.__client = client

    def refresh_token(self, key: str, uid: str, token: Any):
        new_token = self.__client.refresh_token(token=token)
        user_utils.set_user_auth_info(key, uid, new_token)

    def login_button(self, title: str, icon: str | None, scope: str) -> Any | None:
        result = self.__client.authorize_button(
            name=title,
            icon=icon,
            redirect_uri=f"{Options.get().domain}/component/streamlit_oauth.authorize_button/index.html",
            scope=scope,
            # key=self.kind,
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=True,
            pkce="S256",
        )
        if result is not None:
            if token := result.get("token"):
                return json.loads(json.dumps(token))
        return None

    @staticmethod
    def get() -> "_GoogleOAuth2Client":
        from streamlit_oauth import OAuth2Component

        client = OAuth2Component(
            client_id=os.environ["GOOGLE_AUTH_CLIENT_ID"],
            client_secret=os.environ["GOOGLE_AUTH_CLIENT_SECRET"],
            authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
            token_endpoint="https://oauth2.googleapis.com/token",
            refresh_token_endpoint="https://oauth2.googleapis.com/token",
            revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
        )
        return _GoogleOAuth2Client(client=client)
