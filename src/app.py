from flask import Flask
from flask_restful import Api
from api.models import db, OwnerModel, PetModel, VeterinarianModel, AppointmentModel, TreatmentModel, MedicationModel, VaccineModel
from api.controllers import ClientRegistration, ClientUpdate, ClientDeletion, ClientList, ClientDetail, PetRegistration, PetUpdate, PetDeletion, PetDetail, PetsByOwner,VeterinarianRegistration, VeterinarianUpdate, VeterinarianDeletion, VeterinarianDetail, VeterinarianList, AppointmentRegistration, AppointmentUpdate, AppointmentDeletion, AppointmentDetail, AppointmentList, TreatmentRegistration, TreatmentUpdate, TreatmentDeletion, TreatmentDetail, TreatmentsByPet

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veterinary.db'  # Cambia esto si usas otro tipo de base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Inicializar Flask-RESTful
api = Api(app)

# Rutas de clientes
api.add_resource(ClientRegistration, '/api/clients/register')
api.add_resource(ClientUpdate, '/api/clients/<int:client_id>')
api.add_resource(ClientDeletion, '/api/clients/<int:client_id>')
api.add_resource(ClientList, '/api/clients')
api.add_resource(ClientDetail, '/api/clients/<int:client_id>') 

# Rutas de mascotas
api.add_resource(PetRegistration, '/api/pets/register')
api.add_resource(PetUpdate, '/api/pets/<int:pet_id>')
api.add_resource(PetDeletion, '/api/pets/<int:pet_id>')
api.add_resource(PetDetail, '/api/pets/<int:pet_id>')
api.add_resource(PetsByOwner, '/api/owners/<int:owner_id>/pets')

# Rutas de veterinarios
api.add_resource(VeterinarianRegistration, '/api/veterinarians/register')
api.add_resource(VeterinarianUpdate, '/api/veterinarians/<int:veterinarian_id>')
api.add_resource(VeterinarianDeletion, '/api/veterinarians/<int:veterinarian_id>')
api.add_resource(VeterinarianDetail, '/api/veterinarians/<int:veterinarian_id>')
api.add_resource(VeterinarianList, '/api/veterinarians')

# Rutas para citas
api.add_resource(AppointmentRegistration, '/api/appointments/register')
api.add_resource(AppointmentUpdate, '/api/appointments/<int:appointment_id>')
api.add_resource(AppointmentDeletion, '/api/appointments/<int:appointment_id>')
api.add_resource(AppointmentDetail, '/api/appointments/<int:appointment_id>')
api.add_resource(AppointmentList, '/api/appointments')

# Rutas de tratamientos
api.add_resource(TreatmentRegistration, '/api/treatments/register')
api.add_resource(TreatmentUpdate, '/api/treatments/<int:treatment_id>')
api.add_resource(TreatmentDeletion, '/api/treatments/<int:treatment_id>')
api.add_resource(TreatmentDetail, '/api/treatments/<int:treatment_id>')
api.add_resource(TreatmentsByPet, '/api/pets/<int:pet_id>/treatments')

# Crear tablas al iniciar la aplicación
#with app.app_context():
 #   db.create_all()
  #  print("Base de datos creada exitosamente.")






