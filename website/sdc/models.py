# -*- coding: utf-8 -*-
"""
==========
sdc.models
==========

Persistent model for the student demo cup.

"""
import datetime
from abilian.core.entities import Entity
from sqlalchemy import (
    UnicodeText, Column, DateTime, Enum
)

from .common import THEMES

class SDCApplication(Entity):
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    theme = Column(UnicodeText, nullable=False, default=unicode(THEMES[0], encoding='utf-8'))
    leader = Column(UnicodeText, nullable=False)
    prenom = Column(UnicodeText, nullable=False)
    email = Column(UnicodeText, unique=True, nullable=False)
    telephone = Column(UnicodeText, nullable=False)
    organization = Column(UnicodeText, default=u"", nullable=False)
    intervenants = Column(UnicodeText, default=u"", nullable=False)
    summary = Column(UnicodeText, default=u"", nullable=False)

    @property
    def _name(self):
        return self.email
