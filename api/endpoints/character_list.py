from copy import deepcopy
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required

from model import db, Character

from .. import api
from ..pagination import pagination
from ..pagination.arguments import pagination_request_parser
from ..pagination.fields import pagination_response_fields
from ..pagination.schema_hook import pagination_schema_hook
from .character import character_fields, character_payload_fields, character_parser


character_list_fields = api.model(
    "CharacterList",
    {
        "data": fields.List(fields.Nested(character_fields)),
        "pagination": fields.List(fields.Nested(pagination_response_fields)),
    },
)

character_list_parser = deepcopy(pagination_request_parser)
character_list_parser.add_argument(
    "sort_by", type=str, choices=tuple(character_payload_fields.keys()), location="args"
)
character_list_parser.add_argument(
    "sort_direction", type=str, choices=("asc", "desc"), location="args"
)
character_list_parser.add_argument(
    "filter_by",
    type=str,
    choices=tuple(character_payload_fields.keys()),
    location="args",
)
character_list_parser.add_argument("filter_value", type=str, location="args")


@api.route("/characters")
class CharacterListResource(Resource):
    @api.doc(security="Bearer", description="Retrieve all characters")
    @api.expect(character_list_parser)
    @api.marshal_with(character_list_fields)
    @api.response(400, "Invalid input")
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self):
        args = character_list_parser.parse_args()

        query = Character.query

        try:
            if args["sort_by"] is not None:
                query = query.order_by(
                    getattr(
                        getattr(Character, args["sort_by"]),
                        args["sort_direction"] or "asc",
                    )()
                )
        except AttributeError:
            pass

        try:
            if args["filter_by"] is not None and args["filter_value"] is not None:
                query = query.filter(
                    getattr(Character, args["filter_by"]).ilike(
                        f'%{args["filter_value"]}%'
                    )
                )
        except AttributeError:
            pass

        return pagination.paginate(
            query, character_fields, pagination_schema_hook=pagination_schema_hook
        )

    @api.doc(security="Bearer", description="Add a character")
    @api.expect(character_payload_fields)
    @api.marshal_with(character_fields, code=201, description="Character created")
    @api.response(400, "Invalid input")
    @api.response(401, "Unauthorized")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def post(self):
        args = character_parser.parse_args()

        character = Character(**args)

        db.session.add(character)
        db.session.commit()

        return character, 201
