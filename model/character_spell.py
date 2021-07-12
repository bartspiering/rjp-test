from . import db


class CharacterSpell(db.Model):
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.id"), primary_key=True
    )
    character = db.relationship("Character", back_populates="spells")

    spell_id = db.Column(db.Integer, db.ForeignKey("spell.id"), primary_key=True)
    spell = db.relationship("Spell", back_populates="characters")
