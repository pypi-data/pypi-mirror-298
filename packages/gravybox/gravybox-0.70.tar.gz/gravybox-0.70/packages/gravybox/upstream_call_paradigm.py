from asyncio import create_task, as_completed
from typing import List, Coroutine, Type

from pydantic import BaseModel

from gravybox.exceptions import DataUnavailable


def merge_dicts_and_trim_nones(first: dict, second: dict):
    trimmed_first = {}
    for key, value in first.items():
        if isinstance(value, str):
            if len(value) > 0:
                trimmed_first[key] = value
        elif value is not None:
            trimmed_first[key] = value
    trimmed_second = {}
    for key, value in second.items():
        if isinstance(value, str):
            if len(value) > 0:
                trimmed_second[key] = value
        elif value is not None:
            trimmed_second[key] = value
    result = trimmed_first | trimmed_second
    return result


def all_fields_populated(instance: BaseModel):
    for key, value in instance.model_dump().items():
        if value is None:
            return False
    return True


def no_fields_populated(instance: BaseModel):
    for key, value in instance.model_dump().items():
        if value is not None:
            return False
    return True


class UpstreamCentrifuge:
    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel]):
        self.tasks = [create_task(upstream_call) for upstream_call in upstream_calls]
        self.result_model = result_model

    async def activate(self):
        final_result = self.result_model()
        for upstream_call_wrapper in as_completed(self.tasks):
            upstream_result = await upstream_call_wrapper
            if upstream_result is not None:
                final_result_dict = merge_dicts_and_trim_nones(final_result.model_dump(), upstream_result.model_dump())
                final_result = self.result_model.model_validate(final_result_dict)
                if all_fields_populated(final_result):
                    break
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if no_fields_populated(final_result):
            raise DataUnavailable()
        return self.result_model.model_validate(final_result)


class UpstreamSequencer:
    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel]):
        self.upstream_calls = upstream_calls
        self.result_model = result_model

    async def activate(self):
        final_result = self.result_model()
        for upstream_call_wrapper in self.upstream_calls:
            upstream_result = await upstream_call_wrapper
            if upstream_result is not None:
                final_result_dict = merge_dicts_and_trim_nones(final_result.model_dump(), upstream_result.model_dump())
                final_result = self.result_model.model_validate(final_result_dict)
                if all_fields_populated(final_result):
                    break
        if no_fields_populated(final_result):
            raise DataUnavailable()
        return self.result_model.model_validate(final_result)
