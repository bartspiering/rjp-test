from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from .user import User
from .character import Character
from .potion import Potion
from .character_potion import CharacterPotion
from .spell import Spell
from .character_spell import CharacterSpell


__all__ = ["User", "Character", "Potion", "CharacterPotion", "Spell", "CharacterSpell"]
