import inspect
from typing import Dict, List, Optional, Literal

from pydantic import BaseModel, root_validator, validator, Field


class Resource(BaseModel):
    cpu: int = Field(gt=0)
    gpu: int = Field(gt=0)
    ram: int = Field(gt=0)


class ImageInfo(BaseModel):
    image_pull_policy: Literal["Always", "IfNotPresent"] = "Always"
    image_type: Literal["public", "private"] = "public"
    registry_namespace_id: Optional[int]
    # image_pull_secret: int | str


class PytorchJob(BaseModel):
    master_image: str
    master_commands: List[str]
    cluster_id: int
    num_workers: int = 1
    resource: Resource
    # worker_image: Optional[str]
    worker_commands: Optional[List[str]]
    sfs_id: Optional[int]
    sfs_mount_path: Optional[str] = ""
    image_pull_policy: str = "Always"
    image_type: str = "public"
    image_info: ImageInfo = ImageInfo()
    env: Dict[str, str] = {}

    @root_validator(pre=False)
    def __post_init__(cls, values):
        print("User ")
        breakpoint()
        if values['worker_commands'] is None:
            values['worker_commands'] = values['master_commands']
        return values

    @validator('worker_commands')
    def validate_worker_config(cls, value):
        print("User ")
        breakpoint()
        return value

    @validator('env')
    def validate_env(cls, env_dict: dict):
        env_vars = []
        for env_key, env_value in env_dict.items():
            env_vars.append({'name': env_key,
                            "value": env_value})
        return env_vars

    @classmethod
    def get_signature(cls):
        return inspect.signature(cls)


user = PytorchJob(master_image='',
                  master_commands=["John Doe"],
                  cluster_id=1,
                  resource={'cpu': -1,
                            "gpu": 1,
                            "ram": 1},
                  env={'hi': 1,
                       "hello": "hghy"})
print(user)
breakpoint()

print(user.dict())
print(PytorchJob.get_signature())
breakpoint()
x = PytorchJob.get_signature()

{"name": "tir-job-090316133636", "image": "vipin10/minst-nfs", "sfs_id": 143, "isClone": false, "job_cpu": 4, "job_gpu": 1, "job_type": "PyTorchJob", "image_url": "vipin10/minst-nfs", "cluster_id": 276, "image_type": "public", "job_memory": "8GB", "master_replica": 1, "sfs_mount_path": "/mnt/data", "worker_replica": 2, "master_commands": "WyJweXRob24zIiwgIi9vcHQvcHl0b3JjaC1tbmlzdC9tbmlzdC5weSJd", "worker_commands": "WyJweXRob24zIiwgIi9vcHQvcHl0b3JjaC1tbmlzdC9tbmlzdC5weSJd", "image_pull_policy": "Always", "environmentVariable": [], "worker_command_same_as_master": true}