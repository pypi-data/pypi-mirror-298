import os
import subprocess
import sys
import tarfile
import tempfile
import threading
import traceback
from typing import Optional

import mlflow
from ML_management.mlmanagement.base_exceptions import MLMClientError
from ML_management.mlmanagement.log_api import _raise_error
from ML_management.mlmanagement.model_type import ModelType
from ML_management.mlmanagement.session import AuthSession
from ML_management.mlmanagement.variables import get_log_service_url


def download_artifacts_by_name_version(
    name: str, version: int, model_type: ModelType, path: str, dst_path: Optional[str] = None
) -> str:
    """Download an artifact by name and version to a local directory, and return a local path for it."""
    url = get_log_service_url("download_artifacts_by_name_version")
    params = {
        "path": os.path.normpath(path) if path else path,
        "name": name,
        "version": version,
        "model_type": model_type.value,
    }
    return _request_download_artifacts(url, params, dst_path)


def download_job_artifacts(job_id: str, path: str = "", dst_path: Optional[str] = None) -> str:
    """Download an artifact file or directory from a job to a local directory, and return a local path for it."""
    url = get_log_service_url("download_job_artifacts")
    params = {"path": os.path.normpath(path) if path else path, "job_name": job_id}
    return _request_download_artifacts(url, params, dst_path)


def _load_model_type(
    name: str,
    version: int,
    model_type: ModelType,
    unwrap: bool = True,
    install_requirements: bool = False,
    dst_path: Optional[str] = None,
):
    """Load model from local path."""
    local_path = download_artifacts_by_name_version(
        name=name, version=version, model_type=model_type, path="", dst_path=dst_path
    )
    if install_requirements:
        _set_model_version_requirements(local_path)
    loaded_model = mlflow.pyfunc.load_model(model_uri=local_path, suppress_warnings=True)
    if unwrap:
        artifacts_path = loaded_model._model_impl.context._artifacts
        loaded_model = loaded_model.unwrap_python_model()
        loaded_model.artifacts = artifacts_path
    return loaded_model


def load_dataset(
    name: str, version: int, install_requirements: bool = False, unwrap: bool = True, dst_path: Optional[str] = None
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the dataset.
    version: int
        Version of the dataset.
    install_requirements: bool = False
        Whether to install dataset requirements. Default: False.
    unwrap: bool = True
        Whether to unwrap dataset. Default: True.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    DatasetLoaderPattern
        The object of the dataset to use.
    """
    return _load_model_type(name, version, ModelType.DATASET_LOADER, unwrap, install_requirements, dst_path)


def _set_model_version_requirements(local_path) -> None:
    """Installing requirements of the model locally."""
    with open(os.path.join(local_path, "requirements.txt")) as req:
        requirements = req.read().split("\n")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--default-timeout=100", *requirements]
        )
    except Exception:
        print(traceback.format_exc())


def load_model(
    name: str, version: int, install_requirements: bool = False, unwrap: bool = True, dst_path: Optional[str] = None
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the model.
    version: int
        Version of the model.
    install_requirements: bool = False
        Whether to install model requirements. Default: False.
    unwrap: bool = True
        Whether to unwrap model. Default: True.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    Model
        The object of the model to use.
    """
    return _load_model_type(name, version, ModelType.MODEL, unwrap, install_requirements, dst_path)


def load_executor(
    name: str, version: int, install_requirements: bool = False, unwrap: bool = True, dst_path: Optional[str] = None
):
    """Download all model's files for loading model locally.

    Parameters
    ==========
    name: str
        Name of the executor.
    version: int
        Version of the executor.
    install_requirements: bool = False
        Whether to install executor requirements. Default: False.
    unwrap: bool = True
        Whether to unwrap executor. Default: True.
    dst_path: Optional[str]: None
        Destination path. Default: None.
    Returns
    =======
    BaseExecutor
        The object of the executor to use.
    """
    return _load_model_type(name, version, ModelType.EXECUTOR, unwrap, install_requirements, dst_path)


def _untar_folder(buff, to_folder):
    try:
        with tarfile.open(mode="r|", fileobj=buff) as tar:
            tar.extractall(to_folder)
    except Exception as err:
        raise MLMClientError("Some error during untar the content.") from err


def _request_download_artifacts(url, params: dict, dst_path: Optional[str] = None):
    path = params["path"]
    with AuthSession().get(url=url, params=params, stream=True) as response:
        _raise_error(response)
        untar = response.headers.get("untar") == "True"
        if dst_path is None:
            dst_path = tempfile.mkdtemp()
        dst_path = os.path.abspath(os.path.normpath(dst_path))
        local_path = os.path.normpath(os.path.join(dst_path, os.path.normpath(path)))
        if untar:
            r, w = os.pipe()
            with open(r, "rb") as buff:
                try:
                    thread = threading.Thread(target=_untar_folder, args=(buff, local_path))
                    thread.start()
                except Exception as err:
                    os.close(r)
                    os.close(w)
                    raise err

                with open(w, "wb") as wfd:
                    for chunk in response.iter_raw():
                        wfd.write(chunk)
                thread.join()
                return local_path
        else:
            dirs = os.path.dirname(local_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            with open(local_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            return local_path
