from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from flask_restx.reqparse import RequestParser

from .. import api
from model import db, Potion


potion_field_dict = {
    "name": fields.String,
    "known_ingredients": fields.String,
    "effect": fields.String,
    "potionistics": fields.String,
    "difficulty_level": fields.String,
}

potion_payload_fields = api.model("PotionPayload", potion_field_dict)

potion_fields = api.model(
    "Potion",
    {
        **{
            "id": fields.Integer,
        },
        **potion_field_dict,
    },
)

potion_parser = RequestParser()
potion_parser.add_argument("name", type=str, required=True)
potion_parser.add_argument("known_ingredients", type=str)
potion_parser.add_argument("effect", type=str)
potion_parser.add_argument("potionistics", type=str)
potion_parser.add_argument("difficulty_level", type=str)


@api.route("/potions/<int:potion_id>")
class PotionResource(Resource):
    @api.doc(security="Bearer", description="Get a potion by ID")
    @api.marshal_with(potion_fields)
    @api.response(401, "Unauthorized")
    @api.response(404, "Potion not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, potion_id: int):
        return Potion.query.get_or_404(potion_id, description="Potion not found")

    @api.doc(security="Bearer", description="Change a potion")
    @api.expect(potion_payload_fields)
    @api.marshal_with(potion_fields, code=200, description="Potion updated")
    @api.response(400, "Invalid input")
    @api.response(401, "Unauthorized")
    @api.response(404, "Potion not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def put(self, potion_id: int):
        potion = Potion.query.get_or_404(potion_id, description="Potion not found")

        args = potion_parser.parse_args()

        for key, value in args.items():
            setattr(potion, key, value)

        db.session.commit()

        return potion

    @api.doc(security="Bearer", description="Delete a potion")
    @api.response(204, "Potion deleted")
    @api.response(401, "Unauthorized")
    @api.response(404, "Potion not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def delete(self, potion_id: int):
        potion = Potion.query.get_or_404(potion_id, description="Potion not found")

        db.session.delete(potion)
        db.session.commit()

        return None, 204
