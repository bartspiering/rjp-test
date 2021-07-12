from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from flask_restx.reqparse import RequestParser

from .. import api
from model import db, Character


character_field_dict = {
    "name": fields.String,
    "gender": fields.String,
    "job": fields.String,
    "house": fields.String,
    "wand": fields.String,
    "patronus": fields.String,
    "species": fields.String,
    "blood_status": fields.String,
    "hair_colour": fields.String,
    "eye_colour": fields.String,
    "loyalty": fields.String,
    "skills": fields.String,
    "birth": fields.String,
    "death": fields.String,
}

character_payload_fields = api.model("CharacterPayload", character_field_dict)

character_fields = api.model(
    "Character",
    {
        **{
            "id": fields.Integer,
        },
        **character_field_dict,
    },
)

character_parser = RequestParser()
character_parser.add_argument("name", type=str, required=True)
character_parser.add_argument("gender", type=str)
character_parser.add_argument("job", type=str)
character_parser.add_argument("house", type=str)
character_parser.add_argument("wand", type=str)
character_parser.add_argument("patronus", type=str)
character_parser.add_argument("species", type=str)
character_parser.add_argument("blood_status", type=str)
character_parser.add_argument("hair_colour", type=str)
character_parser.add_argument("eye_colour", type=str)
character_parser.add_argument("loyalty", type=str)
character_parser.add_argument("skills", type=str)
character_parser.add_argument("birth", type=str)
character_parser.add_argument("death", type=str)


@api.route("/characters/<int:character_id>")
class CharacterResource(Resource):
    @api.doc(security="Bearer", description="Get a character by ID")
    @api.marshal_with(character_fields)
    @api.response(401, "Unauthorized")
    @api.response(404, "Character not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, character_id: int):
        return Character.query.get_or_404(
            character_id, description="Character not found"
        )

    @api.doc(security="Bearer", description="Change a character")
    @api.expect(character_payload_fields)
    @api.marshal_with(character_fields, code=200, description="Character updated")
    @api.response(400, "Invalid input")
    @api.response(401, "Unauthorized")
    @api.response(404, "Character not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def put(self, character_id: int):
        character = Character.query.get_or_404(
            character_id, description="Character not found"
        )

        args = character_parser.parse_args()

        for key, value in args.items():
            setattr(character, key, value)

        db.session.commit()

        return character

    @api.doc(security="Bearer", description="Delete a character")
    @api.response(204, "Character deleted")
    @api.response(401, "Unauthorized")
    @api.response(404, "Character not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def delete(self, character_id: int):
        character = Character.query.get_or_404(
            character_id, description="Character not found"
        )

        db.session.delete(character)
        db.session.commit()

        return None, 204
