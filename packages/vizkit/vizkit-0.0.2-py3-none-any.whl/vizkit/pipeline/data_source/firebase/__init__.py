from dataclasses import dataclass
from typing import TYPE_CHECKING
import streamlit as st

from vizkit.pipeline.data_source.firebase import user as user_utils
from vizkit.pipeline.data_source.firebase import db
from .. import DataSource, DataFiles, DataFile, DataFileMeta
from . import auth


if TYPE_CHECKING:
    from .. import Pipeline


@dataclass
class ProjectName:
    user: str | None
    project: str


class FirebaseDataSource(DataSource):
    @property
    def is_local(self) -> bool:
        return False

    def __init__(self) -> None:
        super().__init__()

    def get_inflated_link(self, key: str) -> str | None:
        return db.get_inflated_id(key)

    def insert_inflated_link(self, inflated: str) -> str:
        return db.insert_inflated_id(inflated, self._generate_share_link_key)

    def list_user_data_files_for_project(
        self, project: str
    ) -> list[DataFileMeta] | None:
        if user := auth.get_user():
            return db.get_owned_project_files(user.uid, project)
        else:
            return None

    def get_data_file_meta(self, id: str) -> DataFileMeta:
        return db.get_file_meta(id)

    def load_data_file(self, id: str) -> DataFile:
        return db.get_file(id)

    def __get_owner_info(self, meta: DataFileMeta | None) -> str | None:
        if meta and meta.owner is not None:
            owner_info = f"Owner: {user_utils.get_user_name_by_uid(meta.owner)}"
            user = auth.get_user()
            if user and user.uid == meta.owner:
                owner_info += " (You)"
            return owner_info
        elif meta:
            return "This data file is not owned by anyone"
        else:
            return None

    def __get_projects(self, curr_file: DataFileMeta | None) -> list[ProjectName]:
        projects = []
        user = auth.get_user()
        # Load all projects owned by the user
        if user:
            for p in db.get_projects(user.uid):
                projects.append(ProjectName(None, p))
        if curr_file:
            # current file is owned by the user, but not in the list of projects
            if (
                user
                and curr_file.owner == user.uid
                and curr_file.project not in projects
            ):
                projects.append(ProjectName(None, curr_file.project))
            # current file is not owned by the user
            if not user or curr_file.owner != user.uid:
                projects.append(ProjectName(curr_file.owner, curr_file.project))
        return projects

    def __get_files_for_project(
        self,
        project: str | None,
        data_files: DataFiles,
        selected: DataFileMeta | None,
    ) -> list[DataFileMeta]:
        if not project:
            return []
        files: list[DataFileMeta] = []
        # Add all files in the project
        for m in data_files.projects.get(project, []):
            files.append(m)
        # Add the unclaimed data file
        user = auth.get_user()
        uid = user.uid if user else None
        if selected and (
            not selected.owner or (selected.owner != uid and selected not in files)
        ):
            files.append(selected)
        return files

    def render_data_source_block(self, pipeline: "Pipeline", initial_inputs: list[str]):
        user = auth.get_user()
        curr_data_file = (
            self.get_data_file_meta(pipeline.inputs[0])
            if len(pipeline.inputs) > 0
            else None
        )
        curr_data_file_is_claimed = curr_data_file and curr_data_file.owner is not None
        with st.sidebar:
            owner_info = self.__get_owner_info(curr_data_file)
            # 1. Project selector
            init_file = (
                self.get_data_file_meta(initial_inputs[0])
                if len(initial_inputs) > 0
                else None
            )
            projects = self.__get_projects(curr_data_file)
            init_proj = None
            if user and init_file and user.uid == init_file.owner:
                init_proj = ProjectName(None, init_file.project)
            elif init_file:
                init_proj = ProjectName(init_file.owner, init_file.project)
            init_index = projects.index(init_proj) if init_proj in projects else None
            project = st.selectbox(
                "Project",
                projects,
                format_func=lambda x: x.project,
                index=init_index,
                help=owner_info,
                key=f"project",
            )
            pipeline.project = project.project if project else None
            # 2. Data file selector
            data_files = (
                db.get_owned_project_files(user.uid, project.project)
                if user and project
                else []
            )
            if init_file and (not user or init_file.owner != user.uid):
                data_files.append(init_file)
            init_runid = init_file.runid if init_file else None
            init_index = None
            for i, x in enumerate(data_files):
                if x.runid == init_runid:
                    init_index = i
                    break
            selected = st.selectbox(
                "Data Source",
                data_files,
                index=init_index,
                format_func=lambda x: x.runid,
                help=owner_info,
                key=f"data-source",
            )
            if selected:
                assert selected.sha256
                pipeline.inputs = [selected.sha256]
            # Claim and Login buttons
            if curr_data_file:
                if curr_data_file.owner is not None:
                    if user is None:
                        auth.google_login_button("🔒 Login to share pipeline")
                else:
                    if user is not None:
                        if st.button("✅ Claim Ownership", use_container_width=True):
                            db.claim_file(pipeline.inputs[0], user.uid)
                            st.rerun()
                    else:
                        auth.google_login_button("🔒 Login to claim ownership")
            else:
                if user is None:
                    auth.google_login_button("🔒 Login to get your pipelines")

            # Share button
            if curr_data_file_is_claimed and user is not None:
                self._render_share_button(pipeline)

            # Logout button
            if user is not None:
                if st.button("⎋ Logout", use_container_width=True):
                    auth.logout()
                    st.rerun()
