from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Tls:
    certfp: str = None
    cipher: str = None

@dataclass
class Geoip:
    country_code: str = None
    asn: str = None
    asname: str = None

@dataclass
class UserChannel:
    name: str = None
    level: str = None

@dataclass
class User:
    username: str = None
    realname: str = None
    vhost: str = None
    cloakedhost: str = None
    servername: str = None
    account: str = None
    reputation: int = None
    security_groups: list[str] = field(default_factory=list)
    modes: str = None
    snomasks: str = None
    operlogin: str = None
    operclass: str = None
    channels: list[UserChannel] = field(default_factory=list[UserChannel])

@dataclass
class ServerFeatures:
    software: str = None
    protocol: int = 0
    usermodes: str = None
    chanmodes: list[str] = field(default_factory=list)
    nick_character_sets: str = None

@dataclass
class Server:
    info: str = None
    num_users: int = 0
    boot_time: str = None
    synced: int = 0
    features: ServerFeatures = field(default_factory=ServerFeatures)

@dataclass
class Client:
    name: str = None
    id: str = None
    hostname: str = None
    ip: str = None
    details: str = None
    geoip: Geoip = field(default_factory=Geoip)
    server_port: int = 0
    client_port: int = 0
    connected_since: str = None
    idle_since: str = None
    tls: Tls = field(default_factory=Tls)
    user: User = field(default_factory=User)
    server: Server = field(default_factory=Server)

@dataclass
class ChannelBans:
    name: str = None
    set_by: str = None
    set_at: str = None

@dataclass
class ChannelBanExemptions:
    name: str = None
    set_by: str = None
    set_at: str = None

@dataclass
class ChannelInviteExceptions:
    name: str = None
    set_by: str = None
    set_at: str = None

@dataclass
class ChannelMembers:
    level: str = None
    name: str = None
    id: str = None
    hostname: str = None
    ip: str = None
    details: str = None
    geoip: Geoip = field(default_factory=Geoip)

@dataclass
class Channel:
    name: str = None
    creation_time: str = None
    num_users: int = 0
    topic: str = None
    topic_set_by: str = None
    topic_set_at: str = None
    modes: str = None
    bans: List[ChannelBans] = field(default_factory=list[ChannelBans])
    ban_exemptions: List[ChannelBanExemptions] = field(default_factory=list[ChannelBanExemptions])
    invite_exceptions: List[ChannelInviteExceptions] = field(default_factory=list[ChannelInviteExceptions])
    members: List[ChannelMembers] = field(default_factory=list[ChannelMembers])