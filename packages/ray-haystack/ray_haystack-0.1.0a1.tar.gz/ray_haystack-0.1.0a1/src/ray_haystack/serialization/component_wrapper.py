from typing import Any, Dict, List, Optional, Type

from haystack.core.component import Component
from haystack.core.errors import DeserializationError
from haystack.core.serialization import component_from_dict, component_to_dict

from ray_haystack.serialization.worker_asset import WorkerAsset


class ComponentWrapper:
    def __init__(
        self,
        component_class: Optional[Type] = None,  # Should be only used during deserialization
        component_data: Optional[Dict[str, Any]] = None,  # Should be only used during deserialization
        assets: Optional[List[WorkerAsset]] = None,  # Should be only used during deserialization
        name: Optional[str] = None,
        component: Optional[Component] = None,
    ):
        self._assets = assets or []
        self._name = name

        if component:
            self._component = component
            self._assets = self._collect_assets()
        elif component_class and component_data:
            self._import_assets()
            self._component = component_from_dict(component_class, component_data, None)
        else:
            raise DeserializationError(
                "You should either provide component instance to the wrapper or the \
                                       combination of component_class and component_data (serialized component)"
            )

    def get_component(self):
        return self._component

    def _collect_assets(self):
        return WorkerAsset.get_assets(self._name)

    def _import_assets(self):
        if self._assets:
            for asset in self._assets:
                asset.import_asset()

    def __reduce__(self):
        # we return a tuple of class_name to call, and parameters to pass when re-creating
        return (
            self.__class__,
            (self._component.__class__, component_to_dict(self._component), self._assets, self._name),
        )
