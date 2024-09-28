from ctypes import (
    c_int,
    cdll,
    POINTER,
    c_uint32,
    c_char,
    c_char_p,
    c_uint,
    byref,
    create_string_buffer,
)
from dataclasses import asdict, dataclass
import enum
import json
from os import path
from typing import (
    List,
    Dict,
    Optional,
    Type,
    TypeVar,
    Generic,
    TypedDict,
)

T = TypeVar("T")

LIB_PATH = path.join(path.dirname(__file__), "cdylib", "libfireball_c")

API_VERSION = 1  # removed from fireball-core, but still in the C API
JSON_FORMAT = 1


# integer values must align with fireball-core's BitAgentMessages enum
class AgentMessages(enum.Flag):
    NEW_CONFIG_AVAILABLE = 1 << 0
    NEW_APP_SETTINGS_AVAILABLE = 1 << 1
    NEW_SERVER_SETTINGS_AVAILABLE = 1 << 2


NO_MESSAGES = AgentMessages(0)


# string values must deserialize to values in fireball-core's AgentLanguage enum,
# according to the deserialization rules defined by `serde` for the enum.
# Also, we'd like StrEnum here, but it's only available in python 3.11. Inheriting from
# str allows us to easily serialize this with `json.dumps`.
class AgentLanguage(str, enum.Enum):
    DOTNET = "DotNet"
    DOTNET_CORE = "DotNetCore"
    GO = "Go"
    NODE = "Node"
    JAVA = "Java"
    PYTHON = "Python"
    PHP = "Php"
    RUBY = "Ruby"


@dataclass(frozen=True)
class BindingApiSuccess(Generic[T]):
    messages: AgentMessages
    data: T


# we'd probably like `kw_only=True` for large dataclasses like this, but that feature
# was added in python 3.10
@dataclass(frozen=True)
class InitOptions:
    app_name: str
    app_path: str
    agent_language: AgentLanguage
    agent_version: str
    server_host_name: str
    server_path: str
    server_type: str
    config_paths: Optional[List[str]]
    overrides: Optional[Dict[str, str]]

    def _to_json_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


libfireball_c = cdll.LoadLibrary(LIB_PATH)

libfireball_c.initialize_application.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_char_p,  # init_options_buf
    c_uint,  # init_options_buf_len
    POINTER(c_char_p),  # result
    POINTER(c_uint),  # result_size
    POINTER(c_uint),  # messages
]
libfireball_c.initialize_application.restype = c_int

libfireball_c.free_result.argtypes = [c_char_p]
libfireball_c.free_result.restype = c_int


class MustFreeBuffer(c_char_p):
    """
    Special subclass of c_char_p that guarantees fireball's `free_result` will be called
    when an instance is deleted by python's garbage collector. This is useful for cases
    where fireball allocates memory and leaves the caller responsible for freeing it.
    """

    def __del__(self) -> None:
        # If this fails, it'll at least be logged at the ERROR level.
        #
        # Translating the return code to an Exception in a __del__ could raise the
        # exception during GC, where the caller can't handle it.
        libfireball_c.free_result(self)


class InitAppSettings(TypedDict):
    """
    This class describes the basic structure of the dictionary we expect to receive
    from `initialize_application`. Ideally we'd use a more sophisticated data validation
    library to deserialize the data we receive back from Fireball. There are
    multiple potential solutions (libraries) for this and all are fairly complex - we
    don't want to spend time right now evaluating each of them. For now though, a
    TypedDict gives us basic type hints for top-level keys and values.
    """

    app_id: int
    common_config: Dict
    init_options: Dict
    teamserver_status: str
    teamserver_settings: Optional[Dict]
    archived_date: Optional[str]


def initialize_application(
    init_options: InitOptions,
) -> BindingApiSuccess[InitAppSettings]:
    """
    This should be the first call from an application to Fireball to populate all of the
    agent-provided parameters required for teamserver communication.

    The app_id in the returned dictionary should be used for all other reporting calls.
    It will be used to differentiate between different applications in the same process.

    Calling init on an already initialized application will simply return the currently
    known agent settings.

    Calling init on an application which has already been shut down will start the
    application again on teamserver and return its settings. A new app_id will be
    generated for the restarted application.
    """
    init_options_bytes = init_options._to_json_bytes()
    result = MustFreeBuffer()
    result_size = c_uint()
    messages = c_uint()
    return_status: int = libfireball_c.initialize_application(
        API_VERSION,
        JSON_FORMAT,
        init_options_bytes,
        len(init_options_bytes),
        byref(result),
        byref(result_size),
        byref(messages),
    )
    assert_ok(return_status)
    result_dict: InitAppSettings = (
        json.loads(result.value[: result_size.value])
        if result.value is not None
        else {}
    )

    return BindingApiSuccess(messages=AgentMessages(messages.value), data=result_dict)


class InstanceInfo(TypedDict):
    """
    InstanceInfo describes static information about the loaded Fireball library.
    """

    reporting_instance_id: str
    """
    Reporting instance ID of the current process. This a new UUID created during
    the process. It will be reported as the X-Contrast-Reporting-Instance header
    to all TeamServer calls.
    """

    crate_version: str
    """
    Version of the fireball crate used for this build.
    """

    git_tag: str
    """
    git tag of this fireball release.
    """


def get_info() -> InstanceInfo:
    """
    Get static fireball api information. This api is safe to call anytime, even
    without initializing any applications.
    """

    result = MustFreeBuffer()
    result_size = c_uint()

    return_status: int = libfireball_c.get_info(
        API_VERSION,
        JSON_FORMAT,
        byref(result),
        byref(result_size),
    )
    assert_ok(return_status)
    result_dict: InstanceInfo = (
        json.loads(result.value[: result_size.value])
        if result.value is not None
        else {}
    )

    return result_dict


libfireball_c.get_info.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    POINTER(c_char_p),  # result
    POINTER(c_uint),  # result_size
]
libfireball_c.get_info.restype = c_int


@dataclass(frozen=True)
class DiscoveredRoute:
    """
    Describes a route handler registered by the application.

    This is similar to an ObservedRoute, but adds a field for
    reporting the application framework (since route discovery
    requires framework support) and makes the URL optional
    (since there isn't a concrete request being observed and
    the route may be registered for a general URL pattern).
    """

    framework: str
    """
    The application framework that registered the route handler.
    """

    signature: str
    """
    The signature of the route handler.
    """

    url: Optional[str]
    """
    The concrete, normalized URL of the request that matches
    this route.
    """

    verb: Optional[str]
    """
    The HTTP verb used by the route handler.

    If None, the route handler is assumed to handle all verbs.
    """


def new_discovered_routes(
    app_id: int, routes: List[DiscoveredRoute]
) -> BindingApiSuccess[None]:
    """
    Report discovered routes.

    If an exception is raised, then no routes are reported.
    """
    discovered_routes_bytes = json.dumps([asdict(route) for route in routes]).encode(
        "utf-8"
    )
    messages = c_uint()

    return_status: int = libfireball_c.new_discovered_routes(
        API_VERSION,
        JSON_FORMAT,
        app_id,
        discovered_routes_bytes,
        len(discovered_routes_bytes),
        byref(messages),
    )

    assert_ok(return_status)
    return BindingApiSuccess(messages=AgentMessages(messages.value), data=None)


libfireball_c.new_discovered_routes.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_uint,  # app_id
    c_char_p,  # routes_buf
    c_uint,  # routes_buf_len
    POINTER(c_uint),  # messages
]
libfireball_c.new_discovered_routes.restype = c_int


# We'd like StrEnum here, but it's only available in python 3.11. Inheriting from
# str allows us to easily serialize this with `json.dumps`.
class SourceType(str, enum.Enum):
    """
    The type of the source of the data.
    """

    BODY = "BODY"
    BROKER_MESSAGE = "BROKER_MESSAGE"
    CANARY_DATABASE = "CANARY_DATABASE"
    COOKIE = "COOKIE"
    COOKIE_KEY = "COOKIE_KEY"
    HEADER = "HEADER"
    HEADER_KEY = "HEADER_KEY"
    HEADER_MAP = "HEADER_MAP"
    JMS_MESSAGE = "JMS_MESSAGE"
    JWS_MESSAGE = "JWS_MESSAGE"
    MATRIX_PARAMETER = "MATRIX_PARAMETER"
    MULTIPART = "MULTIPART"
    MULTIPART_CONTENT_DATA = "MULTIPART_CONTENT_DATA"
    MULTIPART_FILE_NAME = "MULTIPART_FILE_NAME"
    MULTIPART_FORM_DATA = "MULTIPART_FORM_DATA"
    MULTIPART_HEADER = "MULTIPART_HEADER"
    MULTIPART_HEADER_KEY = "MULTIPART_HEADER_KEY"
    MULTIPART_PARAMETER = "MULTIPART_PARAMETER"
    MULTIPART_PARAMETER_KEY = "MULTIPART_PARAMETER_KEY"
    MULTIPART_PART_NAME = "MULTIPART_PART_NAME"
    OTHER = "OTHER"
    PARAMETER = "PARAMETER"
    PARAMETER_KEY = "PARAMETER_KEY"
    PATH_PARAMETER = "PATH_PARAMETER"
    QUERYSTRING = "QUERYSTRING"
    RABBITMQ_MESSAGE = "RABBITMQ_MESSAGE"
    RMI_MESSAGE = "RMI_MESSAGE"
    RPC_MESSAGE = "RPC_MESSAGE"
    SERVER_VARIABLE = "SERVER_VARIABLE"
    SESSION_ID = "SESSION_ID"
    SOCKET = "SOCKET"
    TAINTED_DATABASE = "TAINTED_DATABASE"
    URI = "URI"
    WEBSERVICE_BODY = "WEBSERVICE_BODY"
    WEBSERVICE_HEADER = "WEBSERVICE_HEADER"
    WEBSOCKET = "WEBSOCKET"


@dataclass(frozen=True)
class RouteSource:
    """
    A dataflow source event observed within a route handler.
    """

    type: SourceType
    name: Optional[str] = None


@dataclass(frozen=True)
class ObservedRoute:
    signature: str
    """
    The signature of the route that handled the current request.
    """

    verb: Optional[str]
    """
    The HTTP verb of the current request.
    """

    url: str
    """
    The concrete, normalized URL of the current request.
    """

    sources: List[RouteSource]
    """
    The Assess sources retrieved while processing the current request.
    """

    def _to_json_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


def new_observed_route(app_id: int, route: ObservedRoute) -> BindingApiSuccess[None]:
    """
    Record an observed route.

    Routes are reported periodically in batches. This endpoint can be called multiple
    times for the same route, but Fireball will only report duplicate routes at a rate
    of once per minute to avoid overloading TeamServer. The caller can implement this
    same throttling on its side to improve performance and avoid sending duplicate
    routes to Fireball.
    """
    observed_route_bytes = route._to_json_bytes()
    messages = c_uint()

    return_status: int = libfireball_c.new_observed_route(
        API_VERSION,
        JSON_FORMAT,
        app_id,
        observed_route_bytes,
        len(observed_route_bytes),
        byref(messages),
    )

    assert_ok(return_status)
    return BindingApiSuccess(messages=AgentMessages(messages.value), data=None)


libfireball_c.new_observed_route.argtypes = [
    c_uint32,  # version
    c_uint32,  # format
    c_uint,  # app_id
    c_char_p,  # observed_route_buf
    c_uint,  # observed_route_buf_len
    POINTER(c_uint),  # messages
]
libfireball_c.new_observed_route.restype = c_int


def assert_ok(return_status: int) -> None:
    """
    Assert that a call to a fireball C API function was successful, and raise
    an Error if it was not.

    Errors are translated into different exception types based on the return code.

    The Error will contain the error message and stack trace from the last error
    that occurred in the fireball C API.
    """
    if return_status == 0:
        return

    Exc = RETURN_CODES_TO_EXCEPTIONS.get(return_status, UnexpectedError)

    error_message_length = libfireball_c.last_error_message_length()
    error_message = create_string_buffer(error_message_length)

    error_stack_length = libfireball_c.last_error_stack_length()
    error_stack = create_string_buffer(error_stack_length)

    last_error_message_return_status = libfireball_c.last_error_message(
        error_message, error_message_length, error_stack, error_stack_length
    )
    # Make sure not to recursively call assert_ok because it could
    # cause infinite recursion.
    if last_error_message_return_status < 0:
        raise UnexpectedError(
            "An error occurred, but the error message could not be retrieved. "
            "See the reporter logs for more information.",
            stack="",
        )

    raise Exc(error_message.value.decode(), error_stack.value.decode())


@dataclass
class Error(Exception):
    """
    An error that occurred in the fireball C API.
    """

    message: str
    stack: str


class Panic(Error):
    """
    There was an unhandled panic in the fireball code.

    This should never happen and should be considered a bug.
    """

    ...


class ArgumentValidationError(Error):
    """
    Indicates invalid arguments were passed to the api call.

    This could be improper formatting, non-existen app_id, bad serialization,
    or missing required fields.  This error indicates an agent bug.
    """

    ...


class AppArchivedError(Error):
    """
    Indicates that the application has been archived on TeamServer.

    The agent should stop reporting data for this application, or re-initialize
    it if it thinks it has been unarchived.
    """

    ...


class AuthenticationError(Error):
    """
    The TeamServer authentication credentials are wrong or expired.

    The agent shoulds stop reporting data until the credentials are updated.
    """

    ...


class TeamServerError(Error):
    """
    An unhandled error from TeamServer.

    It should not normally occur. This error indicate a broken connection to
    the server and some other invalid state. Read the details for more information.
    """

    ...


class ConfigurationError(Error):
    """
    Indicates a configuration error in the Contrast agent.

    This could be a missing configuration file, a bad configuration file,
    or a configuration file that is not readable.
    """

    ...


class UnexpectedError(Error):
    """
    Any other unexpected error in the Fireball client, such as when parsing responses
    or configuration.

    This should never happen and may indicate a bug.
    """

    ...


RETURN_CODES_TO_EXCEPTIONS: Dict[int, Type[Error]] = {
    1: Panic,
    2: ArgumentValidationError,
    3: AppArchivedError,
    4: AuthenticationError,
    5: TeamServerError,
    6: ConfigurationError,
    7: UnexpectedError,
}

libfireball_c.last_error_message.argtypes = [
    POINTER(c_char),  # message_buffer
    c_int,  # message_length
    POINTER(c_char),  # stack_buffer
    c_int,  # stack_length
]
libfireball_c.last_error_message.restype = c_int

libfireball_c.last_error_message_length.argtypes = []
libfireball_c.last_error_message_length.restype = c_int

libfireball_c.last_error_stack_length.argtypes = []
libfireball_c.last_error_stack_length.restype = c_int
