from app import app
from api.models import db

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()
    print("Base de datos creada exitosamente.")
