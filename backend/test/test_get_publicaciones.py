from data.test_parameters import Parameters

image_data_list = [
    {
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[]",
        "imagen_url": "string"
    	},
	{
        "titulo": "Tiiitulo con espacios entre medio",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[\"azul\"]",
        "imagen_url": "string"
		},
	{
        "titulo": "lorem ipsum",
        "descripcion": """
		Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Nullam gravida odio nec diam consectetur, vel finibus lectus tincidunt. 
        Ut vulputate libero vel quam fringilla, nec dapibus dui consequat. 
        Aenean volutpat tellus eu libero cursus, vel posuere neque lacinia. 
        Suspendisse potenti. Quisque nec metus sit amet purus aliquam facilisis. 
        Integer lacinia erat vel lacus euismod, vitae tincidunt massa eleifend. 
        Donec ultricies, erat vel auctor venenatis, arcu lectus volutpat mi, 
        sit amet convallis mauris odio id nisl.
        """,
        "usuario_nombre": "string",
        "tags": "[\"blanco y negro\"]",
        "imagen_url": "string"
    	},
	{
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "Usuario tonto",
        "tags": "[\"gato\", \"perro\", \"pajaro\", \"lagarto\"]",
        "imagen_url": "string"
    	}
]

def test_get_publicaciones(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in image_data_list:
        Parameters().post_image(test_client, access_token, image_data)
    response = test_client.get("/publicaciones/")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data
    assert len(response_data) == 4, response_data