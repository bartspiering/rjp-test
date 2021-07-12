import os
import pandas as pd
import alembic.config

from core import create_app
from model import Character, Potion, Spell, db


def run_setup(config_name="DevelopmentConfig"):
    alembic.config.main(
        argv=[
            "--raiseerr",
            f"-xconfig={config_name}",
            "upgrade",
            "head",
        ]
    )

    rename_columns = lambda x: x.lower().replace(" ", "_")
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x

    characters_data = (
        pd.read_csv("csv_data/Characters.csv", sep=";")
        .rename(columns=rename_columns)
        .applymap(trim_strings)
    )

    potions_data = (
        pd.read_csv("csv_data/Potions.csv", sep=";")
        .rename(columns=rename_columns)
        .applymap(trim_strings)
    )

    spells_data = (
        pd.read_csv("csv_data/Spells.csv", sep=";")
        .rename(columns=rename_columns)
        .applymap(trim_strings)
    )

    db.session.bulk_save_objects(
        [Character(**row) for row in characters_data.to_dict("records")]
        + [Potion(**row) for row in potions_data.to_dict("records")]
        + [Spell(**row) for row in spells_data.to_dict("records")]
    )

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()

    database_file = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite://", "")

    if os.path.exists(database_file):
        os.remove(database_file)

    run_setup()
