# Huawei Cloud OBS store plugin for MLflow
This repository provides a MLflow plugin that allows users to use a Huawei Cloud OBS as the artifact store for MLflow.

## Implementation overview
* `huaweicloudstoreplugin`: this package includes the `HuaweiCloudObsArtifactRepository` class that is used to read and write artifacts from Huawei Cloud OBS storage.
* `setup.py` file defines entrypoints that tell MLflow to automatically associate the `obs` URIs with the `HuaweiCloudObsArtifactRepository` implementation when the `huaweicloudstoreplugin` library is installed. The entrypoints are configured as follows:

```
entry_points={
        "mlflow.artifact_repository":
            "obs=huaweicloudstoreplugin.store.artifact.huaweicloud_obs_artifact_repo.py:HuaweiCloudObsArtifactRepository"
        ]
    },
```


# Usage

Install by pip on both your client and the server, and then use MLflow as normal. The Huawei Cloud OBS artifact store support will be provided automatically.

```bash
pip install huaweicloudstoreplugin
```


The plugin implements all of the MLflow artifact store APIs.
It expects Huawei Cloud Storage access credentials in the ``MLFLOW_OBS_REGION``, ``MLFLOW_OBS_ACCESS_KEY_ID`` and ``MLFLOW_OBS_SECRET_ACCESS_KEY`` environment variables,
so you must set these variables on both your client application and your MLflow tracking server.
To use Huawei Cloud OBS as an artifact store, an OBS URI of the form ``obs://<bucket>/<path>`` must be provided, as shown in the example below:

```python
import mlflow


class DemoModel(mlflow.pyfunc.PythonModel):
    def predict(self, ctx, inp) -> int:
        return 1

    
experiment = "demo"
mlflow.create_experiment(experiment, artifact_location="obs://mlflow-test/")
mlflow.set_experiment(experiment)
mlflow.pyfunc.log_model('model_test', python_model=DemoModel())

```

In the example provided above, the ``log_model`` operation creates three entries in the OBS storage ``obs://mlflow-test/$RUN_ID/artifacts/model_test/``, the MLmodel file
and the conda.yaml file associated with the model.
