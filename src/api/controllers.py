from flask_restful import Resource, reqparse
from api.models import OwnerModel as ClientModel,PetModel,OwnerModel,VeterinarianModel,AppointmentModel,TreatmentModel, db
from datetime import datetime
import pytest
# Parser para manejar los datos enviados en las solicitudes
client_parser = reqparse.RequestParser()
client_parser.add_argument("name", type=str, required=True, help="El nombre del cliente es obligatorio")
client_parser.add_argument("email", type=str, required=True, help="El correo del cliente es obligatorio")
client_parser.add_argument("phone", type=str, required=True, help="El teléfono del cliente es obligatorio")
client_parser.add_argument("address", type=str, required=True, help="La dirección del cliente es obligatoria")

# Parser para manejar los datos enviados en las solicitudes
pet_parser = reqparse.RequestParser()
pet_parser.add_argument("name", type=str, required=True, help="El nombre de la mascota es obligatorio")
pet_parser.add_argument("species", type=str, required=True, help="La especie de la mascota es obligatoria")
pet_parser.add_argument("breed", type=str, required=False, help="La raza de la mascota es opcional")
pet_parser.add_argument("age", type=int, required=True, help="La edad de la mascota es obligatoria")
pet_parser.add_argument("owner_id", type=int, required=True, help="El ID del dueño es obligatorio")

# Parser para veterinarios
veterinarian_parser = reqparse.RequestParser()
veterinarian_parser.add_argument("name", type=str, required=True, help="El nombre del veterinario es obligatorio")
veterinarian_parser.add_argument("email", type=str, required=True, help="El correo del veterinario es obligatorio")
veterinarian_parser.add_argument("phone", type=str, required=False, help="El teléfono del veterinario es opcional")
veterinarian_parser.add_argument("specialty", type=str, required=False, help="La especialidad del veterinario es opcional")

# Parser para manejar los datos enviados en las solicitudes
appointment_parser = reqparse.RequestParser()
appointment_parser.add_argument("date", type=str, required=True, help="La fecha de la cita es obligatoria (YYYY-MM-DD HH:MM).")
appointment_parser.add_argument("reason", type=str, required=True, help="El motivo de la cita es obligatorio.")
appointment_parser.add_argument("pet_id", type=int, required=True, help="El ID de la mascota es obligatorio.")
appointment_parser.add_argument("veterinarian_id", type=int, required=True, help="El ID del veterinario es obligatorio.")

# Parser para tratamientos
treatment_parser = reqparse.RequestParser()
treatment_parser.add_argument("description", type=str, required=True, help="La descripción es obligatoria.")
treatment_parser.add_argument("cost", type=float, required=True, help="El costo es obligatorio.")
treatment_parser.add_argument("pet_id", type=int, required=True, help="El ID de la mascota es obligatorio.")




### CONTROLADORES ###

class ClientRegistration(Resource):
    def post(self):
        args = client_parser.parse_args()

        # Validar si el cliente ya existe usando el correo electrónico
        existing_client = ClientModel.query.filter_by(email=args["email"]).first()
        if existing_client:
            return {"message": "El correo ya está registrado.", "status": "error"}, 400

        # Crear una instancia de un nuevo cliente
        new_client = ClientModel(
            name=args.get("name"),
            email=args.get("email"),
            phone=args.get("phone"),
            address=args.get("address")
        )

        try:
            # Guardar el nuevo cliente en la base de datos
            db.session.add(new_client)
            db.session.commit()
            return {
                "message": "Cliente registrado exitosamente.",
                "status": "success",
                "data": {
                    "id": new_client.id,
                    "name": new_client.name,
                    "email": new_client.email,
                    "phone": new_client.phone,
                    "address": new_client.address
                }
            }, 201
        except Exception as e:
            # Manejar errores durante la operación
            db.session.rollback()
            return {
                "message": "Error al registrar el cliente.",
                "status": "error",
                "error": str(e)
            }, 500



class ClientUpdate(Resource):
    def put(self, client_id):
        args = client_parser.parse_args()

        # Buscar el cliente por ID
        client = ClientModel.query.get(client_id)
        if not client:
            return {"message": "Cliente no encontrado."}, 404

        # Actualizar datos del cliente
        client.name = args["name"]
        client.email = args["email"]
        client.phone = args["phone"]
        client.address = args["address"]

        try:
            db.session.commit()
            return {"message": "Cliente actualizado correctamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el cliente.", "error": str(e)}, 500


class ClientDeletion(Resource):
    def delete(self, client_id):
        client = ClientModel.query.get(client_id)
        if not client:
            return {"message": "Cliente no encontrado."}, 404

        try:
            db.session.delete(client)
            db.session.commit()
            return {"message": "Cliente eliminado exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el cliente.", "error": str(e)}, 500


class ClientDetail(Resource):
    def get(self, client_id):
        # Buscar el cliente por ID
        client = ClientModel.query.get(client_id)
        if not client:
            return {"message": "Cliente no encontrado."}, 404

        # Retornar información del cliente
        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
        }, 200


class ClientList(Resource):
    def get(self):
        # Obtener todos los clientes
        clients = ClientModel.query.all()
        clients_list = [
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "address": client.address,
            }
            for client in clients
        ]
        return {"clients": clients_list}, 200
    

class PetRegistration(Resource):
    def post(self):
        args = pet_parser.parse_args()

        # Verificar si el cliente (dueño) existe
        owner = OwnerModel.query.get(args["owner_id"])
        if not owner:
            return {"message": "El dueño especificado no existe."}, 400

        # Crear una nueva mascota
        new_pet = PetModel(
            name=args["name"],
            species=args["species"],
            breed=args.get("breed"),
            age=args["age"],
            owner_id=args["owner_id"]
        )

        try:
            db.session.add(new_pet)
            db.session.commit()
            return {"message": "Mascota registrada exitosamente."}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar la mascota.", "error": str(e)}, 500


class PetUpdate(Resource):
    def put(self, pet_id):
        args = pet_parser.parse_args()

        # Buscar la mascota por ID
        pet = PetModel.query.get(pet_id)
        if not pet:
            return {"message": "Mascota no encontrada."}, 404

        # Actualizar datos de la mascota
        pet.name = args["name"]
        pet.species = args["species"]
        pet.breed = args.get("breed")
        pet.age = args["age"]
        pet.owner_id = args["owner_id"]

        try:
            db.session.commit()
            return {"message": "Mascota actualizada correctamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar la mascota.", "error": str(e)}, 500


class PetDeletion(Resource):
    def delete(self, pet_id):
        # Buscar la mascota por ID
        pet = PetModel.query.get(pet_id)
        if not pet:
            return {"message": "Mascota no encontrada."}, 404

        try:
            db.session.delete(pet)
            db.session.commit()
            return {"message": "Mascota eliminada exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar la mascota.", "error": str(e)}, 500


class PetDetail(Resource):
    def get(self, pet_id):
        # Buscar la mascota por ID
        pet = PetModel.query.get(pet_id)
        if not pet:
            return {"message": "Mascota no encontrada."}, 404

        # Retornar información de la mascota
        return {
            "id": pet.id,
            "name": pet.name,
            "species": pet.species,
            "breed": pet.breed,
            "age": pet.age,
            "owner_id": pet.owner_id
        }, 200


class PetsByOwner(Resource):
    def get(self, owner_id):
        # Verificar si el dueño existe
        owner = OwnerModel.query.get(owner_id)
        if not owner:
            return {"message": "Dueño no encontrado."}, 404

        # Obtener todas las mascotas del dueño
        pets = PetModel.query.filter_by(owner_id=owner_id).all()
        pets_list = [
            {
                "id": pet.id,
                "name": pet.name,
                "species": pet.species,
                "breed": pet.breed,
                "age": pet.age,
            }
            for pet in pets
        ]

        return {"owner": owner.name, "pets": pets_list}, 200

class VeterinarianRegistration(Resource):
    def post(self):
        args = veterinarian_parser.parse_args()

        # Verificar si el veterinario ya existe por correo
        if VeterinarianModel.query.filter_by(email=args["email"]).first():
            return {"message": "El correo ya está registrado."}, 400

        # Crear un nuevo veterinario
        new_veterinarian = VeterinarianModel(
            name=args["name"],
            email=args["email"],
            phone=args.get("phone"),
            specialty=args.get("specialty")
        )

        try:
            db.session.add(new_veterinarian)
            db.session.commit()
            return {"message": "Veterinario registrado exitosamente."}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar el veterinario.", "error": str(e)}, 500


class VeterinarianUpdate(Resource):
    def put(self, veterinarian_id):
        args = veterinarian_parser.parse_args()

        # Buscar el veterinario por ID
        veterinarian = VeterinarianModel.query.get(veterinarian_id)
        if not veterinarian:
            return {"message": "Veterinario no encontrado."}, 404

        # Actualizar datos del veterinario solo si están presentes en los argumentos
        if args.get("name"):
            veterinarian.name = args["name"]
        if args.get("email"):
            veterinarian.email = args["email"]
        if args.get("phone"):
            veterinarian.phone = args.get("phone")
        if args.get("specialty"):
            veterinarian.specialty = args.get("specialty")

        try:
            db.session.commit()
            return {"message": "Veterinario actualizado correctamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el veterinario.", "error": str(e)}, 500



class VeterinarianDeletion(Resource):
    def delete(self, veterinarian_id):
        # Buscar el veterinario por ID
        veterinarian = VeterinarianModel.query.get(veterinarian_id)
        if not veterinarian:
            return {"message": "Veterinario no encontrado."}, 404

        try:
            db.session.delete(veterinarian)
            db.session.commit()
            return {"message": "Veterinario eliminado exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el veterinario.", "error": str(e)}, 500


class VeterinarianDetail(Resource):
    def get(self, veterinarian_id):
        # Buscar el veterinario por ID
        veterinarian = VeterinarianModel.query.get(veterinarian_id)
        if not veterinarian:
            return {"message": "Veterinario no encontrado."}, 404

        return {
            "id": veterinarian.id,
            "name": veterinarian.name,
            "email": veterinarian.email,
            "phone": veterinarian.phone,
            "specialty": veterinarian.specialty,
        }, 200


class VeterinarianList(Resource):
    def get(self):
        # Obtener todos los veterinarios
        veterinarians = VeterinarianModel.query.all()
        veterinarian_list = [
            {
                "id": veterinarian.id,
                "name": veterinarian.name,
                "email": veterinarian.email,
                "phone": veterinarian.phone,
                "specialty": veterinarian.specialty,
            }
            for veterinarian in veterinarians
        ]
        return {"veterinarians": veterinarian_list}, 200


# Registrar una nueva cita
class AppointmentRegistration(Resource):
    def post(self):
        args = appointment_parser.parse_args()

        # Verificar si la mascota existe
        pet = PetModel.query.get(args["pet_id"])
        if not pet:
            return {"message": "La mascota especificada no existe."}, 404

        # Verificar si el veterinario existe
        veterinarian = VeterinarianModel.query.get(args["veterinarian_id"])
        if not veterinarian:
            return {"message": "El veterinario especificado no existe."}, 404

        # Crear una nueva cita
        try:
            new_appointment = AppointmentModel(
                date=datetime.strptime(args["date"], "%Y-%m-%d %H:%M"),
                reason=args["reason"],
                pet_id=args["pet_id"],
                veterinarian_id=args["veterinarian_id"]
            )
            db.session.add(new_appointment)
            db.session.commit()
            return {"message": "Cita registrada exitosamente."}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar la cita.", "error": str(e)}, 500


# Actualizar una cita existente
class AppointmentUpdate(Resource):
    def put(self, appointment_id):
        args = appointment_parser.parse_args()

        # Verificar si la cita existe
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return {"message": "Cita no encontrada."}, 404

        # Actualizar datos de la cita
        try:
            appointment.date = datetime.strptime(args["date"], "%Y-%m-%d %H:%M")
            appointment.reason = args["reason"]
            appointment.pet_id = args["pet_id"]
            appointment.veterinarian_id = args["veterinarian_id"]

            db.session.commit()
            return {"message": "Cita actualizada correctamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar la cita.", "error": str(e)}, 500


# Eliminar una cita existente
class AppointmentDeletion(Resource):
    def delete(self, appointment_id):
        # Verificar si la cita existe
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return {"message": "Cita no encontrada."}, 404

        # Eliminar la cita
        try:
            db.session.delete(appointment)
            db.session.commit()
            return {"message": "Cita eliminada exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar la cita.", "error": str(e)}, 500


# Obtener detalles de una cita específica
class AppointmentDetail(Resource):
    def get(self, appointment_id):
        # Verificar si la cita existe
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return {"message": "Cita no encontrada."}, 404

        # Devolver detalles de la cita
        return {
            "id": appointment.id,
            "date": appointment.date.strftime("%Y-%m-%d %H:%M"),
            "reason": appointment.reason,
            "pet_id": appointment.pet_id,
            "veterinarian_id": appointment.veterinarian_id
        }, 200


# Obtener lista de citas (por veterinario o mascota)
class AppointmentList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("veterinarian_id", type=int, required=False, help="ID del veterinario opcional.")
        parser.add_argument("pet_id", type=int, required=False, help="ID de la mascota opcional.")
        args = parser.parse_args()

        # Validar los argumentos proporcionados
        if not args["veterinarian_id"] and not args["pet_id"]:
            # Si no se proporcionan argumentos, devolver todas las citas
            appointments = AppointmentModel.query.all()
        elif args["veterinarian_id"]:
            # Filtrar por veterinario
            appointments = AppointmentModel.query.filter_by(veterinarian_id=args["veterinarian_id"]).all()
        elif args["pet_id"]:
            # Filtrar por mascota
            appointments = AppointmentModel.query.filter_by(pet_id=args["pet_id"]).all()
        else:
            # Caso de error inesperado
            return {"message": "Argumentos inválidos."}, 400

        # Construir la lista de citas
        appointments_list = [
            {
                "id": appointment.id,
                "date": appointment.date.strftime("%Y-%m-%d %H:%M"),
                "reason": appointment.reason,
                "pet_id": appointment.pet_id,
                "veterinarian_id": appointment.veterinarian_id
            }
            for appointment in appointments
        ]

        return {"appointments": appointments_list}, 200

    
class TreatmentRegistration(Resource):
    def post(self):
        args = treatment_parser.parse_args()

        # Validar que la cita exista
        appointment = AppointmentModel.query.get(args["appointment_id"])
        if not appointment:
            return {"message": "La cita especificada no existe."}, 404

        # Crear un nuevo tratamiento
        new_treatment = TreatmentModel(
            description=args["description"],
            cost=args["cost"],
            appointment_id=args["appointment_id"]
        )

        try:
            db.session.add(new_treatment)
            db.session.commit()
            return {
                "message": "Tratamiento registrado exitosamente.",
                "treatment": {
                    "id": new_treatment.id,
                    "description": new_treatment.description,
                    "cost": new_treatment.cost,
                    "appointment_id": new_treatment.appointment_id
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar el tratamiento.", "error": str(e)}, 500


class TreatmentUpdate(Resource):
    def put(self, treatment_id):
        args = treatment_parser.parse_args()

        # Buscar el tratamiento por ID
        treatment = TreatmentModel.query.get(treatment_id)
        if not treatment:
            return {"message": "Tratamiento no encontrado."}, 404

        # Actualizar los detalles del tratamiento
        treatment.description = args["description"]
        treatment.cost = args["cost"]
        treatment.pet_id = args["pet_id"]

        try:
            db.session.commit()
            return {"message": "Tratamiento actualizado correctamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el tratamiento.", "error": str(e)}, 500

class TreatmentDeletion(Resource):
    def delete(self, treatment_id):
        """
        Eliminar un tratamiento específico.
        """
        try:
            # Buscar el tratamiento por ID
            treatment = TreatmentModel.query.get(treatment_id)

            if not treatment:
                return {"message": "Tratamiento no encontrado."}, 404

            # Eliminar el tratamiento
            db.session.delete(treatment)
            db.session.commit()

            return {"message": "Tratamiento eliminado exitosamente.", "treatment_id": treatment_id}, 200

        except Exception as e:
            # Manejo de errores inesperados
            db.session.rollback()
            return {
                "message": "Error al eliminar el tratamiento.",
                "error": str(e)
            }, 500


class TreatmentDetail(Resource):
    def get(self, treatment_id):
        # Buscar el tratamiento por ID
        treatment = TreatmentModel.query.get(treatment_id)
        if not treatment:
            return {"message": "Tratamiento no encontrado."}, 404

        return {
            "id": treatment.id,
            "description": treatment.description,
            "cost": treatment.cost,
            "pet_id": treatment.pet_id
        }, 200

class TreatmentsByPet(Resource):
    def get(self, pet_id):
        """
        Obtener todos los tratamientos asociados a una mascota específica.
        """
        try:
            # Verificar si la mascota existe
            pet = PetModel.query.get(pet_id)
            if not pet:
                return {"message": "La mascota especificada no existe."}, 404

            # Obtener todos los tratamientos de la mascota
            treatments = TreatmentModel.query.filter_by(pet_id=pet_id).all()
            treatments_list = [
                {
                    "id": treatment.id,
                    "description": treatment.description,
                    "cost": treatment.cost,
                    "appointment_id": treatment.appointment_id,
                }
                for treatment in treatments
            ]

            # Retornar los tratamientos
            return {
                "message": "Tratamientos recuperados exitosamente.",
                "pet_name": pet.name,
                "treatments": treatments_list
            }, 200

        except Exception as e:
            # Manejar errores inesperados
            return {
                "message": "Ocurrió un error al intentar recuperar los tratamientos.",
                "error": str(e)
            }, 500
