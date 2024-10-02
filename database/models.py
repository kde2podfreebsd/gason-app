from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, constr
from typing import List, Optional

class QRCodeType(Enum):
    URL = "url"
    FILE = "file"

@dataclass
class User:
    chatid: int
    username: str
    first_name: Optional[str]
    second_name: Optional[str]
    phone: Optional[str]
    qrcode_path: Optional[str]

@dataclass
class Admin:
    chatid: int
    username: str
    qr_code_background: str
    qr_code_type: QRCodeType

@dataclass
class Event:
    text: str
    inst_post_url: str
    tg_post_url: str
    button_text: str
    admin_chatid: int  # Связка с админом
    files: List[str]
