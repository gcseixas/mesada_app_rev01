from app import app, db
from app import models  # IMPORTANTE: registra as tabelas

with app.app_context():
    db.create_all()

print("Banco e tabelas criados com sucesso")
