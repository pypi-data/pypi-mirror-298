""" Azure Container Instances runtime.

# See more details here:
https://docs.microsoft.com/en-us/python/api/overview/azure/container-instance?view=azure-python
"""

from powerlift.executors.localmachine import LocalMachine
from powerlift.bench.store import Store
from typing import List
from powerlift.executors.base import Executor, handle_err
import random
from multiprocessing import Pool


class AzureContainerInstance(Executor):
    """Runs trials on Azure Container Instances."""

    def __init__(
        self,
        store: Store,
        azure_tenant_id: str,
        subscription_id: str,
        azure_client_id: str,
        credential=None,
        azure_client_secret: str = None,
        resource_group: str = "powerlift_rg",
        shell_install: str = None,
        pip_install: str = None,
        wheel_filepaths: List[str] = None,
        n_running_containers: int = 1,
        num_cores: int = 4,
        mem_size_gb: int = 16,
        # other images available at:
        # https://mcr.microsoft.com/en-us/product/devcontainers/python/tags
        # TODO: change default to mcr.microsoft.com/devcontainers/python:latest
        image: str = "mcr.microsoft.com/devcontainers/python:latest",
        docker_db_uri: str = None,
        delete_group_container_on_complete: bool = True,
    ):
        """Runs remote execution of trials via Azure Container Instances.

        Args:
            store (Store): Store that houses trials.
            azure_tenant_id (str): Azure tentant ID.
            subscription_id (str): Azure subscription ID.
            azure_client_id (str): Azure client ID.
            credential: Azure credential
            azure_client_secret (str): Azure client secret.
            resource_group (str): Azure resource group.
            shell_install (str): apt-get install parameters.
            pip_install (str): pip install parameters.
            wheel_filepaths (List[str], optional): List of wheel filepaths to install on ACI trial run. Defaults to None.
            n_running_containers (int, optional): Max number of containers to run simultaneously. Defaults to 1.
            num_cores (int, optional): Number of cores per container. Defaults to 1.
            mem_size_gb (int, optional): RAM size in GB per container. Defaults to 2.
            image (str, optional): Image to execute. Defaults to "mcr.microsoft.com/devcontainers/python:latest".
            docker_db_uri (str, optional): Database URI for container. Defaults to None.
            delete_group_container_on_complete (bool, optional): Delete group containers after completion. Defaults to True.
        """
        from multiprocessing import Manager

        self._credential = credential
        self._image = image
        self._shell_install = shell_install
        self._pip_install = pip_install
        self._n_running_containers = n_running_containers
        self._num_cores = num_cores
        self._mem_size_gb = mem_size_gb
        self._delete_group_container_on_complete = delete_group_container_on_complete

        self._docker_db_uri = docker_db_uri
        self._azure_json = {
            "tenant_id": azure_tenant_id,
            "client_id": azure_client_id,
            "client_secret": azure_client_secret,
            "subscription_id": subscription_id,
            "resource_group": resource_group,
        }
        self._batch_id = random.getrandbits(64)

        self._pool = Pool()
        self._runner_id_to_result = {}
        self._store = store
        self._wheel_filepaths = wheel_filepaths

    def __del__(self):
        if self._pool is not None:
            self._pool.close()

    def delete_credentials(self):
        """Deletes credentials in object for accessing Azure Resources."""
        del self._azure_json

    def submit(self, experiment_id, timeout=None):
        from powerlift.run_azure import __main__ as remote_process

        uri = (
            self._docker_db_uri if self._docker_db_uri is not None else self._store.uri
        )

        params = (
            experiment_id,
            self._n_running_containers,
            uri,
            timeout,
            self._image,
            self._azure_json,
            self._credential,
            self._num_cores,
            self._mem_size_gb,
            self._delete_group_container_on_complete,
            self._batch_id,
        )
        self._batch_id = random.getrandbits(64)
        self._runner_id_to_result[0] = self._pool.apply_async(
            remote_process.run_azure_process,
            params,
            error_callback=handle_err,
        )

    def join(self):
        results = []
        if self._pool is not None:
            for _, result in self._runner_id_to_result.items():
                res = result.get()
                results.append(res)
        return results

    def cancel(self):
        if self._pool is not None:
            self._pool.terminate()

    @property
    def store(self):
        return self._store

    @property
    def wheel_filepaths(self):
        return self._wheel_filepaths
