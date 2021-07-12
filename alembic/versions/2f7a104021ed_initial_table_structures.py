"""initial table structures

Revision ID: 2f7a104021ed
Revises: 
Create Date: 2021-07-09 18:19:57.931328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import EmailType, PasswordType


# revision identifiers, used by Alembic.
revision = "2f7a104021ed"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", EmailType, nullable=False, unique=True),
        sa.Column("password", PasswordType(max_length=1137), nullable=False),
    )

    op.create_table(
        "character",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("gender", sa.Text, nullable=True),
        sa.Column("job", sa.Text, nullable=True),
        sa.Column("house", sa.Text, nullable=True),
        sa.Column("wand", sa.Text, nullable=True),
        sa.Column("patronus", sa.Text, nullable=True),
        sa.Column("species", sa.Text, nullable=True),
        sa.Column("blood_status", sa.Text, nullable=True),
        sa.Column("hair_colour", sa.Text, nullable=True),
        sa.Column("eye_colour", sa.Text, nullable=True),
        sa.Column("loyalty", sa.Text, nullable=True),
        sa.Column("skills", sa.Text, nullable=True),
        sa.Column("birth", sa.Text, nullable=True),
        sa.Column("death", sa.Text, nullable=True),
    )

    op.create_table(
        "potion",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("known_ingredients", sa.Text, nullable=True),
        sa.Column("effect", sa.Text, nullable=True),
        sa.Column("characteristics", sa.Text, nullable=True),
        sa.Column("difficulty_level", sa.Text, nullable=True),
    )

    op.create_table(
        "character_potion",
        sa.Column("character_id", sa.Integer, sa.ForeignKey("character.id")),
        sa.Column("potion_id", sa.Integer, sa.ForeignKey("potion.id")),
        sa.PrimaryKeyConstraint("character_id", "potion_id"),
    )

    op.create_table(
        "spell",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("incantation", sa.Text, nullable=True),
        sa.Column("type", sa.Text, nullable=True),
        sa.Column("effect", sa.Text, nullable=True),
        sa.Column("light", sa.Text, nullable=True),
    )

    op.create_table(
        "character_spell",
        sa.Column("character_id", sa.Integer, sa.ForeignKey("character.id")),
        sa.Column("spell_id", sa.Integer, sa.ForeignKey("spell.id")),
        sa.PrimaryKeyConstraint("character_id", "spell_id"),
    )


def downgrade():
    op.drop_table("user")
    op.drop_table("character")
    op.drop_table("potion")
    op.drop_table("character_potion")
    op.drop_table("spell")
    op.drop_table("character_spell")
