from flask_restx import Resource
from flask_jwt_extended import jwt_required

from model import Spell, CharacterSpell

from .. import api
from ..pagination import pagination
from ..pagination.arguments import pagination_request_parser
from ..pagination.schema_hook import pagination_schema_hook
from .spell import spell_fields
from .spell_list import spell_list_fields


@api.route("/characters/<int:character_id>/spells")
class CharacterSpellListResource(Resource):
    @api.doc(security="Bearer", description="Retrieve all spells of a character")
    @api.expect(pagination_request_parser)
    @api.marshal_with(spell_list_fields)
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, character_id: int):
        query = Spell.query.join(
            CharacterSpell, CharacterSpell.spell_id == Spell.id
        ).filter(CharacterSpell.character_id == character_id)

        return pagination.paginate(
            query,
            spell_fields,
            pagination_schema_hook=pagination_schema_hook,
        )
