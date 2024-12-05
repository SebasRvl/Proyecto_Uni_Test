import pytest
from api.models import db, OwnerModel as ClientModel, PetModel, VeterinarianModel, AppointmentModel, TreatmentModel
from app import app
from datetime import datetime

@pytest.fixture
def client():
    """Fixture para configurar el cliente de prueba."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


# Pruebas de clientes
def test_register_client(client):
    response = client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'


def test_register_duplicate_client(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    response = client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    assert response.status_code == 400


def test_update_client(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    response = client.put('/api/clients/1', json={
        "name": "John Smith",
        "email": "johnsmith@example.com",
        "phone": "987654321",
        "address": "456 Elm Street"
    })
    assert response.status_code == 200
    assert response.json['message'] == "Cliente actualizado correctamente."


def test_delete_client(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    response = client.delete('/api/clients/1')
    assert response.status_code == 200
    assert response.json['message'] == "Cliente eliminado exitosamente."


def test_get_client_list(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    response = client.get('/api/clients')
    assert response.status_code == 200
    assert len(response.json['clients']) == 1


def test_get_client_detail(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    response = client.get('/api/clients/1')
    assert response.status_code == 200
    assert response.json['name'] == "John Doe"


# Pruebas de mascotas
def test_register_pet(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    response = client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    assert response.status_code == 201
    assert response.json['message'] == "Mascota registrada exitosamente."


def test_update_pet(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    response = client.put('/api/pets/1', json={
        "name": "Max",
        "species": "Dog",
        "breed": "Labrador",
        "age": 4,
        "owner_id": 1
    })
    assert response.status_code == 200
    assert response.json['message'] == "Mascota actualizada correctamente."


def test_delete_pet(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    response = client.delete('/api/pets/1')
    assert response.status_code == 200
    assert response.json['message'] == "Mascota eliminada exitosamente."


# Pruebas de veterinarios
def test_register_veterinarian(client):
    response = client.post('/api/veterinarians/register', json={
        "name": "Dr. Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    assert response.status_code == 201
    assert response.json['message'] == "Veterinario registrado exitosamente."


def test_update_veterinarian(client):
    client.post('/api/veterinarians/register', json={
        "name": "Dr. Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    response = client.put('/api/veterinarians/1', json={
        "name": "Dr. John Smith",
        "email": "drjohnsmith@example.com",
        "phone": "555-6666",
        "specialty": "Surgery"
    })
    assert response.status_code == 200


def test_delete_veterinarian(client):
    client.post('/api/veterinarians/register', json={
        "name": "Dr. Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    response = client.delete('/api/veterinarians/1')
    assert response.status_code == 200
    assert response.json['message'] == "Veterinario eliminado exitosamente."


# Pruebas de citas
def test_register_appointment(client):
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    response = client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1
    })
    assert response.status_code == 201
    assert response.json['message'] == "Cita registrada exitosamente."
def test_update_appointment_not_found(client):
    # Intentar actualizar una cita que no existe
    response = client.put('/api/appointments/1', json={
        "date": "2023-12-10 14:30",
        "reason": "Updated reason",
        "pet_id": 1,
        "veterinarian_id": 1
    })
    assert response.status_code == 404
    assert response.json['message'] == "Cita no encontrada."


def test_update_appointment_error(client, mocker):
    # Crear datos iniciales
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1
    })

    # Simular un error en la base de datos
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar actualizar la cita
    response = client.put('/api/appointments/1', json={
        "date": "2023-12-11 10:00",
        "reason": "Updated reason",
        "pet_id": 1,
        "veterinarian_id": 1
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al actualizar la cita."
    assert "error" in response.json
def test_register_client_duplicate_email(client):
    # Registrar un cliente con un correo
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    # Intentar registrar otro cliente con el mismo correo
    response = client.post('/api/clients/register', json={
        "name": "Jane Doe",
        "email": "johndoe@example.com",  # Misma dirección de correo
        "phone": "987654321",
        "address": "456 Elm Street"
    })
    assert response.status_code == 400
    assert response.json['message'] == "El correo ya está registrado."
    assert response.json['status'] == "error"


def test_register_client_db_error(client, mocker):
    # Simular un error en la base de datos
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))
    
    # Intentar registrar un cliente
    response = client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al registrar el cliente."
    assert response.json['status'] == "error"
    assert "error" in response.json
def test_update_client_not_found(client):
    # Intentar actualizar un cliente que no existe
    response = client.put('/api/clients/1', json={
        "name": "John Updated",
        "email": "johnupdated@example.com",
        "phone": "987654321",
        "address": "456 Updated Street"
    })
    assert response.status_code == 404
    assert response.json['message'] == "Cliente no encontrado."


def test_update_client_db_error(client, mocker):
    # Crear un cliente inicial
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })

    # Simular un error en la base de datos durante el commit
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar actualizar el cliente
    response = client.put('/api/clients/1', json={
        "name": "John Updated",
        "email": "johnupdated@example.com",
        "phone": "987654321",
        "address": "456 Updated Street"
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al actualizar el cliente."
    assert "error" in response.json
def test_delete_client_not_found(client):
    # Intentar eliminar un cliente que no existe
    response = client.delete('/api/clients/1')
    assert response.status_code == 404
    assert response.json['message'] == "Cliente no encontrado."


def test_delete_client_db_error(client, mocker):
    # Crear un cliente
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })

    # Simular un error en la base de datos durante la eliminación
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar eliminar el cliente
    response = client.delete('/api/clients/1')
    assert response.status_code == 500
    assert response.json['message'] == "Error al eliminar el cliente."
    assert "error" in response.json


def test_get_client_detail_not_found(client):
    # Intentar obtener detalles de un cliente que no existe
    response = client.get('/api/clients/1')
    assert response.status_code == 404
    assert response.json['message'] == "Cliente no encontrado."


def test_get_client_detail_success(client):
    # Registrar un cliente
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })

    # Obtener detalles del cliente
    response = client.get('/api/clients/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name'] == "John Doe"
    assert response.json['email'] == "johndoe@example.com"
    assert response.json['phone'] == "123456789"
    assert response.json['address'] == "123 Main Street"
def test_register_pet_owner_not_found(client):
    # Intentar registrar una mascota con un dueño inexistente
    response = client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1  # Dueño inexistente
    })
    assert response.status_code == 400
    assert response.json['message'] == "El dueño especificado no existe."


def test_register_pet_db_error(client, mocker):
    # Crear un dueño
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })

    # Simular un error en la base de datos durante el registro
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar registrar una mascota
    response = client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al registrar la mascota."
    assert "error" in response.json
def test_update_pet_not_found(client):
    # Intentar actualizar una mascota que no existe
    response = client.put('/api/pets/1', json={
        "name": "Buddy Updated",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 4,
        "owner_id": 1
    })
    assert response.status_code == 404
    assert response.json['message'] == "Mascota no encontrada."


def test_update_pet_db_error(client, mocker):
    # Crear un dueño y una mascota inicial
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })

    # Simular un error en la base de datos durante la actualización
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar actualizar la mascota
    response = client.put('/api/pets/1', json={
        "name": "Buddy Updated",
        "species": "Dog",
        "breed": "Labrador Retriever",
        "age": 4,
        "owner_id": 1
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al actualizar la mascota."
    assert "error" in response.json
def test_delete_pet_not_found(client):
    # Intentar eliminar una mascota que no existe
    response = client.delete('/api/pets/1')
    assert response.status_code == 404
    assert response.json['message'] == "Mascota no encontrada."


def test_delete_pet_success(client):
    # Crear un dueño y una mascota inicial
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })

    # Eliminar la mascota
    response = client.delete('/api/pets/1')
    assert response.status_code == 200
    assert response.json['message'] == "Mascota eliminada exitosamente."


def test_delete_pet_db_error(client, mocker):
    # Crear un dueño y una mascota inicial
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })

    # Simular un error en la base de datos durante la eliminación
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar eliminar la mascota
    response = client.delete('/api/pets/1')
    assert response.status_code == 500
    assert response.json['message'] == "Error al eliminar la mascota."
    assert "error" in response.json
def test_get_pet_detail_not_found(client):
    # Intentar obtener detalles de una mascota que no existe
    response = client.get('/api/pets/1')
    assert response.status_code == 404
    assert response.json['message'] == "Mascota no encontrada."


def test_get_pet_detail_success(client):
    # Crear un dueño y una mascota inicial
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })

    # Obtener detalles de la mascota
    response = client.get('/api/pets/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name'] == "Buddy"
    assert response.json['species'] == "Dog"
    assert response.json['breed'] == "Golden Retriever"
    assert response.json['age'] == 3
    assert response.json['owner_id'] == 1
def test_get_pets_by_owner_not_found(client):
    # Intentar obtener mascotas de un dueño que no existe
    response = client.get('/api/owners/1/pets')
    assert response.status_code == 404
    assert response.json['message'] == "Dueño no encontrado."


def test_get_pets_by_owner_no_pets(client):
    # Crear un dueño sin mascotas
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })

    # Intentar obtener mascotas del dueño
    response = client.get('/api/owners/1/pets')
    assert response.status_code == 200
    assert response.json['owner'] == "John Doe"
    assert response.json['pets'] == []


def test_get_pets_by_owner_with_pets(client):
    # Crear un dueño y registrar mascotas
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/pets/register', json={
        "name": "Kitty",
        "species": "Cat",
        "breed": "Persian",
        "age": 2,
        "owner_id": 1
    })

    # Obtener mascotas del dueño
    response = client.get('/api/owners/1/pets')
    assert response.status_code == 200
    assert response.json['owner'] == "John Doe"
    assert len(response.json['pets']) == 2
    assert response.json['pets'][0]['name'] == "Buddy"
    assert response.json['pets'][1]['name'] == "Kitty"
def test_register_veterinarian_duplicate_email(client):
    # Registrar un veterinario con un correo
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    # Intentar registrar otro veterinario con el mismo correo
    response = client.post('/api/veterinarians/register', json={
        "name": "Dr. Jane Doe",
        "email": "drsmith@example.com",  # Misma dirección de correo
        "phone": "555-6666",
        "specialty": "Surgery"
    })
    assert response.status_code == 400
    assert response.json['message'] == "El correo ya está registrado."


def test_register_veterinarian_db_error(client, mocker):
    # Simular un error en la base de datos durante el registro
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar registrar un veterinario
    response = client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al registrar el veterinario."
    assert "error" in response.json
def test_update_veterinarian_not_found(client):
    # Intentar actualizar un veterinario que no existe
    response = client.put('/api/veterinarians/1', json={
        "name": "Dr. John Updated",
        "email": "drjohnupdated@example.com",
        "phone": "555-8888",
        "specialty": "Cardiology"
    })
    assert response.status_code == 404
    assert response.json['message'] == "Veterinario no encontrado."


def test_update_veterinarian_success(client):
    # Crear un veterinario inicial
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Actualizar el veterinario
    response = client.put('/api/veterinarians/1', json={
        "name": "Dr. John Updated",
        "email": "drjohnupdated@example.com",
        "phone": "555-8888",
        "specialty": "Cardiology"
    })
    assert response.status_code == 200
    assert response.json['message'] == "Veterinario actualizado correctamente."


def test_update_veterinarian_db_error(client, mocker):
    # Crear un veterinario inicial
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Simular un error en la base de datos durante la actualización
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar actualizar el veterinario
    response = client.put('/api/veterinarians/1', json={
        "name": "Dr. John Updated",
        "email": "drjohnupdated@example.com",
        "phone": "555-8888",
        "specialty": "Cardiology"
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al actualizar el veterinario."
    assert "error" in response.json
def test_delete_veterinarian_not_found(client):
    # Intentar eliminar un veterinario que no existe
    response = client.delete('/api/veterinarians/1')
    assert response.status_code == 404
    assert response.json['message'] == "Veterinario no encontrado."


def test_delete_veterinarian_success(client):
    # Crear un veterinario inicial
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Eliminar el veterinario
    response = client.delete('/api/veterinarians/1')
    assert response.status_code == 200
    assert response.json['message'] == "Veterinario eliminado exitosamente."


def test_delete_veterinarian_db_error(client, mocker):
    # Crear un veterinario inicial
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Simular un error en la base de datos durante la eliminación
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar eliminar el veterinario
    response = client.delete('/api/veterinarians/1')
    assert response.status_code == 500
    assert response.json['message'] == "Error al eliminar el veterinario."
    assert "error" in response.json
def test_get_veterinarian_detail_not_found(client):
    # Intentar obtener detalles de un veterinario que no existe
    response = client.get('/api/veterinarians/1')
    assert response.status_code == 404
    assert response.json['message'] == "Veterinario no encontrado."


def test_get_veterinarian_detail_success(client):
    # Crear un veterinario inicial
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Obtener detalles del veterinario
    response = client.get('/api/veterinarians/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['name'] == "Dr. John Smith"
    assert response.json['email'] == "drsmith@example.com"
    assert response.json['phone'] == "555-5555"
    assert response.json['specialty'] == "Dentistry"
def test_get_veterinarian_list_empty(client):
    # Intentar obtener la lista de veterinarios cuando no hay ninguno registrado
    response = client.get('/api/veterinarians')
    assert response.status_code == 200
    assert response.json['veterinarians'] == []


def test_get_veterinarian_list_with_data(client):
    # Crear veterinarios iniciales
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. Jane Doe",
        "email": "drjanedoe@example.com",
        "phone": "555-6666",
        "specialty": "Surgery"
    })

    # Obtener la lista de veterinarios
    response = client.get('/api/veterinarians')
    assert response.status_code == 200
    assert len(response.json['veterinarians']) == 2
    assert response.json['veterinarians'][0]['name'] == "Dr. John Smith"
    assert response.json['veterinarians'][1]['name'] == "Dr. Jane Doe"
def test_register_appointment_pet_not_found(client):
    # Crear un veterinario
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Intentar registrar una cita con un `pet_id` inexistente
    response = client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,  # Mascota inexistente
        "veterinarian_id": 1
    })
    assert response.status_code == 404
    assert response.json['message'] == "La mascota especificada no existe."


def test_register_appointment_veterinarian_not_found(client):
    # Crear una mascota
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })

    # Intentar registrar una cita con un `veterinarian_id` inexistente
    response = client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1  # Veterinario inexistente
    })
    assert response.status_code == 404
    assert response.json['message'] == "El veterinario especificado no existe."


def test_register_appointment_db_error(client, mocker):
    # Crear una mascota y un veterinario
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })

    # Simular un error en la base de datos durante el registro
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar registrar una cita
    response = client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1
    })
    assert response.status_code == 500
    assert response.json['message'] == "Error al registrar la cita."
    assert "error" in response.json
def test_delete_appointment_not_found(client):
    # Intentar eliminar una cita que no existe
    response = client.delete('/api/appointments/1')
    assert response.status_code == 404
    assert response.json['message'] == "Cita no encontrada."


def test_delete_appointment_success(client):
    # Crear una mascota y un veterinario
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    # Crear una cita
    client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1
    })

    # Eliminar la cita
    response = client.delete('/api/appointments/1')
    assert response.status_code == 200
    assert response.json['message'] == "Cita eliminada exitosamente."


def test_delete_appointment_db_error(client, mocker):
    # Crear una mascota, un veterinario y una cita
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1
    })

    # Simular un error en la base de datos durante la eliminación
    mocker.patch('api.models.db.session.commit', side_effect=Exception('Database error'))

    # Intentar eliminar la cita
    response = client.delete('/api/appointments/1')
    assert response.status_code == 500
    assert response.json['message'] == "Error al eliminar la cita."
    assert "error" in response.json
def test_get_treatment_detail_not_found(client):
    # Intentar obtener detalles de un tratamiento que no existe
    response = client.get('/api/treatments/1')
    assert response.status_code == 404
    assert response.json['message'] == "Tratamiento no encontrado."


def test_get_appointment_detail_not_found(client):
    # Intentar obtener detalles de una cita que no existe
    response = client.get('/api/appointments/1')
    assert response.status_code == 404
    assert response.json['message'] == "Cita no encontrada."


def test_get_appointment_detail_success(client):
    # Crear una mascota y un veterinario para registrar una cita
    client.post('/api/clients/register', json={
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "address": "123 Main Street"
    })
    client.post('/api/pets/register', json={
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "owner_id": 1
    })
    client.post('/api/veterinarians/register', json={
        "name": "Dr. John Smith",
        "email": "drsmith@example.com",
        "phone": "555-5555",
        "specialty": "Dentistry"
    })
    client.post('/api/appointments/register', json={
        "date": "2023-12-10 14:30",
        "reason": "Routine checkup",
        "pet_id": 1,
        "veterinarian_id": 1
    })

    # Obtener detalles de la cita
    response = client.get('/api/appointments/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['date'] == "2023-12-10 14:30"
    assert response.json['reason'] == "Routine checkup"
    assert response.json['pet_id'] == 1
    assert response.json['veterinarian_id'] == 1
def test_delete_treatment_not_found(client):
    # Intentar eliminar un tratamiento que no existe
    response = client.delete('/api/treatments/1')
    assert response.status_code == 404
    assert response.json['message'] == "Tratamiento no encontrado."


