from flask_restx import reqparse


pagination_request_parser = reqparse.RequestParser()
pagination_request_parser.add_argument("page", type=int, location="args")
pagination_request_parser.add_argument("size", type=int, location="args")
