from datetime import datetime
from zoneinfo import ZoneInfo

from app import bcrypt


def gerar_hash_senha(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")


def verificar_hash_senha(password_hash, password):
    if isinstance(password_hash, bytes):
        password_hash = password_hash.decode("utf-8")

    if isinstance(password_hash, str) and password_hash.startswith("\\x"):
        password_hash = bytes.fromhex(password_hash[2:]).decode("utf-8")

    return bcrypt.check_password_hash(password_hash, password)


def agora_brasil():
    return datetime.now(ZoneInfo("America/Sao_Paulo")).replace(tzinfo=None)
