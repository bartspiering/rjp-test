from flask import abort
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from .. import api
from model import db, CharacterSpell, Character, Spell
from .spell import spell_fields


@api.route("/characters/<int:character_id>/spells/<int:spell_id>")
class CharacterSpellResource(Resource):
    @api.doc(security="Bearer")
    @api.marshal_with(spell_fields)
    @api.response(401, "Unauthorized")
    @api.response(404, "Link between character and spell not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, character_id: int, spell_id: int):
        return (
            Spell.query.join(CharacterSpell, CharacterSpell.spell_id == Spell.id)
            .filter(CharacterSpell.character_id == character_id)
            .filter(CharacterSpell.spell_id == spell_id)
            .first_or_404(description="Link between character and spell not found")
        )

    @api.doc(security="Bearer")
    @api.response(200, "Character linked to spell")
    @api.response(401, "Unauthorized")
    @api.response(404, "Character or spell not found")
    @api.response(409, "Link between character and spell already exists")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def put(self, character_id: int, spell_id: int):
        character = Character.query.get_or_404(
            character_id, description="Character or spell not found"
        )

        spell = Spell.query.get_or_404(
            spell_id, description="Character or spell not found"
        )

        character_spell = CharacterSpell()
        character_spell.character = character
        character_spell.spell = spell

        db.session.add(character_spell)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, "Link between character and spell already exists")

        return {"message": "Character linked to spell"}, 200

    @api.doc(security="Bearer")
    @api.response(204, "Link between character and spell deleted")
    @api.response(401, "Unauthorized")
    @api.response(404, "Link between character and spell not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def delete(self, character_id: int, spell_id: int):
        character_spell = (
            CharacterSpell.query.filter(CharacterSpell.character_id == character_id)
            .filter(CharacterSpell.spell_id == spell_id)
            .first_or_404(description="Link between character and spell not found")
        )

        db.session.delete(character_spell)
        db.session.commit()

        return None, 204
