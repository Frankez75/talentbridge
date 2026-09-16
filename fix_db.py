from run import app
from pkg.models import db

with app.app_context():
    db.session.execute(db.text("DROP TABLE IF EXISTS alembic_version"))
    db.session.commit()
    print("Dropped alembic_version table successfully.")
