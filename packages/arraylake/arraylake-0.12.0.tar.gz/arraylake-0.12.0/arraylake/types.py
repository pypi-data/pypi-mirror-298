from __future__ import annotations

import sys
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum, IntEnum
from typing import Annotated, Any, Literal, NewType, Optional, Union
from uuid import UUID

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    ConfigDict,
    EmailStr,
    EncodedBytes,
    EncoderProtocol,
    Field,
    SecretStr,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)
from typing_extensions import TypedDict

if sys.version_info >= (3, 11):
    # python 3.11+
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        pass


# default factories
def utc_now():
    # drop microseconds because bson does not support them
    return datetime.now(timezone.utc).replace(microsecond=0)


class DBIDBytes(bytes):
    def __str__(self) -> str:
        """Format as hex digits"""
        return self.hex()

    def __repr__(self):
        return str(self)


class DBIDEncoder(EncoderProtocol):
    @classmethod
    def decode(cls, v: Any) -> DBIDBytes:
        return to_dbid_bytes(v)

    @classmethod
    def encode(cls, v: bytes) -> bytes:
        return v

    @classmethod
    def get_json_format(cls) -> str:
        return "dbid-encoder"


DBID = Annotated[DBIDBytes, EncodedBytes(encoder=DBIDEncoder)]


# These are type aliases, which allow us to write e.g. Path instead of str. Since they can be used interchangeably,
# I'm not sure how useful they are.

CommitID = DBID
CommitIDHex = str
Path = str
MetastoreUrl = Union[AnyUrl, AnyHttpUrl]

# These are used by mypy in static typing to ensure logical correctness but cannot be used at runtime for validation.
# They are more strict than the aliases; they have to be explicitly constructed.

SessionID = NewType("SessionID", str)
TagName = NewType("TagName", str)
BranchName = NewType("BranchName", str)

CommitHistory = Iterator[CommitID]


class BulkCreateDocBody(BaseModel):
    session_id: SessionID
    content: Mapping[str, Any]
    path: Path


class CollectionName(StrEnum):
    sessions = "sessions"
    metadata = "metadata"
    chunks = "chunks"
    nodes = "nodes"


class ChunkHash(TypedDict):
    method: str
    token: str


class SessionType(StrEnum):
    read_only = "read"
    write = "write"


# validators
def to_dbid_bytes(v: Any) -> DBIDBytes:
    if isinstance(v, str):
        return DBIDBytes.fromhex(v)
    if isinstance(v, bytes):
        return DBIDBytes(v)
    if hasattr(v, "binary"):
        return DBIDBytes(v.binary)
    raise ValueError("Invalid DBID object")


def datetime_to_isoformat(v: datetime) -> str:
    return v.isoformat()


class SessionBase(BaseModel):
    # NOTE: branch is Optional to accommodate workflows where a particular
    # commit is checked out.
    branch: Optional[BranchName] = None
    base_commit: Optional[CommitID] = None
    # TODO: Do we bite the bullet and replace all these author_name/author_email
    # properties with principal_id?
    author_name: Optional[str] = None
    author_email: EmailStr
    message: Optional[str] = None
    session_type: SessionType

    @field_validator("base_commit", mode="before")
    @classmethod
    def validate_base_commit(cls, id: Any) -> Optional[DBIDBytes]:
        return to_dbid_bytes(id) if id is not None else None

    @field_serializer("base_commit")
    def serialize_base_commit(self, base_commit: Optional[CommitID]) -> Optional[CommitIDHex]:
        if base_commit is not None:
            return str(base_commit)
        else:
            return None

    @model_validator(mode="before")
    @classmethod
    def _one_of_branch_or_commit(cls, values):
        if not values.get("branch") and not values.get("base_commit"):
            raise ValueError("At least one of branch or base_commit must not be None")
        return values


class NewSession(SessionBase):
    expires_in: timedelta


class SessionInfo(SessionBase):
    id: SessionID = Field(alias="_id")
    start_time: datetime
    expiration: datetime

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class SessionExpirationUpdate(BaseModel):
    session_id: SessionID
    expires_in: timedelta


class ModelWithID(BaseModel):
    id: DBID = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, id: Any) -> DBIDBytes:
        return to_dbid_bytes(id)

    @field_serializer("id")
    def serialize_id(self, id: DBID) -> str:
        return str(id)


class RepoCreateBody(BaseModel):
    name: str
    description: Optional[str] = None
    bucket_nickname: Optional[str] = None


# Used for `/orgs/{org}/{repo}/visibility` endpoint
class RepoVisibilityModel(BaseModel):
    """The visibility of a repo"""

    visibility: RepoVisibility


class RepoVisibility(str, Enum):
    # PRIVATE: Visible only to repo members.
    # NOTE: Currently, this means any member of an org.
    PRIVATE = "PRIVATE"

    # AUTHENTICATED_PUBLIC: Visible to any authenticated user of Arraylake.
    AUTHENTICATED_PUBLIC = "AUTHENTICATED_PUBLIC"

    # PUBLIC: Visible to anybody on the public internet.
    # PUBLIC = "PUBLIC"


Platform = Literal["s3", "s3-compatible", "minio", "gs"]


# TODO: Rename this to role_based_access_delegation
class CustomerManagedRoleAuth(BaseModel):
    method: Literal["customer_managed_role"]
    external_customer_id: str
    external_role_name: str
    shared_secret: Optional[str] = None


# NOTE: Deprecating HMAC and bucket policy methods
class BucketPolicyAuth(BaseModel):
    method: Literal["bucket_policy"]


# NOTE: Deprecating HMAC and bucket policy methods
class HmacAuth(BaseModel):
    method: Literal["hmac"]
    # NOTE: Once written, credential secrets are not included in the response.
    access_key_id: SecretStr = Field(exclude=True)
    secret_access_key: SecretStr = Field(exclude=True)

    @field_serializer("access_key_id", "secret_access_key", when_used="json")
    def dump_secret(self, v):
        return v.get_secret_value()


# TODO: Rename to Self Managed
class AnonymousAuth(BaseModel):
    method: Literal["anonymous"]


AuthConfig = Union[CustomerManagedRoleAuth, BucketPolicyAuth, HmacAuth, AnonymousAuth]


class Bucket(BaseModel):
    id: UUID
    nickname: str
    platform: Platform
    name: str
    created: datetime = Field(default_factory=utc_now)
    updated: datetime
    created_by: Optional[EmailStr] = None
    prefix: str = ""
    extra_config: Mapping[str, Union[str, bool]]

    # NOTE: To prevent credential leakage, we don't share the auth_config here.

    @model_validator(mode="before")
    @classmethod
    def set_initial_updated(cls, data: Any) -> Any:
        if isinstance(data, dict) and "updated" not in data:
            data["updated"] = data.get("created", utc_now())
        return data

    @field_validator("created", "updated")
    @classmethod
    def timestamp_in_utc_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=timezone.utc)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)


class NewBucket(BaseModel):
    nickname: str
    platform: Platform
    name: str
    prefix: str = ""  # default for compatibility with older data
    extra_config: Mapping[str, Union[str, bool]]
    auth_config: AuthConfig = Field(discriminator="method")

    @model_validator(mode="after")
    def _validate_bucket_options(self):
        if self.platform in ["s3"]:  # TODO: decide if the same is needed for gs buckets
            if "region_name" not in self.extra_config:
                raise ValueError("S3 buckets require a region_name.")
        if self.platform == "s3-compatible":
            if "endpoint_url" not in self.extra_config:
                raise ValueError("S3-compatible buckets require an endpoint_url.")
        return self

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        # NOTE: S3 and GCS have fairly strict naming rules so we can mostly rely on them here.
        # Our checks are meant to make sure the data we receive is valid.
        if " " in name:
            raise ValueError("Bucket name must not contain spaces.")
        if "://" in name:
            raise ValueError("Bucket name must not contain schemes.")
        if "/" in name:
            raise ValueError("Bucket name must not contain slashes.")
        if len(name) < 3:
            raise ValueError("Bucket name must be at least 3 characters long.")
        return name

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, prefix: str) -> str:
        if prefix == "":
            return prefix
        # Remove leading and trailing whitespace.
        prefix = prefix.strip()
        if " " in prefix:
            raise ValueError("Bucket prefix must not contain spaces.")
        if len(prefix) > 900:  # S3 max key size minus some buffer for key
            raise ValueError("Bucket prefix must be at most 900 characters long.")
        if prefix.startswith("/") or prefix.endswith("/"):
            raise ValueError("Bucket prefix must not start or end with a slash.")
        return prefix

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, nickname: str) -> str:
        # Remove leading and trailing whitespace.
        nickname = nickname.strip()

        # NOTE: We only impose a limit on string size. This is intended to be a
        # human-friendly identifier, so we're looser than e.g. S3 regarding
        # naming conventions and restrictions.
        if len(nickname) < 3:
            raise ValueError("Bucket nickname must be at least 3 characters long.")
        if len(nickname) > 64:
            raise ValueError("Bucket nickname must be at most 64 characters long.")
        return nickname

    @field_validator("auth_config")
    @classmethod
    def validate_auth_config(cls, auth_config: AuthConfig | None) -> AuthConfig | None:
        if auth_config and auth_config.method not in ["customer_managed_role", "anonymous"]:
            # Deprecating HMAC and bucket policy methods
            raise ValueError("Bucket auth config method must be Anonymous or Customer Managed Role")
        return auth_config if auth_config else None

    def region_name(self) -> str | None:
        region = self.extra_config.get("region_name")
        return str(region) if region else None


class BucketModifyRequest(BaseModel):
    """A request with optional fields to modify a bucket's config on a per-field
    basis."""

    nickname: str | None = None
    platform: Platform | None = None
    name: str | None = None
    prefix: str | None = None
    extra_config: dict[str, Any] | None = None
    auth_config: AuthConfig | None = None

    @field_validator("auth_config")
    @classmethod
    def validate_auth_config(cls, auth_config: AuthConfig | None) -> AuthConfig | None:
        if auth_config and auth_config.method not in ["customer_managed_role", "anonymous"]:
            # Deprecating HMAC and bucket policy methods
            raise ValueError("Bucket auth config method must be Anonymous or Customer Managed Role")
        return auth_config if auth_config else None


class BucketResponse(Bucket):
    is_default: bool
    auth_config: AuthConfig | None = None


class RepoOperationMode(StrEnum):
    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class NewRepoOperationStatus(BaseModel):
    mode: RepoOperationMode
    message: str | None = None


class RepoOperationStatusResponse(NewRepoOperationStatus):
    initiated_by: dict
    estimated_end_time: datetime | None = None


class LegacyBucketResponse(Bucket):
    """Bucket Response object for older clients using auth_method in place of auth_config"""

    is_default: bool
    auth_method: str


class Repo(ModelWithID):
    org: str
    name: str
    created: datetime = Field(default_factory=utc_now)
    updated: datetime
    description: Optional[str] = None
    created_by: Optional[UUID] = None
    visibility: RepoVisibility = RepoVisibility.PRIVATE
    bucket: BucketResponse | LegacyBucketResponse | None = None
    status: RepoOperationStatusResponse

    def _asdict(self):
        """custom dict method ready to be serialized as json"""
        d = self.model_dump()
        d["id"] = str(d["id"])
        if self.created_by is not None:
            d["created_by"] = str(d["created_by"])
        if d["bucket"]:
            d["bucket"]["id"] = str(d["bucket"]["id"])
        if d["status"]["estimated_end_time"]:
            d["status"]["estimated_end_time"] = datetime_to_isoformat(d["status"]["estimated_end_time"])
        return d

    def __repr__(self):
        return f"<Repo {self.org}/{self.name} created at {self.created} by {self.created_by}. Last updated at {self.updated}>"

    @model_validator(mode="before")
    @classmethod
    def set_initial_updated(cls, data: Any) -> Any:
        if isinstance(data, dict) and "updated" not in data:
            data["updated"] = data.get("created", utc_now())
        return data

    @field_validator("created", "updated")
    @classmethod
    def timestamp_in_utc_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=timezone.utc)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)


class Author(BaseModel):
    name: Optional[str] = None
    email: EmailStr

    # TODO: Harmonize this with Commit.author_entry() for DRY.
    def entry(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        else:
            return f"<{self.email}>"


class NewCommit(BaseModel):
    session_id: SessionID
    session_start_time: datetime
    parent_commit: CommitID | None = None
    commit_time: datetime
    author_name: str | None = None
    author_email: EmailStr
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str

    @field_serializer("parent_commit")
    def serialize_commit_id(self, parent_commit: Optional[CommitID]) -> Optional[CommitIDHex]:
        if parent_commit is not None:
            return str(parent_commit)
        else:
            return None

    @field_validator("parent_commit", mode="before")
    @classmethod
    def validate_parent_commit(cls, id: Any) -> Optional[DBIDBytes]:
        return to_dbid_bytes(id) if id is not None else None

    @field_serializer("commit_time", "session_start_time")
    def serialize_commit_time(self, commit_time: datetime) -> str:
        return datetime_to_isoformat(commit_time)


# TODO: remove duplication with NewCommit. Redefining these attributes works around this error:
# Definition of "Config" in base class "ModelWithID" is incompatible with definition in base class "NewCommit"
class Commit(ModelWithID):
    session_start_time: datetime
    parent_commit: Optional[CommitID] = None
    commit_time: datetime
    author_name: Optional[str] = None
    author_email: EmailStr
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str

    @field_serializer("session_start_time", "commit_time")
    def serialize_session_start_time(self, t: datetime) -> str:
        return datetime_to_isoformat(t)

    @field_validator("parent_commit", mode="before")
    @classmethod
    def validate_parent_commit(cls, id: Any) -> Optional[DBIDBytes]:
        return to_dbid_bytes(id) if id is not None else None

    @field_serializer("parent_commit")
    def serialize_commit_id(self, parent_commit: Optional[CommitID]) -> Optional[CommitIDHex]:
        if parent_commit is not None:
            return str(parent_commit)
        else:
            return None

    def author_entry(self) -> str:
        if self.author_name:
            return f"{self.author_name} <{self.author_email}>"
        else:
            return f"<{self.author_email}>"


class Branch(BaseModel):
    id: BranchName = Field(alias="_id")
    commit_id: CommitID
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @field_validator("commit_id", mode="before")
    @classmethod
    def validate_commit_id(cls, id: CommitID) -> DBIDBytes:
        return to_dbid_bytes(id)

    @field_serializer("commit_id")
    def serialize_commit_id(self, commit_id: CommitID) -> CommitIDHex:
        return str(commit_id)


class NewTag(BaseModel):
    label: TagName
    commit_id: CommitID
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str | None
    author_name: Optional[str] = None
    author_email: EmailStr

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @field_validator("commit_id", mode="before")
    @classmethod
    def validate_commit_id(cls, id: CommitID) -> DBIDBytes:
        return to_dbid_bytes(id)

    @field_serializer("commit_id")
    def serialize_commit_id(self, commit_id: CommitID) -> CommitIDHex:
        return str(commit_id)


class Tag(BaseModel):
    # ---
    # This field exists for backcompat with arraylake<=0.9.5
    # Delete when we don't support those versions
    id: TagName = Field(alias="label")
    # ---

    label: TagName
    created_at: datetime
    commit: Commit
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str | None
    author_name: Optional[str] = None
    author_email: EmailStr

    # ---
    # These fields exist for backcompat with arraylake<=0.9.5
    # Delete when we don't support those versions
    @computed_field  # type: ignore[prop-decorator]
    @property
    def _id(self) -> TagName:
        return self.label

    @computed_field  # type: ignore[prop-decorator]
    @property
    def commit_id(self) -> CommitID:
        return self.commit.id

    @field_validator("commit_id", mode="before")
    @classmethod
    def validate_commit_id(cls, id: CommitID) -> DBIDBytes:
        return to_dbid_bytes(id)

    @field_serializer("commit_id")
    def serialize_commit_id(self, commit_id: CommitID) -> CommitIDHex:
        return str(commit_id)

    # ---

    @field_serializer("created_at")
    def serialize_created_at_time(self, t: datetime) -> str:
        return datetime_to_isoformat(t)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


@dataclass
class DocResponse:
    id: str  # not DBID
    session_id: SessionID
    path: Path
    content: Mapping[str, Any] | None = None
    deleted: bool = False

    def __post_init__(self):
        checks = [
            isinstance(self.id, str),
            # session_id: Cannot use isinstance() with NewType, so we use str
            isinstance(self.session_id, str),
            isinstance(self.path, Path),
            isinstance(self.deleted, bool),
            isinstance(self.content, dict) if self.content else True,
        ]
        if not all(checks):
            raise ValueError(f"Validation failed {self}, {checks}")


class DocSessionsResponse(ModelWithID):
    session_id: SessionID
    deleted: bool = False
    chunksize: int = 0


class SessionPathsResponse(BaseModel):
    id: CommitIDHex = Field(alias="_id")
    path: Path
    deleted: bool = False


class ChunkstoreSchemaVersion(IntEnum):
    # V0 stores the full key as an absolute path in the uri attribute
    V0 = 0
    # V1 stores the hash and session_id (sid) in the manifest, it then creates
    # a relative key as f"{hash}.{sid}"
    V1 = 1


class ReferenceData(BaseModel):
    uri: Optional[str] = None  # will be None in non-virtual new style repos
    offset: int
    length: int
    hash: Optional[ChunkHash] = None
    # Schema version
    v: ChunkstoreSchemaVersion = ChunkstoreSchemaVersion.V0
    # sid (session identifier) should be not None for v > V0
    sid: Optional[SessionID] = None

    @field_validator("v", mode="before")
    @classmethod
    def _resolve_schema_version(cls, v):
        """Old library versions sometimes pass None as the version, ensure it's V0"""
        return v or ChunkstoreSchemaVersion.V0

    @field_serializer("v")
    def _serialize_version(self, v: ChunkstoreSchemaVersion) -> Optional[int]:
        # For compatibility with old clients, we cannot serialize 0 as a version
        # it has to be None
        if v == ChunkstoreSchemaVersion.V0:
            return None
        else:
            return v

    @classmethod
    def new_virtual(cls, for_version: ChunkstoreSchemaVersion, uri: str, offset: int, length: int, sid: SessionID) -> ReferenceData:
        return cls(
            uri=uri,
            offset=offset,
            length=length,
            hash=None,
            v=for_version,
            sid=None if for_version == ChunkstoreSchemaVersion.V0 else sid,
        )

    @classmethod
    def new_inline(cls, for_version: ChunkstoreSchemaVersion, data: str, length: int, hash: ChunkHash, sid: SessionID) -> ReferenceData:
        assert data.startswith("inline://") or data.startswith("base64:"), "Invalid inline data format"
        return cls(
            uri=data,
            offset=0,
            length=length,
            hash=hash,
            v=for_version,
            sid=None if for_version == ChunkstoreSchemaVersion.V0 else sid,
        )

    @classmethod
    def new_materialized_v0(cls, uri: str, length: int, hash: ChunkHash) -> ReferenceData:
        return cls(uri=uri, offset=0, length=length, hash=hash, v=ChunkstoreSchemaVersion.V0, sid=None)

    @classmethod
    def new_materialized_v1(cls, length: int, hash: ChunkHash, sid: SessionID) -> ReferenceData:
        return cls(
            uri=None,
            offset=0,
            length=length,
            hash=hash,
            v=ChunkstoreSchemaVersion.V1,
            sid=sid,
        )

    def is_virtual(self) -> bool:
        return self.hash is None and not (not self.uri)

    def is_inline(self) -> bool:
        return self.hash is not None and not (not self.uri) and self.uri.startswith("inline://")

    def _is_materialized_v0(self) -> bool:
        return self.v == ChunkstoreSchemaVersion.V0 and not (not self.hash) and not (not self.uri) and not self.uri.startswith("inline://")

    def _is_materialized_v1(self) -> bool:
        return self.v == ChunkstoreSchemaVersion.V1 and not self.uri

    def is_materialized(self) -> bool:
        return self._is_materialized_v1() or self._is_materialized_v0()

    @model_validator(mode="after")
    def _validate_one_of_three_types(self):
        cond = [self.is_materialized(), self.is_virtual(), self.is_inline()]
        if cond.count(True) != 1:
            raise ValueError(f"Invalid {type(self).__name__}: must be materialized, inline or virtual")
        return self

    @model_validator(mode="after")
    def _validate_position(self):
        if self.length < 0:
            raise ValueError(f"Invalid {type(self).__name__}: length must be > 0")
        if self.offset < 0:
            raise ValueError(f"Invalid {type(self).__name__}: offset must be > 0")
        return self

    @model_validator(mode="after")
    def _validate_v0(self):
        if self.v == ChunkstoreSchemaVersion.V0:
            if self._is_materialized_v0() and not (self.uri or "")[:5] in ["gs://", "s3://"]:
                raise ValueError(f"Invalid {type(self).__name__}: V0 chunk manifests must have an uri")
            if self.sid is not None:
                raise ValueError(f"Invalid {type(self).__name__}: V0 chunk manifests cannot include an sid")
        return self

    @model_validator(mode="after")
    def _validate_v1(self):
        if self.v == ChunkstoreSchemaVersion.V1:
            if self._is_materialized_v1() and not self.hash:
                raise ValueError(f"Invalid {type(self).__name__}: V1 chunk manifests must have a hash")
            if not self.sid:
                raise ValueError(f"Invalid {type(self).__name__}: V1 chunk manifests must have an sid")
        return self

    @model_validator(mode="after")
    def _validate_virtual(self):
        if self.is_virtual() and self.uri and (self.uri[:5] not in ["gs://", "s3://"]):
            raise ValueError(f"Invalid {type(self).__name__}: virtual chunk manifests must have an S3 uri or GS uri. Got {self.uri}")
        return self


class UpdateBranchBody(BaseModel):
    branch: BranchName
    new_commit: CommitID
    new_branch: bool = False
    base_commit: Optional[CommitID] = None
    # TODO: Make session_id mandatory once all clients are using
    # managed_sessions by default.
    session_id: Optional[SessionID] = None

    @field_validator("new_commit", "base_commit", mode="before")
    @classmethod
    def validate_commit_id(cls, cid: Any) -> Optional[DBIDBytes]:
        return to_dbid_bytes(cid) if cid is not None else None

    @field_serializer("new_commit", "base_commit")
    def serialize_commit_id(self, cid: CommitID) -> Optional[CommitIDHex]:
        if cid is not None:
            return str(cid)
        else:
            return None


class OauthTokensResponse(BaseModel):
    access_token: SecretStr
    id_token: SecretStr
    refresh_token: Optional[SecretStr] = None
    expires_in: int
    token_type: str

    def dict(self, **kwargs) -> dict[str, Any]:
        """custom dict that drops default values"""
        tokens = super().model_dump(**kwargs)
        # special case: drop refresh token if it is None
        if not tokens.get("refresh_token", 1):
            del tokens["refresh_token"]
        return tokens

    @field_serializer("access_token", "id_token", "refresh_token", when_used="unless-none")
    def dump_secret(self, v) -> str:
        if isinstance(v, SecretStr):
            return v.get_secret_value()
        return v


class OauthTokens(OauthTokensResponse):
    refresh_token: SecretStr

    def dict(self, **kwargs) -> dict[str, Any]:
        """custom dict method that decodes secrets"""
        tokens = super().model_dump(**kwargs)
        for k, v in tokens.items():
            if isinstance(v, SecretStr):
                tokens[k] = v.get_secret_value()
        return tokens

    def __hash__(self):
        return hash((self.access_token, self.id_token, self.refresh_token, self.expires_in, self.token_type))


class UserInfo(BaseModel):
    id: UUID
    first_name: Union[str, None] = None
    family_name: Union[str, None] = None
    email: EmailStr

    def as_author(self) -> Author:
        return Author(name=f"{self.first_name} {self.family_name}", email=self.email)


class ApiTokenInfo(BaseModel):
    id: UUID
    client_id: str
    email: EmailStr
    expiration: int

    def as_author(self) -> Author:
        return Author(email=self.email)


class PathSizeResponse(BaseModel):
    path: Path
    number_of_chunks: int
    total_chunk_bytes: int


class Array(BaseModel):
    attributes: dict[str, Any] = {}
    chunk_grid: dict[str, Any] = {}
    chunk_memory_layout: Optional[str] = None
    compressor: Union[dict[str, Any], None] = None
    data_type: Union[str, dict[str, Any], None] = None
    fill_value: Any = None
    extensions: list = []
    shape: Optional[tuple[int, ...]] = None


# Utility to coerce Array data types to string version
def get_array_dtype(arr: Array) -> str:
    import numpy as np

    if isinstance(arr.data_type, str):
        return str(np.dtype(arr.data_type))
    elif isinstance(arr.data_type, dict):
        return str(arr.data_type["type"])
    else:
        raise ValueError(f"unexpected array type {type(arr.data_type)}")


class Tree(BaseModel):
    trees: dict[str, Tree] = {}
    arrays: dict[str, Array] = {}
    attributes: dict[str, Any] = {}

    def _as_rich_tree(self, name: str = "/"):
        from rich.jupyter import JupyterMixin
        from rich.tree import Tree as _RichTree

        class RichTree(_RichTree, JupyterMixin):
            pass

        def _walk_and_format_tree(td: Tree, tree: _RichTree) -> _RichTree:
            for key, group in td.trees.items():
                branch = tree.add(f":file_folder: {key}")
                _walk_and_format_tree(group, branch)
            for key, arr in td.arrays.items():
                dtype = get_array_dtype(arr)
                tree.add(f":regional_indicator_a: {key} {arr.shape} {dtype}")
            return tree

        return _walk_and_format_tree(self, _RichTree(name))

    def __rich__(self):
        return self._as_rich_tree()

    def _as_ipytree(self, name: str = ""):
        from ipytree import Node
        from ipytree import Tree as IpyTree

        def _walk_and_format_tree(td: Tree) -> list[Node]:
            nodes = []
            for key, group in td.trees.items():
                _nodes = _walk_and_format_tree(group)
                node = Node(name=key, nodes=_nodes)
                node.icon = "folder"
                node.opened = False
                nodes.append(node)
            for key, arr in td.arrays.items():
                dtype = get_array_dtype(arr)
                node = Node(name=f"{key} {arr.shape} {dtype}")
                node.icon = "table"
                node.opened = False
                nodes.append(node)
            return nodes

        nodes = _walk_and_format_tree(self)
        node = Node(name=name, nodes=nodes)
        node.icon = "folder"
        node.opened = True
        tree = IpyTree(nodes=[node])

        return tree

    def _repr_mimebundle_(self, **kwargs):
        try:
            _tree = self._as_ipytree(name="/")
        except ImportError:
            try:
                _tree = self._as_rich_tree(name="/")
            except ImportError:
                return repr(self)
        return _tree._repr_mimebundle_(**kwargs)


class UserDiagnostics(BaseModel):
    system: Optional[dict[str, str]] = None
    versions: Optional[dict[str, str]] = None
    config: Optional[dict[str, str]] = None
    service: Optional[dict[str, str]] = None


class S3TempCredentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str


TempCredentials = Union[S3TempCredentials]
