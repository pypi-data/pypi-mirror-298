from abc import ABC, abstractmethod
from typing import Callable

class CustomTracer(ABC):
    @abstractmethod
    def inspect_func(self, func: Callable) -> dict[str, str]:
        pass


class OpenHostaTracer(CustomTracer):
    def inspect_func(self, func: Callable) -> dict[str, str]:
        result = {}
        # check if func have attribute _last_response and add it to result
        if hasattr(func, "_last_response"):
            result["_last_response"] = getattr(func, "_last_response")
        # check if func have attribute _last_request and add it to result
        if hasattr(func, "_last_request"):
            result["_last_request"] = getattr(func, "_last_request")
        return result


_tracer_registry = {
    "openhosta": OpenHostaTracer(),
}

def get_tracer(tracer_name: str) -> CustomTracer:
    return _tracer_registry[tracer_name]

def call_custom_tracers(func: Callable) -> dict[str, dict[str, str]]:
    result = {}
    for tracer in _tracer_registry.values():
        result[tracer.__class__.__name__] = tracer.inspect_func(func)
    return result
