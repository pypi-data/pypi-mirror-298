import os
import json
import obs
import posixpath
from six.moves import urllib

from mlflow.entities import FileInfo
from mlflow.exceptions import MlflowException
from mlflow.store.artifact.artifact_repo import ArtifactRepository


def flatten(sequence):
    for item in sequence:
        if isinstance(item[1], list):
            for sub_item in flatten(item[1]):
                yield sub_item
        else:
            yield item


def check_status(resp):
    """If the return code is greater than or equal to 300, the interface invocation fails."""
    if isinstance(resp, list):
        err_object = [i[0] for i in flatten(resp) if i[1]["status"] >= 300]
        if err_object:
            err_message = f"List of objects that failed to upload: {err_object}."
            raise Exception(err_message)
    else:
        if resp.status >= 300:
            err_message = json.dumps(
                {
                    "status": resp.status,
                    "reason": resp.reason,
                    "errorCode": resp.errorCode,
                    "errorMessage": resp.errorMessage,
                }
            )
            raise Exception(err_message)


class HuaweiCloudObsEcsArtifactRepository(ArtifactRepository):
    """Stores artifacts on Huawei Cloud OBS."""

    def __init__(self, artifact_uri, obs_bucket=None):
        super(HuaweiCloudObsEcsArtifactRepository, self).__init__(artifact_uri)
        self.obs_bucket = obs_bucket

    @staticmethod
    def get_environs():
        obs_region = os.environ.get('MLFLOW_OBS_REGION')

        if not obs_region:
            raise Exception('please set Environment variable MLFLOW_OBS_REGION.')
        return obs_region

    def _get_obs_client(self):
        region = self.get_environs()
        server = f'https://obs.{region}.myhuaweicloud.com'
        #server = f'https://obs.ap-southeast-3.myhuaweicloud.com'
        return obs.ObsClient(server=server,security_provider_policy='ECS')

    def _get_bucket_client(self, bucket_name):
        if self.obs_bucket:
            return self.obs_bucket
        return self._get_obs_client().bucketClient(bucket_name)

    @staticmethod
    def parse_obs_uri(uri):
        """Parse an OBS URI, returning (bucket, path)"""
        parsed = urllib.parse.urlparse(uri)
        if parsed.scheme != "obs":
            raise Exception("Not an OBS URI: %s" % uri)
        path = parsed.path
        if path.startswith('/'):
            path = path[1:]
        return parsed.netloc, path

    def log_artifact(self, local_file, artifact_path=None):
        if not os.path.isfile(local_file):
            raise Exception("The local_file parameter is expected to be a single experiment output file.")
        (bucket, dest_path) = self.parse_obs_uri(self.artifact_uri)
        if artifact_path:
            dest_path = posixpath.join(dest_path, artifact_path)
        dest_path = posixpath.join(
            dest_path, os.path.basename(local_file))
        results = self._get_bucket_client(bucket).putFile(objectKey=dest_path, file_path=local_file)
        check_status(results)

    def log_artifacts(self, local_dir, artifact_path=None):
        if not os.path.isdir(local_dir):
            raise Exception("The local_file parameter is expected to be a single experiment output file.")
        (bucket, dest_path) = self.parse_obs_uri(self.artifact_uri)
        if artifact_path:
            dest_path = posixpath.join(dest_path, artifact_path)
        local_dir = os.path.abspath(local_dir)
        results = self._get_bucket_client(bucket).putFile(objectKey=dest_path, file_path=local_dir)
        check_status(results)

    def list_artifacts(self, path=None):
        (bucket, artifact_path) = self.parse_obs_uri(self.artifact_uri)
        dest_path = artifact_path
        if path:
            dest_path = posixpath.join(dest_path, path)
        infos = []
        prefix = dest_path + "/" if dest_path else ""
        results = self._get_bucket_client(bucket).listObjects(prefix=prefix, delimiter="/")
        check_status(results)
        for obj in results.body.contents:
            file_path = obj.key
            self._verify_listed_object_contains_artifact_path_prefix(
                listed_object_path=file_path, artifact_path=artifact_path)
            file_rel_path = posixpath.relpath(path=file_path, start=artifact_path)
            file_size = obj.size
            infos.append(FileInfo(file_rel_path, False, file_size))

        prefix_list = [i.prefix for i in results.body.commonPrefixs]
        for subdir_path in prefix_list:
            self._verify_listed_object_contains_artifact_path_prefix(
                listed_object_path=subdir_path, artifact_path=artifact_path)
            subdir_rel_path = posixpath.relpath(path=subdir_path, start=artifact_path)
            if subdir_rel_path.endswith("/"):
                subdir_rel_path = subdir_rel_path[:-1]
            infos.append(FileInfo(subdir_rel_path, True, None))
        return sorted(infos, key=lambda f: f.path)

    @staticmethod
    def _verify_listed_object_contains_artifact_path_prefix(listed_object_path, artifact_path):
        if not listed_object_path.startswith(artifact_path):
            raise MlflowException(
                "The path of the listed obs object does not begin with the specified"
                " artifact path. Artifact path: {artifact_path}. Object path:"
                " {object_path}.".format(
                    artifact_path=artifact_path, object_path=listed_object_path))

    def _download_file(self, remote_file_path, local_path):
        (bucket, obs_root_path) = self.parse_obs_uri(self.artifact_uri)
        obs_full_path = posixpath.join(obs_root_path, remote_file_path)
        results = self._get_bucket_client(bucket).getObject(obs_full_path, local_path)
        check_status(results)

    def delete_artifacts(self, artifact_path=None):
        (bucket, dest_path) = self.parse_obs_uri(self.artifact_uri)
        if artifact_path:
            dest_path = posixpath.join(dest_path, artifact_path)
        list_results = self._get_bucket_client(bucket).listObjects(prefix=dest_path)
        check_status(list_results)
        list_objects = [i.key for i in list_results.body.contents]
        for object_key in list_objects:
            self._verify_listed_object_contains_artifact_path_prefix(
                listed_object_path=object_key, artifact_path=dest_path
            )
            delete_results = self._get_bucket_client(bucket).deleteObject(objectKey=object_key)
            check_status(delete_results)
