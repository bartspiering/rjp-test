from flask import abort
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from .. import api
from model import db, CharacterPotion, Character, Potion
from .potion import potion_fields


@api.route("/characters/<int:character_id>/potions/<int:potion_id>")
class CharacterPotionResource(Resource):
    @api.doc(security="Bearer")
    @api.marshal_with(potion_fields)
    @api.response(401, "Unauthorized")
    @api.response(404, "Link between character and potion not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, character_id: int, potion_id: int):
        return (
            Potion.query.join(CharacterPotion, CharacterPotion.potion_id == Potion.id)
            .filter(CharacterPotion.character_id == character_id)
            .filter(CharacterPotion.potion_id == potion_id)
            .first_or_404(description="Link between character and potion not found")
        )

    @api.doc(security="Bearer")
    @api.response(200, "Character linked to potion")
    @api.response(401, "Unauthorized")
    @api.response(404, "Character or potion not found")
    @api.response(409, "Link between character and potion already exists")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def put(self, character_id: int, potion_id: int):
        character = Character.query.get_or_404(
            character_id, description="Character or potion not foun"
        )

        potion = Potion.query.get_or_404(
            potion_id, description="Character or potion not found"
        )

        character_potion = CharacterPotion()
        character_potion.character = character
        character_potion.potion = potion

        db.session.add(character_potion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, "Link between character and potion already exists")

        return {"message": "Character linked to potion"}, 200

    @api.doc(security="Bearer")
    @api.response(204, "Link between character and potion deleted")
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @api.response(404, "Link between character and potion not found")
    @jwt_required()
    def delete(self, character_id: int, potion_id: int):
        character_potion = (
            CharacterPotion.query.filter(CharacterPotion.character_id == character_id)
            .filter(CharacterPotion.potion_id == potion_id)
            .first_or_404(description="Link between character and potion not found")
        )

        db.session.delete(character_potion)
        db.session.commit()

        return None, 204
