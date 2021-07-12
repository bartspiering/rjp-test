from . import db


class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    incantation = db.Column(db.Text, nullable=True)
    type = db.Column(db.Text, nullable=True)
    effect = db.Column(db.Text, nullable=True)
    light = db.Column(db.Text, nullable=True)

    characters = db.relationship("CharacterSpell", back_populates="spell")
