from typing import Callable, cast
from zipfile import ZipFile
import io
from google.cloud.firestore_v1.transaction import Transaction
from google.cloud.firestore_v1 import (
    DocumentReference,
    Query,
)
from google.cloud.exceptions import Conflict
from google.cloud.storage import Bucket
from google.cloud.firestore import Client, Transaction, transactional, ArrayUnion
import streamlit as st
import pandas as pd
import toml

from vizkit.pipeline.data_source import DataFile, DataFileMeta
from vizkit.pipeline.data_source.firebase import app as fb_app


_BUCKET = fb_app.get_bucket()
_STORE = fb_app.get_store()


def __get_data_cache() -> dict[str, DataFile]:
    return st.session_state.setdefault("data_file_cache", {})


def __get_meta_cache() -> dict[str, DataFileMeta]:
    return st.session_state.setdefault("data_file_meta_cache", {})


def __get_user_projects_cache() -> dict[str, dict[str, list[str] | None]]:
    return st.session_state.setdefault("data_user_projects_cache", {})


def __evict_user_cache(user: str):
    cache = __get_user_projects_cache()
    if user in cache:
        del cache[user]


def upload_file(
    bucket: Bucket, client: Client, data: bytes, name: str, meta: DataFileMeta
) -> tuple[str, bool]:
    """Upload file to bucket and add metadata to firestore"""
    file = io.BytesIO(data)
    blob = bucket.blob(name)
    new_blob = not blob.exists()
    if blob.exists():
        return blob.public_url, new_blob
    # Upload file
    blob.upload_from_file(file)
    blob.patch()
    blob.metadata = meta.to_dict()
    blob.patch()
    # Add to `results` collection
    docRef = client.collection("results").document(meta.sha256)
    docRef.set(meta.to_dict())
    return blob.public_url, new_blob


def claim_file(id: str, owner: str):
    """Claim the ownership of a file"""
    t = _STORE.transaction()
    resultDocRef = _STORE.document("results", id)

    @transactional
    def claim_file_in_transaction(tx: Transaction, resultDocRef: DocumentReference):
        meta = resultDocRef.get(transaction=tx)
        if not meta.exists:
            raise ValueError("File not found: " + id + ".zip")
        meta = meta.to_dict() or {}
        # Add to user's results
        project = meta.get("project") or "<n/a>"
        runid = meta.get("runid") or "<n/a>"
        projectDocRef = _STORE.document("users", owner, "projects", project)
        if not projectDocRef.get(transaction=tx).exists:
            tx.create(projectDocRef, {"files": [id]})
        else:
            tx.update(projectDocRef, {"files": ArrayUnion([id])})
        # Update metadata
        tx.update(resultDocRef, {"owner": owner})
        # Update cache
        cache = __get_data_cache()
        if id in cache:
            cache[id].meta.owner = owner
        cache = __get_meta_cache()
        if id in cache:
            cache[id].owner = owner
        __evict_user_cache(owner)
        return True

    claim_file_in_transaction(t, resultDocRef)


def get_file(id: str) -> DataFile:
    """Download and load data file"""
    # Check cache
    cache = __get_data_cache()
    if id in cache:
        return cache[id]
    # Download file
    blob = _BUCKET.blob(f"results/{id}.zip")
    if not blob.exists():
        blobs = list(_BUCKET.list_blobs(prefix=f"results/{id}", max_results=1))
        if len(blobs) == 0:
            raise ValueError("File not found: " + id + ".zip")
        blob = blobs[0]
    assert isinstance(blob.name, str)
    id = blob.name.split("/")[-1].removesuffix(".zip")
    file = io.BytesIO()
    blob.download_to_file(file)
    file.seek(0)
    with ZipFile(file, "r") as zip:
        with zip.open("results.csv") as f:
            results = pd.read_csv(f)
        with zip.open("config.toml") as f:
            config = toml.loads(f.read().decode("utf-8"))
    file = DataFile(
        results=results,
        config=config,
        meta=get_file_meta(id),
    )
    # Update cache
    cache[id] = file
    return file


def get_file_meta(id: str) -> DataFileMeta:
    """Get metadata of a data file"""
    # Check cache
    cache = __get_meta_cache()
    if id in cache:
        return cache[id]
    # Get metadata from firestore
    docRef = _STORE.document("results", id)
    meta = docRef.get()
    if not meta.exists:
        raise ValueError("File not found: " + id + ".zip")
    m = meta.to_dict() or {}
    runid = m.get("runid")
    assert runid is not None
    project = m.get("project")
    assert project is not None
    profile = m.get("profile")
    assert profile is not None
    meta = DataFileMeta(
        sha256=m.get("sha256", id),
        runid=runid,
        project=project,
        profile=profile,
        owner=m.get("owner"),
    )
    # Update cache
    cache[id] = meta
    return meta


def get_projects(owner: str) -> list[str]:
    """Get list of data files owned by a user"""
    cache = __get_user_projects_cache()
    if owner in cache:
        return list(cache[owner].keys())
    collectionRef = _STORE.collection("users", owner, "projects").list_documents()
    ids = []
    for doc in collectionRef:
        assert isinstance(doc, DocumentReference)
        ids.append(doc.id)
    cache[owner] = {p: None for p in ids}
    return ids


def __get_project_file_ids(owner: str, project: str) -> list[str]:
    cache = __get_user_projects_cache()
    if owner in cache and project in cache[owner] and cache[owner][project] is not None:
        return cache[owner][project] or []
    docRef = _STORE.document("users", owner, "projects", project).get()
    if not docRef.exists:
        return []
    doc = docRef.to_dict() or {}
    files = list(doc.get("files", []))
    cache.setdefault(owner, {})[project] = files
    return files


def get_owned_project_files(owner: str, project: str) -> list[DataFileMeta]:
    """Get list of data files owned by a user"""
    ids = __get_project_file_ids(owner, project)
    results = []
    for id in ids:
        results.append(get_file_meta(id))
    return results


def get_inflated_id(short_id: str) -> str | None:
    doc = _STORE.document("share-links-v1", short_id).get()
    if not doc.exists:
        return None
    return doc.get("inflated")


def insert_inflated_id(inflated: str, gen_key: Callable[[], str]) -> str:
    while True:
        try:
            tx = _STORE.transaction()
            links = _STORE.collection("share-links-v1")
            query = links.where("inflated", "==", inflated).limit(1)
            short_id = gen_key()
            new_doc = links.document(short_id)
            return __insert_inflated_id(tx, inflated, query, new_doc, short_id)
        except Conflict:
            continue


@transactional
def __insert_inflated_id(
    transaction: Transaction,
    inflated: str,
    query: Query,
    new_doc: DocumentReference,
    short_id: str,
):
    docs = query.get(transaction=transaction)
    if len(docs) > 0:
        return docs[0].id
    transaction.create(new_doc, {"inflated": inflated})
    return short_id
