from .register import RegisterResource
from .login import LoginResource

from .character import CharacterResource
from .character_list import CharacterListResource

from .character_potion import CharacterPotionResource
from .character_potion_list import CharacterPotionListResource

from .character_spell import CharacterSpellResource
from .character_spell_list import CharacterSpellListResource

from .spell import SpellResource
from .spell_list import SpellListResource

from .potion import PotionResource
from .potion_list import PotionListResource


__all__ = [
    "RegisterResource",
    "LoginResource",
    "CharacterResource",
    "CharacterListResource",
    "CharacterPotionResource",
    "CharacterPotionListResource",
    "CharacterSpellResource",
    "CharacterSpellListResource",
    "SpellResource",
    "SpellListResource",
    "PotionResource",
    "PotionListResource",
]
