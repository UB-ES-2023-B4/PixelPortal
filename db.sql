CREATE TABLE Usuarios (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    contrasena VARCHAR(100),
    descripcion VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE Seguidores (
    seguidor_id BIGINT UNSIGNED,
    seguido_id BIGINT UNSIGNED,
    fecha_creacion TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (seguidor_id, seguido_id),
    FOREIGN KEY (seguidor_id) REFERENCES Usuarios (id),
    FOREIGN KEY (seguido_id) REFERENCES Usuarios (id)
);

CREATE TABLE Publicaciones (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT UNSIGNED,
    titulo VARCHAR(100),
    descripcion VARCHAR(500),
    imagen_url VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios (id)
);

CREATE TABLE Comentarios (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT UNSIGNED,
    publicacion_id BIGINT UNSIGNED,
    contenido TEXT,
    fecha_creacion TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios (id),
    FOREIGN KEY (publicacion_id) REFERENCES Publicaciones (id)
);

CREATE TABLE Likes (
    usuario_id BIGINT UNSIGNED,
    publicacion_id BIGINT UNSIGNED,
    fecha_creacion TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (usuario_id, publicacion_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios (id),
    FOREIGN KEY (publicacion_id) REFERENCES Publicaciones (id)
);
