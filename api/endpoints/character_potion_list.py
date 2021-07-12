from flask_restx import Resource
from flask_jwt_extended import jwt_required

from model import Potion, CharacterPotion

from .. import api
from ..pagination import pagination
from ..pagination.arguments import pagination_request_parser
from ..pagination.schema_hook import pagination_schema_hook
from .potion import potion_fields
from .potion_list import potion_list_fields


@api.route("/characters/<int:character_id>/potions")
class CharacterPotionListResource(Resource):
    @api.doc(security="Bearer", description="Retrieve all potions of a character")
    @api.expect(pagination_request_parser)
    @api.marshal_with(potion_list_fields)
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, character_id: int):
        query = Potion.query.join(
            CharacterPotion, CharacterPotion.potion_id == Potion.id
        ).filter(CharacterPotion.character_id == character_id)

        return pagination.paginate(
            query,
            potion_fields,
            pagination_schema_hook=pagination_schema_hook,
        )
