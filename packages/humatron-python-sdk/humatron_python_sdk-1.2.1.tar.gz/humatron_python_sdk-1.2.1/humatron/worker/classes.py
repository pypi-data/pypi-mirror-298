"""
This module provides classes and utility functions for working with Humatron,
including request and response handling, payload processing, and asynchronous execution.
"""
import logging

"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""

import datetime
import json
import os
import threading
import uuid
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, NamedTuple, Any, Union

from locked_dict.locked_dict import LockedDict

PayloadPart = dict[Any, Any]
"""Payload part type alias."""
Storage = dict[Any, Any]
"""Storage type alias."""


class Request(NamedTuple):
    """
    Represents a Humatron request with a command, unique ID, timestamp, payload, and optional storage.
    """

    req_cmd: str
    """The command associated with the request."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp when the request was created in ISO format."""
    payload: list[PayloadPart]
    """A list of payload parts containing the data for the request."""
    storage: Optional[Storage]
    """Optional storage for maintaining state during request processing."""

    @classmethod
    def make(cls, cmd: str, payload: list[PayloadPart] | PayloadPart, storage: Optional[Storage] = None) -> 'Request':
        """
        Factory method to create a new Request.

        @param cmd :
            The command for the request (e.g., 'start', 'pause').
        @param payload :
            The payload for the request, which can be a list or a single part.
        @param storage :
            Optional storage to pass along with the request.

        @return:
            A new Request instance with the given parameters.
        """
        p = payload if isinstance(payload, list) else [payload]
        return cls(cmd, str(uuid.uuid4()), _utc_now_iso_format(), p, storage)

    @classmethod
    def from_json(cls, js: str) -> 'Request':
        """
        Creates a Request instance from a JSON string.

        @param js :
            The JSON string representing the request.

        @return:
            A new Request instance.
        """
        return cls.from_dict(json.loads(js))

    @classmethod
    def from_dict(cls, d: dict[Any, Any]) -> 'Request':
        """
        Creates a Request instance from a dictionary.

        @param d :
            A dictionary containing the request data.

        @return:
            A new Request instance.
        """
        return cls(d['req_cmd'], d['req_id'], d['req_tstamp'], d['payload'], d.get('storage'))

    def to_json(self) -> str:
        """
        Converts the Request instance to a JSON string.

        @return:
            A JSON string representing the Request instance.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[Any, Any]:
        """
        Converts the Request instance to a dictionary.

        @return:
            A dictionary representing the Request instance.
        """
        return {
            'req_cmd': self.req_cmd,
            'req_id': self.req_id,
            'req_tstamp': self.req_tstamp,
            'payload': self.payload,
            'storage': self.storage
        }


class Response(NamedTuple):
    """
    Represents a Humatron response with a unique ID, timestamp, optional payload, and optional storage.
    """

    resp_id: str
    """The unique identifier for the response."""
    resp_tstamp: str
    """The timestamp when the response was created in ISO format."""
    payload: Optional[list[PayloadPart]]
    """An optional list of payload parts containing the response data."""
    storage: Optional[Storage]
    """Optional storage for maintaining state during response processing."""

    @classmethod
    def from_json(cls, js: str) -> 'Response':
        """
        Creates a Response instance from a JSON string.

        @param js :
            The JSON string representing the response.

        @return:
            A new Response instance.
        """
        return cls.from_dict(json.loads(js))

    @classmethod
    def from_dict(cls, d: dict[Any, Any]) -> 'Response':
        """
        Creates a Response instance from a dictionary.

        @param d :
            A dictionary containing the response data.

        @return:
            A new Response instance.
        """
        return cls(d['resp_id'], d['resp_tstamp'], _get_opt(d, 'payload'), _get_opt(d, 'storage'))

    def to_json(self) -> str:
        """
        Converts the Response instance to a JSON string.

        @return:
            A JSON string representing the Response instance.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[Any, Any]:
        """
        Converts the Response instance to a dictionary.

        @return:
            A dictionary representing the Response instance.
        """
        return {
            'resp_id': self.resp_id,
            'resp_tstamp': self.resp_tstamp,
            'payload': self.payload,
            'storage': self.storage
        }


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
_logger = logging.getLogger('humatron.worker.sdk')


class HumatronWorker(ABC):
    """
    Abstract base class for a Humatron worker.

    This class defines the interface that must be implemented by any concrete Humatron worker.
    """

    @abstractmethod
    def post_request(self, req: Request) -> Optional[Response]:
        """
        Posts a request for processing and optionally returns a response.

        @param req :
            The request to be processed.

        @return:
            The response after processing the request, if any.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closes the worker, releasing any resources.

        This method is responsible for cleaning up resources used by the worker.
        """
        pass


class RequestPayloadPart(NamedTuple):
    """
    Represents a part of the request payload with command, ID, timestamp, and payload part.
    """

    req_cmd: str
    """The command associated with the payload part"""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp of the request."""
    payload_part: PayloadPart
    """A dictionary representing a part of the request payload."""


ResponsePayloadPart = Union[list[PayloadPart], PayloadPart, None]
"""Reponse payload part alias."""


class HumatronWorkerAsyncAdapter(HumatronWorker, ABC):
    """
    Asynchronous adapter for Humatron worker using a thread pool executor.

    This class extends the HumatronWorker to provide asynchronous request processing
    using a thread pool for concurrency.
    """

    def __init__(self, pool_size: Optional[int] = None):
        """
        Initializes the async adapter with a thread pool.

        @param pool_size :
            The maximum number of threads in the pool. Defaults to the number of CPUs.
        """
        super().__init__()
        self._pool = ThreadPoolExecutor(max_workers=pool_size or os.cpu_count())
        self._payloads_parts: list[PayloadPart] = []
        self._lock = threading.Lock()
        self._storage: Optional[LockedDict] = None

    def close(self) -> None:
        """
        Shuts down the thread pool, ensuring all tasks are completed.
        """
        self._pool.shutdown()

    def post_request(self, req: Request) -> Optional[Response]:
        """
        Posts a request asynchronously, processing its payload parts and returning a response.

        @param req :
            The request to be processed asynchronously.

        @return:
            The response after processing the request, or None if no response is available.
        """
        if req.req_cmd == 'interview':
            if req.storage:
                raise ValueError('Storage cannot be provided for `interview` requests.')
            elif not req.payload or len(req.payload) != 1:
                raise ValueError('Invalid payload for `interview` request.')

            pp = self.execute(RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, req.payload[0]), None)

            match pp:
                case dict():
                    return Response(make_id(), _utc_now_iso_format(), [pp], None)
                case _:
                    raise ValueError(f'Unexpected response payload for `interview` request [payload={pp}]')

        if self._storage is None:
            self._storage = LockedDict()
            self._storage.update(req.storage)

        def fn() -> None:
            try:
                res: list[PayloadPart] = []
                if req.payload:
                    for parts in req.payload:
                        parts = self.execute(
                            RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, parts), self._storage
                        )

                        if parts is not None:
                            if not isinstance(parts, list):
                                parts = [parts]

                            parts = list(filter(lambda el: el, parts)) if parts else None

                            if parts:
                                res.extend(parts)
                    with self._lock:
                        if res:
                            self._payloads_parts.extend(res)
            except Exception as e:
                _logger.error(f'Error during processing [error={e}]', exc_info=True)

        self._pool.submit(fn)

        with self._lock:
            if not self._payloads_parts and not self._storage:
                return None

            payloads = self._payloads_parts[:]
            self._payloads_parts.clear()

        return Response(
            make_id(),
            _utc_now_iso_format(),
            (payloads if payloads else None),
            self._storage.copy()
        )


    @abstractmethod
    def execute(self, req: RequestPayloadPart, storage: Optional[Storage]) -> ResponsePayloadPart:
        """
        Abstract method to execute a request payload part.

        @param req :
            The request payload part to be executed.
        @param storage :
            Optional storage used for processing.

        @return:
            The result of the execution, which could be a list of payload parts, a single payload part, or None.
        """
        pass


# Utility functions

def _get_opt(d: dict[str, Any], k: str) -> Optional[Any]:
    """
    Retrieves an optional value from a dictionary by key.

    @param d :
        The dictionary to retrieve the value from.
    @param k :
        The key to search for in the dictionary.

    @return:
        The value associated with the key, or None if the key is not present.
    """
    return d.get(k)


def _utc_now_iso_format() -> str:
    """
    Returns the current UTC time in ISO format, truncated to milliseconds.

    @return:
        The current UTC time in ISO format, truncated to milliseconds.
    """
    return f'{datetime.datetime.utcnow().isoformat()[:-3]}Z'


def make_id() -> str:
    """
    Generates a unique ID.

    @return:
        A unique identifier string.
    """
    return str(uuid.uuid4().hex)


def make_default_response_payload(
    req_cmd: str,
    req_payload_part: PayloadPart,
    contacts: Optional[list[dict[str, Any]]] = None
) -> Optional[PayloadPart]:
    """
    Generates a default response payload based on the request command.

    @param req_cmd :
        The command associated with the request (e.g., 'register', 'heartbeat').
    @param req_payload_part :
        The request payload part for which to generate a response.
    @param contacts :
        An optional list of contacts to include in the response.

    @return:
        The generated response payload, or None if the request command is not supported.
    """
    instance = req_payload_part['instance']

    def mk_response(extra: Optional[PayloadPart] = None) -> PayloadPart:
        d = {
            'resp_cmd': req_cmd,
            'instance_id': instance['id'],
            'ref_payload_id': req_payload_part['payload_id']
        }
        if contacts:
            d['contacts'] = contacts
        if extra:
            d.update(extra)
        return d

    match req_cmd:
        case 'register' | 'pause' | 'resume':
            return mk_response({'result': True})
        case 'unregister':
            return mk_response()
        case 'heartbeat':
            return None
        case _:
            raise ValueError(f'Unsupported request type: {req_cmd}')


def extract_channel_type(
    resources: list[dict[str, Any]],
    res_id: int,
    supported: set[str] = None
) -> str:
    """
    Extracts the channel type for a given resource ID.

    @param resources :
        The list of resources from which to extract the channel type.
    @param res_id :
        The resource ID to find the associated channel type.
    @param supported :
        A set of supported channel types. If provided, an error is raised if the extracted type is not supported.

    @return:
        The extracted channel type.

    @raise ValueError:
        If the resource is not found or the channel type is not supported.
    """
    channel_type = next((r['channel_type'] for r in resources if r['id'] == res_id), None)

    if not channel_type:
        raise ValueError(f'Unexpected resource: {res_id}')
    elif supported and channel_type not in supported:
        raise ValueError(f'Unsupported channel type: {channel_type}')

    return channel_type
