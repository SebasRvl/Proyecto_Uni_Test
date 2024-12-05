from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo para los propietarios
class OwnerModel(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    # Relación con mascotas
    pets = db.relationship('PetModel', backref='owner', lazy=True)

# Modelo para las mascotas
class PetModel(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=False)

    # Relación con el propietario
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)

    # Relación con citas, tratamientos y vacunas
    appointments = db.relationship('AppointmentModel', backref='pet', lazy=True)
    vaccines = db.relationship('VaccineModel', backref='pet', lazy=True)

# Modelo para los veterinarios
class VeterinarianModel(db.Model):
    __tablename__ = 'veterinarians'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    specialty = db.Column(db.String(100), nullable=True)

    # Relación con citas
    appointments = db.relationship('AppointmentModel', backref='veterinarian', lazy=True)

# Modelo para las citas
class AppointmentModel(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    
    # Relación con mascota y veterinario
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    veterinarian_id = db.Column(db.Integer, db.ForeignKey('veterinarians.id'), nullable=False)

    # Relación con tratamiento
    treatment = db.relationship('TreatmentModel', backref='appointment', lazy=True, uselist=False)

# Modelo para los tratamientos
class TreatmentModel(db.Model):
    __tablename__ = 'treatments'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    
    # Relación con cita
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)

    # Relación con medicamentos
    medications = db.relationship('MedicationModel', backref='treatment', lazy=True)

# Modelo para los medicamentos
class MedicationModel(db.Model):
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dose = db.Column(db.String(100), nullable=False)

    # Relación con tratamiento
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=False)

# Modelo para las vacunas
class VaccineModel(db.Model):
    __tablename__ = 'vaccines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    application_date = db.Column(db.Date, nullable=False)

    # Relación con mascota
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
