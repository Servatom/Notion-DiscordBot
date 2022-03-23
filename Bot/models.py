import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean
from database import Base
from sqlalchemy.sql.sqltypes import BigInteger


try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"

class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(BigInteger, index=True, nullable=False)
    notion_api_key = Column(String, nullable=False)
    notion_db_id = Column(String, nullable=False)
    tag = Column(Boolean, default=False)
    prefix = Column(String, default=PREFIX)

    def __init__(self, guild_id, notion_api_key, notion_db_id, tag, prefix=PREFIX):
        self.guild_id = guild_id
        self.notion_api_key = notion_api_key
        self.notion_db_id = notion_db_id
        self.tag = tag
        self.prefix = prefix

    @property
    def serialize(self):
        return {
            "guild_id": self.guild_id,
            "notion_api_key": self.notion_api_key,
            "notion_db_id": self.notion_db_id,
            "tag": self.tag,
            "prefix": self.prefix,
        }
