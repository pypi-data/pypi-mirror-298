import abc
import dataclasses
import hashlib
import logging
import pathlib
import pickle
import typing
import urllib.parse
import azure.core.exceptions
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient, ContentSettings
import tenacity
from irisml.core.hash_generator import HashGenerator


logger = logging.getLogger(__name__)


def create_storage_manager(url: str):
    is_http = urllib.parse.urlparse(url).scheme in ['http', 'https']
    if is_http:
        return AzureBlobStorageManager(url)
    elif pathlib.Path(url).exists():
        return FileSystemStorageManager(pathlib.Path(url))

    raise ValueError(f"Invalid cache storage URL is provided. {url} If it's local file path, please make sure the path exists on your filesystem.")


class StorageManager(abc.ABC):
    """Access the storage that manages cache"""
    @abc.abstractmethod
    def get_hash(self, paths):
        pass

    @abc.abstractmethod
    def get_contents(self, paths):
        pass

    @abc.abstractmethod
    def put_contents(self, paths, contents, hash_value, overwrite: bool):
        pass


class AzureBlobStorageManager(StorageManager):
    """Interact with Azure Blob Storage.

    URL to the container must be provided. If the URL doesn't contain SAS token, Managed Identity and Intractive authentication will be used.

    Hash value will be stored in the metadata field of the blob.
    """
    HASH_METADATA_NAME = 'irisml_hash'

    def __init__(self, container_url):
        self._container_url = container_url
        try:
            self._container_client = ContainerClient.from_container_url(self._container_url)
            # Try to get a list of blobs in order to check the read permission.
            next(self._container_client.list_blobs())
        except (azure.core.exceptions.ResourceExistsError, azure.core.exceptions.ClientAuthenticationError):
            logger.debug("Cache storage is not accessible without credentials. Trying DefaultAzureCredential.")
            self._container_client = ContainerClient.from_container_url(self._container_url, credential=DefaultAzureCredential())
        except StopIteration:
            # Successfully accessed, but there was no existing blob.
            pass

    def get_hash(self, paths):
        blob_client = self._container_client.get_blob_client('/'.join(paths))
        try:
            properties = blob_client.get_blob_properties()
            hash_value = properties.metadata.get(self.HASH_METADATA_NAME)
            return hash_value
        except azure.core.exceptions.ResourceNotFoundError:
            logger.debug(f"{paths} was not found in the container.")
        return None

    # Retries if there was unexpected error. For example, if the blob was modified while downloading, download_blob() will throw ResourceModifiedError
    @tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception_type(azure.core.exceptions.ResourceModifiedError))
    def get_contents(self, paths):
        try:
            contents = self._container_client.download_blob('/'.join(paths), max_concurrency=8, timeout=300).readall()
            return contents
        except azure.core.exceptions.ResourceNotFoundError:
            logger.debug(f"{paths} was not found in the container.")
        return None

    def put_contents(self, paths, contents, hash_value, overwrite):
        blob_client = self._container_client.get_blob_client('/'.join(paths))

        if blob_client.exists() and not overwrite:
            logger.debug("The blob already exists. Skipping upload. Probably it was uploaded by another process.")
            return

        contents_md5_hash = hashlib.md5(contents)
        logger.debug(f"Uploading a cache to Azure Blob. md5_hash={contents_md5_hash.hexdigest()}")
        content_settings = ContentSettings(content_md5=bytearray(contents_md5_hash.digest()))
        try:
            # Set overwrite=True since sometimes a blob data will be corrupted if two processes uploaded to a same blob with overwrite=False.
            blob_client.upload_blob(contents, content_settings=content_settings, metadata={self.HASH_METADATA_NAME: hash_value}, max_concurrency=8, timeout=300, overwrite=True)
        except Exception as e:
            logger.warning(f"Failed to upload cache {paths} (hash={hash_value}) due to {e}. The error is ignored.")

    def __getstate__(self):
        return {'container_url': self._container_url}

    def __setstate__(self, state):
        self.__init__(**state)


class FileSystemStorageManager(StorageManager):
    """Use the local filesystem as the cache."""

    def __init__(self, cache_dir: pathlib.Path):
        assert isinstance(cache_dir, pathlib.Path)
        self._cache_dir = cache_dir

    def get_hash(self, paths):
        loaded = pickle.loads(self.get_contents(paths))
        return HashGenerator.calculate_hash(loaded)

    def get_contents(self, paths):
        filepath = self._cache_dir.joinpath(*paths)
        if not filepath.exists():
            return None
        return filepath.read_binary()

    def put_contents(self, paths, contents, hash_value, overwrite):
        filepath = self._cache_dir.joinpath(*paths)
        if filepath.exists() and not overwrite:
            logger.warning(f"Path {filepath} already exists. The new cache is not saved.")
            return
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(contents)


class CachedOutputs:
    """Used to represent cached outputs so that we can load the contents lazily."""
    def __init__(self, storage_manager, base_paths, outputs_class, hash_values: typing.Dict[str, str]):
        self._storage_manager = storage_manager
        self._paths = base_paths
        self._field_types = {f.name: f.type for f in dataclasses.fields(outputs_class)}
        self._hash_values = hash_values
        self._contents = {}

    def get_hash(self, name: str) -> str:
        assert '.' not in name
        return self._hash_values[name]

    def __getattr__(self, name):
        """Load the actual contents."""

        # First, check if the _field_types is available. It might not be available if this instance was deepcopied.
        field_types = super().__getattribute__('_field_types')
        if not field_types:
            raise AttributeError

        if name not in self._field_types:
            raise AttributeError

        if name in self._contents:
            return self._contents[name]

        logger.debug(f"Getting cache {self._paths + [name]}. hash: {self._hash_values[name]}.")
        try:
            contents = self._storage_manager.get_contents(self._paths + [name])
            value = pickle.loads(contents)
        except Exception as e:
            raise RuntimeError(f"Failed to load the cache {self._paths + [name]}") from e

        # Subscripted generic types cannot be used for isinstance check.
        # if not isinstance(value, self._field_types[name]):
        #     raise RuntimeError(f"The downloaded cache for {name} has invalid type: {type(value)}. Expected: {self._field_types[name]}")

        # Check the hash value of the downloaded cache.
        current_hash = HashGenerator.calculate_hash(value)
        if current_hash != self._hash_values[name]:
            logger.error(f"Downloaded cache {name} has wrong hash. Expected: {self._hash_values[name]}. Actual: {current_hash}. Ignoring this error.")

        self._contents[name] = value
        return value


class CacheManager:
    def __init__(self, storage_manager, no_read: bool):
        self._storage_manager = storage_manager
        self._no_read = no_read

    def get_cache(self, task_name: str, task_version: str, task_hash: str, outputs_class):
        """Try to get the cache for the specified task.

        Args:
            task_name (str): The task name.
            task_version (str): The task version
            task_hash (str): The hash value for the task inputs and config.
            outputs_class (dataclasses.dataclass): The dataclass for the task Outputs.
        Returns:
            CachedOutputs if a cache is found. If not, returns None.
        """
        if self._no_read:
            return None

        base_paths = [task_name, task_version, task_hash]
        hash_values = {}
        for field in dataclasses.fields(outputs_class):
            hash_values[field.name] = self._storage_manager.get_hash(base_paths + [field.name])
            assert hash_values[field.name] is None or isinstance(hash_values[field.name], str)

        if not any(hash_values.values()):
            return None

        if not all(hash_values.values()):
            logger.warning(f"Some cache files are missing: {hash_values}")
            return None

        return CachedOutputs(self._storage_manager, base_paths, outputs_class, hash_values)

    def upload_cache(self, task_name: str, task_version: str, task_hash: str, outputs):
        base_paths = [task_name, task_version, task_hash]
        for name, value in dataclasses.asdict(outputs).items():
            # This hash_value doesn't match with the actual hash for the contents. See HashGenerator for the detail.
            hash_value = HashGenerator.calculate_hash(value)
            contents = pickle.dumps(value)

            # Double check that the hash is calculated correctly.
            # If this check failed, please check the HashGenerator and __getstate__ attribute of the failed object.
            loaded = pickle.loads(contents)
            loaded_hash_value = HashGenerator.calculate_hash(loaded)
            if hash_value != loaded_hash_value:
                logger.error(f"The object {name} has different hash after serialization. Before: {hash_value}. After: {loaded_hash_value} task: {task_name}")
            else:
                logger.debug(f"Saving cache {base_paths + [name]}. hash: {hash_value}, size: {len(contents)}")
                # If no_read=True, we need to allow overwriting the cache.
                self._storage_manager.put_contents(base_paths + [name], contents, hash_value, overwrite=self._no_read)
