from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from flask_restx.reqparse import RequestParser

from .. import api
from model import db, Spell


spell_field_dict = {
    "name": fields.String,
    "incantation": fields.String,
    "type": fields.String,
    "effect": fields.String,
    "light": fields.String,
}

spell_payload_fields = api.model("SpellPayload", spell_field_dict)

spell_fields = api.model(
    "Spell",
    {
        **{
            "id": fields.Integer,
        },
        **spell_field_dict,
    },
)

spell_parser = RequestParser()
spell_parser.add_argument("name", type=str, required=True)
spell_parser.add_argument("incantation", type=str)
spell_parser.add_argument("type", type=str)
spell_parser.add_argument("effect", type=str)
spell_parser.add_argument("light", type=str)


@api.route("/spells/<int:spell_id>")
class SpellResource(Resource):
    @api.doc(security="Bearer", description="Get a spell by ID")
    @api.marshal_with(spell_fields)
    @api.response(401, "Unauthorized")
    @api.response(404, "Spell not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def get(self, spell_id: int):
        return Spell.query.get_or_404(spell_id, description="Spell not found")

    @api.doc(security="Bearer", description="Change a spell")
    @api.expect(spell_payload_fields)
    @api.marshal_with(spell_fields, code=200, description="Spell updated")
    @api.response(400, "Invalid input")
    @api.response(401, "Unauthorized")
    @api.response(404, "Spell not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def put(self, spell_id: int):
        spell = Spell.query.get_or_404(spell_id, description="Spell not found")

        args = spell_parser.parse_args()

        for key, value in args.items():
            setattr(spell, key, value)

        db.session.commit()

        return spell

    @api.doc(security="Bearer", description="Delete a character")
    @api.response(204, "Spell deleted")
    @api.response(401, "Unauthorized")
    @api.response(404, "Spell not found")
    @api.response(422, "Unprocessable entity")
    @jwt_required()
    def delete(self, spell_id: int):
        spell = Spell.query.get_or_404(spell_id, description="Spell not found")

        db.session.delete(spell)
        db.session.commit()

        return None, 204
