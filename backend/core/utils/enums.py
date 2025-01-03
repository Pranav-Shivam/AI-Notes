from enum import Enum
from typing import Final, NamedTuple, List

# Enums for CouchDB user fields
class CouchDBUserFields(Enum):
    USER_ID = "user_id"
    USERNAME = "username"
    EMAIL = "email"
    PASSWORD_HASH = "password_hash"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    ROLES = "roles"
    STATUS = "status"
    METADATA = "metadata"
    FULL_NAME = "full_name"
    PROFILE_PICTURE_URL = "profile_picture_url"
    LAST_LOGIN = "last_login"

# Enums for CouchDB document fields
class CouchDBDocumentFields(Enum):
    DOCUMENT_ID = "document_id"
    NAME = "document_name"
    SOURCE = "document_src"
    DATE_TIME = "date_time"
    EXTENSION = "extension"
    TYPE = "document_type"
    TEXT = "document_text"
    OWNER_ID = "owner_id"
    TAGS = "tags"
    PERMISSIONS = "permissions"
    METADATA = "metadata"
    AUTHOR = "author"
    SOURCE_URL = "source_url"
    FILE_SIZE = "file_size"
    READ_ACCESS = "read"
    WRITE_ACCESS = "write"

# Enums for CouchDB tag fields
class CouchDBTagFields(Enum):
    TAG_ID = "tag_id"
    DOCUMENT_ID = "document_id"
    DATE_TIME = "date_time"
    TAG = "tag"
    OWNER_ID = "owner_id"

# Enums for CouchDB section fields
class CouchDBSectionFields(Enum):
    SECTION_ID = "section_id"
    DOCUMENT_ID = "document_id"
    DATE_TIME = "date_time"
    SECTION = "section"
    TOKEN_COUNT = "token_count"
    TAGS = "tags"
    EMBEDDINGS_VERSION = "embeddings_version"
    OWNER_ID = "owner_id"

# Enums for CouchDB question fields
class CouchDBQuestionFields(Enum):
    QUESTION_ID = "question_id"
    DOCUMENT_ID = "document_id"
    THREAD_ID = "thread_id"
    DATE_TIME = "date_time"
    QUESTION = "question"
    ANSWER = "answer"
    TAGS = "tags"
    RELATED_SECTION_IDS = "related_section_ids"
    OWNER_ID = "owner_id"
    METADATA = "metadata"
    SOURCE = "source"
    CONTEXT = "context"

# Enums for CouchDB thread fields
class CouchDBThreadFields(Enum):
    THREAD_ID = "thread_id"
    USER_ID = "user_id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
    STATUS = "status"
    TAGS = "tags"
    MESSAGES = "messages"
    PERMISSIONS = "permissions"
    METADATA = "metadata"
    TOTAL_MESSAGES = "total_messages"
    AVG_RESPONSE_TIME_MS = "average_response_time_ms"
    CONTEXT = "context"
    PRIORITY = "priority"

# Enums for CouchDB message fields
class CouchDBMessageFields(Enum):
    MESSAGE_ID = "message_id"
    TIMESTAMP = "timestamp"
    SENDER = "sender"
    CONTENT = "content"
    RESPONSE_TIME_MS = "response_time_ms"
    METADATA = "metadata"
    QUERY_TYPE = "query_type"
    RELATED_DOCUMENT_ID = "related_document_id"
    RELATED_SECTION_IDS = "related_section_ids"
    EMBEDDINGS_VERSION = "embeddings_version"

# Enums for Qdrant section fields
class QdrantSectionFields(Enum):
    SECTION_ID = "section_id"
    VECTOR = "vector"
    PAYLOAD = "payload"
    DOCUMENT_ID = "document_id"
    CONTENT = "content"
    TOKEN_COUNT = "token_count"
    TAGS = "tags"
    EMBEDDINGS_VERSION = "embeddings_version"
    OWNER_ID = "owner_id"
    METADATA = "metadata"
    ADDITIONAL_INFO = "additional_info"
    DATABASE_NAME = "sections"
    QUERY_VECTOR_NAME = "text_vector"

# Enums for Qdrant question fields
class QdrantQuestionFields(Enum):
    QUESTION_ID = "question_id"
    VECTOR = "vector"
    PAYLOAD = "payload"
    DOCUMENT_ID = "document_id"
    QUESTION = "question"
    ANSWER = "answer"
    TAGS = "tags"
    RELATED_SECTION_IDS = "related_section_ids"
    EMBEDDINGS_VERSION = "embeddings_version"
    OWNER_ID = "owner_id"
    METADATA = "metadata"
    SOURCE = "source"
    CONTEXT = "context"
    DATABASE_NAME = "questions"
    QUERY_VECTOR_NAME = "text_vector"

# Constants for search parameters
class SearchManagements(Enum):
    SCORE_THRESHOLD = 0.75
    TOP_K = 5
    MIN_SCORE = 0.74

# Constants for token management
class TokenManagements(Enum):
    MAX_TOTAL_TOKENS = 8192
    RESERVED_TOKENS = 1500

# Constants for memory management
class MemoryManagement(Enum):
    MEMORY_THRESHOLD: Final = 100 * 1024 * 1024  # 100MB in bytes
    CHUNK_SIZE: Final = 1024 * 1024  # 1MB in bytes

# Constants for system configuration
class SystemConfigurations(Enum):
    MAX_WORKERS = 4

# Constants for file types
class FileTypes(Enum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    TXT = "txt"

class BotStrategy(Enum):
    NORMAL = "normal"
    DOCUMENT = "document"
    DOCUMENT_THREAD = "document_thread"
    THREAD = "thread"

# Enums for file extensions
class FileExtensions(Enum):
    # Document formats
    PDF = ".pdf"
    DOC = ".doc"
    DOCX = ".docx"
    TXT = ".txt"
    RTF = ".rtf"
    ODT = ".odt"
    PAGES = ".pages"
    
    # Spreadsheet formats
    XLS = ".xls"
    XLSX = ".xlsx"
    CSV = ".csv"
    ODS = ".ods"
    
    # Presentation formats
    PPT = ".ppt"
    PPTX = ".pptx"
    KEY = ".key"
    ODP = ".odp"
    
    # Image formats
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    GIF = ".gif"
    BMP = ".bmp"
    TIFF = ".tiff"
    SVG = ".svg"
    WEBP = ".webp"
    
    # Audio formats
    MP3 = ".mp3"
    WAV = ".wav"
    AAC = ".aac"
    FLAC = ".flac"
    
    # Video formats
    MP4 = ".mp4"
    AVI = ".avi"
    MOV = ".mov"
    WMV = ".wmv"
    MKV = ".mkv"
    
    # Archive formats
    ZIP = ".zip"
    RAR = ".rar"
    TAR = ".tar"
    GZ = ".gz"
    SEVENZ = ".7z"
    
    # Programming and markup
    PY = ".py"
    JS = ".js"
    HTML = ".html"
    CSS = ".css"
    JSON = ".json"
    XML = ".xml"
    MD = ".md"
    
    # Email formats
    EML = ".eml"
    MSG = ".msg"
    
    # Ebook formats
    EPUB = ".epub"
    MOBI = ".mobi"
    AZW = ".azw"

    @classmethod
    def get_document_extensions(cls) -> List[str]:
        return [cls.PDF.value, cls.DOC.value, cls.DOCX.value, cls.TXT.value, 
                cls.RTF.value, cls.ODT.value]

    @classmethod
    def get_image_extensions(cls) -> List[str]:
        return [cls.JPG.value, cls.JPEG.value, cls.PNG.value, cls.GIF.value, 
                cls.BMP.value, cls.TIFF.value, cls.SVG.value, cls.WEBP.value]

    @classmethod
    def get_archive_extensions(cls) -> List[str]:
        return [cls.ZIP.value, cls.RAR.value, cls.TAR.value, cls.GZ.value, 
                cls.SEVENZ.value]

# NamedTuple for HTTP status codes
class HTTPStatusCode(NamedTuple):
    code: int
    message: str

# Enums for HTTP status codes
class HTTPStatus(Enum):
    # 1xx Informational
    CONTINUE = HTTPStatusCode(100, "Continue")
    SWITCHING_PROTOCOLS = HTTPStatusCode(101, "Switching Protocols")
    PROCESSING = HTTPStatusCode(102, "Processing")
    EARLY_HINTS = HTTPStatusCode(103, "Early Hints")

    # 2xx Success
    OK = HTTPStatusCode(200, "OK")
    CREATED = HTTPStatusCode(201, "Created")
    ACCEPTED = HTTPStatusCode(202, "Accepted")
    NON_AUTHORITATIVE_INFORMATION = HTTPStatusCode(203, "Non-Authoritative Information")
    NO_CONTENT = HTTPStatusCode(204, "No Content")
    RESET_CONTENT = HTTPStatusCode(205, "Reset Content")
    PARTIAL_CONTENT = HTTPStatusCode(206, "Partial Content")
    MULTI_STATUS = HTTPStatusCode(207, "Multi-Status")
    ALREADY_REPORTED = HTTPStatusCode(208, "Already Reported")
    IM_USED = HTTPStatusCode(226, "IM Used")

    # 3xx Redirection
    MULTIPLE_CHOICES = HTTPStatusCode(300, "Multiple Choices")
    MOVED_PERMANENTLY = HTTPStatusCode(301, "Moved Permanently")
    FOUND = HTTPStatusCode(302, "Found")
    SEE_OTHER = HTTPStatusCode(303, "See Other")
    NOT_MODIFIED = HTTPStatusCode(304, "Not Modified")
    USE_PROXY = HTTPStatusCode(305, "Use Proxy")
    TEMPORARY_REDIRECT = HTTPStatusCode(307, "Temporary Redirect")
    PERMANENT_REDIRECT = HTTPStatusCode(308, "Permanent Redirect")

    # 4xx Client Errors
    BAD_REQUEST = HTTPStatusCode(400, "Bad Request")
    UNAUTHORIZED = HTTPStatusCode(401, "Unauthorized")
    PAYMENT_REQUIRED = HTTPStatusCode(402, "Payment Required")
    FORBIDDEN = HTTPStatusCode(403, "Forbidden")
    NOT_FOUND = HTTPStatusCode(404, "Not Found")
    METHOD_NOT_ALLOWED = HTTPStatusCode(405, "Method Not Allowed")
    NOT_ACCEPTABLE = HTTPStatusCode(406, "Not Acceptable")
    PROXY_AUTHENTICATION_REQUIRED = HTTPStatusCode(407, "Proxy Authentication Required")
    REQUEST_TIMEOUT = HTTPStatusCode(408, "Request Timeout")
    CONFLICT = HTTPStatusCode(409, "Conflict")
    GONE = HTTPStatusCode(410, "Gone")
    LENGTH_REQUIRED = HTTPStatusCode(411, "Length Required")
    PRECONDITION_FAILED = HTTPStatusCode(412, "Precondition Failed")
    PAYLOAD_TOO_LARGE = HTTPStatusCode(413, "Payload Too Large")
    URI_TOO_LONG = HTTPStatusCode(414, "URI Too Long")
    UNSUPPORTED_MEDIA_TYPE = HTTPStatusCode(415, "Unsupported Media Type")
    RANGE_NOT_SATISFIABLE = HTTPStatusCode(416, "Range Not Satisfiable")
    EXPECTATION_FAILED = HTTPStatusCode(417, "Expectation Failed")
    IM_A_TEAPOT = HTTPStatusCode(418, "I'm a teapot")
    MISDIRECTED_REQUEST = HTTPStatusCode(421, "Misdirected Request")
    UNPROCESSABLE_ENTITY = HTTPStatusCode(422, "Unprocessable Entity")
    LOCKED = HTTPStatusCode(423, "Locked")
    FAILED_DEPENDENCY = HTTPStatusCode(424, "Failed Dependency")
    TOO_EARLY = HTTPStatusCode(425, "Too Early")
    UPGRADE_REQUIRED = HTTPStatusCode(426, "Upgrade Required")
    PRECONDITION_REQUIRED = HTTPStatusCode(428, "Precondition Required")
    TOO_MANY_REQUESTS = HTTPStatusCode(429, "Too Many Requests")
    REQUEST_HEADER_FIELDS_TOO_LARGE = HTTPStatusCode(431, "Request Header Fields Too Large")
    UNAVAILABLE_FOR_LEGAL_REASONS = HTTPStatusCode(451, "Unavailable For Legal Reasons")

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = HTTPStatusCode(500, "Internal Server Error")
    NOT_IMPLEMENTED = HTTPStatusCode(501, "Not Implemented")
    BAD_GATEWAY = HTTPStatusCode(502, "Bad Gateway")
    SERVICE_UNAVAILABLE = HTTPStatusCode(503, "Service Unavailable")
    GATEWAY_TIMEOUT = HTTPStatusCode(504, "Gateway Timeout")
    HTTP_VERSION_NOT_SUPPORTED = HTTPStatusCode(505, "HTTP Version Not Supported")
    VARIANT_ALSO_NEGOTIATES = HTTPStatusCode(506, "Variant Also Negotiates")
    INSUFFICIENT_STORAGE = HTTPStatusCode(507, "Insufficient Storage")
    LOOP_DETECTED = HTTPStatusCode(508, "Loop Detected")
    NOT_EXTENDED = HTTPStatusCode(510, "Not Extended")
    NETWORK_AUTHENTICATION_REQUIRED = HTTPStatusCode(511, "Network Authentication Required")

    @classmethod
    def is_informational(cls, code: int) -> bool:
        return 100 <= code < 200

    @classmethod
    def is_success(cls, code: int) -> bool:
        return 200 <= code < 300

    @classmethod
    def is_redirect(cls, code: int) -> bool:
        return 300 <= code < 400

    @classmethod
    def is_client_error(cls, code: int) -> bool:
        return 400 <= code < 500

    @classmethod
    def is_server_error(cls, code: int) -> bool:
        return 500 <= code < 600

    @classmethod
    def get_status_message(cls, code: int) -> str:
        for status in cls:
            if status.value.code == code:
                return status.value.message
        return "Unknown Status Code"
