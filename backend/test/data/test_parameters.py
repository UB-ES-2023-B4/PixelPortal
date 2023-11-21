class Parameters():
	def __init__(self):
		self._test_user = {
        	"nombre": "Jonadan",
        	"email": "jona@hotmail.com",
        	"contrasena": "Awsome123$"
		}
		self._register_user_list = [
			{"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"},
			{"nombre": "testuser2",     "email": "test@gmail.com",          "contrasena": "testpassword"},
			{"nombre": "testuser3",     "email": "test.ub@alumnes.ub.edu",  "contrasena": "testpassword"},
			{"nombre": "Pepe",          "email": "pepe@gmail.com",          "contrasena": "Qwer!234"}
		]
		self._image_data_list = [
			{"titulo": "string1","descripcion": "string", \
				"usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string1"},
			{"titulo": "string2","descripcion": "string", \
				"usuario_nombre": "Jonadan","tags": "[]", "imagen_url": "string2"},
			{"titulo": "string3","descripcion": "string",\
				"usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string3"},
			{"titulo": "string4","descripcion": "string", \
				"usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string4"}
		]

	def get_test_user(self) -> dict:
		return (self._test_user)
	
	def get_register_user_list(self) -> list:
		return (self._register_user_list)
	
	def get_image_data_list(self) -> list:
		return (self._image_data_list)
	
	def registerUser(self, test_client, user_data) -> dict:
		response = test_client.post("/usuario/", json=user_data)
		assert response.status_code == 200, response.json()
		return (response)

	def registerUsers(self, test_client) -> list:
		for user_data in self._register_user_list:
			response = test_client.post("/usuario/", json=user_data)
			assert response.status_code == 200, response.json()
		return (self._register_user_list)
	
	def login(self, test_client, user_data) -> dict:
		response = test_client.post("/usuario/", json=user_data)
		assert response.status_code == 200, response.json()
		login_user = {"email": user_data["email"], "contrasena": user_data["contrasena"]}
		response = test_client.post("/login/", json=user_data)
		assert response.status_code == 200, response.json()
		return (response)

	def post_image(self, test_client, access_token, image_data):
		headers= {"Authorization": f"Bearer {access_token}"}
		response = test_client.post("/publicaciones", json=image_data, headers=headers)
		return (response)
	
	def post_comment(self, test_client, access_token, userid, pid, comment):
		headers= {"Authorization": f"Bearer {access_token}"}
		json_data = {
			"usuario_id": userid,
			"publicacion_id": pid,
			"contenido": comment
		}
		response = test_client.post("/comentarios", json=json_data, headers=headers)
		return (response)
