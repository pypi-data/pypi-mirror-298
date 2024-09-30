from typing import Dict, Union

from ray.runtime_env import RuntimeEnv
from typing_extensions import Literal, TypedDict


class ActorOptions(TypedDict, total=False):
    """The globally unique name for the actor, which can be used to retrieve the actor via ray.get_actor(name) as long
    as the actor is still alive."""

    name: str

    """Override the namespace to use for the actor. By default, actors are created in an anonymous namespace. The actor
    can be retrieved via ray.get_actor(name=name, namespace=namespace)"""
    namespace: str

    """If specified, requires that the task or actor run on a node with the specified type of accelerator.
    See [accelerator-types](https://docs.ray.io/en/latest/ray-core/accelerator-types.html#accelerator-types)"""
    accelerator_type: str

    """The heap memory request in bytes for this task/actor, rounded down to the nearest integer."""
    memory: Union[int, float]

    """The quantity of CPU cores to reserve for this task or for the lifetime of the actor."""
    num_cpus: Union[int, float]

    """The quantity of GPUs to reserve for this task or for the lifetime of the actor."""
    num_gpus: Union[int, float]

    """The object store memory request"""
    object_store_memory: int

    """The quantity of various custom resources to reserve for this task or for the lifetime of the actor.
    This is a dictionary mapping strings (resource names) to floats."""
    resources: Dict[str, float]

    """Either None, which defaults to the actor will fate share with its creator and will be deleted once its refcount
    drops to zero, or “detached”, which means the actor will live as a global object independent of the creator."""
    lifetime: Literal["detached", "non_detached"]

    """Specifies the runtime environment for this actor or task and its children.
    See [Runtime environments](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html#runtime-environments)
    for detailed documentation."""
    runtime_env: Union[dict, RuntimeEnv]

    """True if tracing is enabled, i.e., task events from the actor should be reported. Defaults to True."""
    enable_task_events: bool

    """This specifies the maximum number of times that the actor should be restarted when it dies unexpectedly. The
    minimum valid value is 0 (default), which indicates that the actor doesn't need to be restarted. A value of -1
    indicates that an actor should be restarted indefinitely."""
    max_restarts: int

    """Set the max number of pending calls allowed on the actor handle. When this value is exceeded,
    PendingCallsLimitExceeded will be raised for further tasks. Note that this limit is counted per handle. -1 means
    that the number of pending calls is unlimited."""
    max_pending_calls: int

    """The max number of concurrent calls to allow for this actor. This only works with direct actor calls. The max
    concurrency defaults to 1 for threaded execution, and 1000 for asyncio execution. Note that the execution order is
    not guaranteed when max_concurrency > 1."""
    max_concurrency: int

    """Create an actor with same name/namespace only if it doesn't exist."""
    get_if_exists: bool


class CommonSettings(TypedDict, total=False):
    actor_options: ActorOptions


class ProcessorSettings(TypedDict, total=False):
    actor_options: ActorOptions


class ComponentSettings(TypedDict, total=False):
    actor_options: ActorOptions


class RayPipelineSettings(TypedDict, total=False):
    common: CommonSettings
    processor: ProcessorSettings
    components: Dict[str, ComponentSettings]
