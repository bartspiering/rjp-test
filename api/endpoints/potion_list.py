from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required

from model import db, Potion

from .. import api
from ..pagination import pagination
from ..pagination.arguments import pagination_request_parser
from ..pagination.fields import pagination_response_fields
from ..pagination.schema_hook import pagination_schema_hook
from .potion import potion_fields, potion_payload_fields, potion_parser


potion_list_fields = api.model(
    "PotionList",
    {
        "data": fields.List(fields.Nested(potion_fields)),
        "pagination": fields.List(fields.Nested(pagination_response_fields)),
    },
)


@api.route("/potions")
class PotionListResource(Resource):
    @api.doc(security="Bearer")
    @api.expect(pagination_request_parser)
    @api.marshal_with(potion_list_fields)
    @jwt_required()
    def get(self):
        return pagination.paginate(
            Potion, potion_fields, pagination_schema_hook=pagination_schema_hook
        )

    @api.doc(security="Bearer")
    @api.expect(potion_payload_fields)
    @api.marshal_with(potion_fields, code=201, description="Potion created")
    @api.response(400, "Invalid input")
    @jwt_required()
    def post(self):
        args = potion_parser.parse_args()

        potion = Potion(**args)

        db.session.add(potion)
        db.session.commit()

        return potion, 201
