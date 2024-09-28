from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ...random.random_str import secret_token


class TokenMixin:
    token: Mapped[Optional[str]] = mapped_column(unique=True, default=secret_token)
