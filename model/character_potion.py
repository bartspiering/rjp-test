from . import db


class CharacterPotion(db.Model):
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.id"), primary_key=True
    )
    character = db.relationship("Character", back_populates="potions")

    potion_id = db.Column(db.Integer, db.ForeignKey("potion.id"), primary_key=True)
    potion = db.relationship("Potion", back_populates="characters")
