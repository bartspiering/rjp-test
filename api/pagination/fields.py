from flask_restx import fields

from .. import api


pagination_response_fields = api.model(
    "PaginationResponse",
    {
        "current_page": fields.String,
        "has_next": fields.Boolean,
        "has_prev": fields.Boolean,
        "next": fields.String,
        "pages": fields.Integer,
        "size": fields.Integer,
        "total": fields.Integer,
    },
)
