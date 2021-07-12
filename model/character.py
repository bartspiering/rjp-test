from . import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Text, nullable=True)
    job = db.Column(db.Text, nullable=True)
    house = db.Column(db.Text, nullable=True)
    wand = db.Column(db.Text, nullable=True)
    patronus = db.Column(db.Text, nullable=True)
    species = db.Column(db.Text, nullable=True)
    blood_status = db.Column(db.Text, nullable=True)
    hair_colour = db.Column(db.Text, nullable=True)
    eye_colour = db.Column(db.Text, nullable=True)
    loyalty = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    birth = db.Column(db.Text, nullable=True)
    death = db.Column(db.Text, nullable=True)

    potions = db.relationship("CharacterPotion", back_populates="character")

    spells = db.relationship("CharacterSpell", back_populates="character")
