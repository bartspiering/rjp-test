from . import db


class Potion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    known_ingredients = db.Column(db.Text, nullable=True)
    effect = db.Column(db.Text, nullable=True)
    characteristics = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.Text, nullable=True)

    characters = db.relationship("CharacterPotion", back_populates="potion")
