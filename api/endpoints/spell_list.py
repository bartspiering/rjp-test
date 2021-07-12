from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required

from model import db, Spell

from .. import api
from ..pagination import pagination
from ..pagination.arguments import pagination_request_parser
from ..pagination.fields import pagination_response_fields
from ..pagination.schema_hook import pagination_schema_hook
from .spell import spell_fields, spell_payload_fields, spell_parser


spell_list_fields = api.model(
    "SpellList",
    {
        "data": fields.List(fields.Nested(spell_fields)),
        "pagination": fields.List(fields.Nested(pagination_response_fields)),
    },
)


@api.route("/spells")
class SpellListResource(Resource):
    @api.doc(security="Bearer", description="Retrieve all spells")
    @api.expect(pagination_request_parser)
    @api.marshal_with(spell_list_fields)
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self):
        return pagination.paginate(
            Spell, spell_fields, pagination_schema_hook=pagination_schema_hook
        )

    @api.doc(security="Bearer", description="Add a spell")
    @api.expect(spell_payload_fields)
    @api.marshal_with(spell_fields, code=201, description="Spell created")
    @api.response(400, "Invalid input")
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def post(self):
        args = spell_parser.parse_args()

        spell = Spell(**args)

        db.session.add(spell)
        db.session.commit()

        return spell, 201
