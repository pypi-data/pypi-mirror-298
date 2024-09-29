from __future__ import annotations

from typing import List

from .base import BaseSession

sessions_class: List[type[BaseSession]] = []
sessions_names: List[str] = []

from .birefnet_general import BiRefNetSessionGeneral

sessions_class.append(BiRefNetSessionGeneral)
sessions_names.append(BiRefNetSessionGeneral.name())

from .u2net import U2netSession

sessions_class.append(U2netSession)
sessions_names.append(U2netSession.name())

from .u2netp import U2netpSession

sessions_class.append(U2netpSession)
sessions_names.append(U2netpSession.name())
