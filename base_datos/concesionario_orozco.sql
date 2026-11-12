CREATE DATABASE concesionario_orozco;

USE concesionario_orozco;

CREATE TABLE concesionario (
    id_concesionario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    whatsapp VARCHAR(20),
    facebook VARCHAR(255),
    instagram VARCHAR(255),
    horario_atencion VARCHAR(150)
);

CREATE TABLE administrador (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE modelo (
    id_modelo INT AUTO_INCREMENT PRIMARY KEY,
    id_marca INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_marca) REFERENCES marca(id_marca) ON DELETE CASCADE
);

CREATE TABLE vehiculo (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    id_modelo INT NOT NULL,
    anio INT NOT NULL,
    precio DECIMAL(14,2) NOT NULL,
    kilometraje INT DEFAULT 0,
    combustible ENUM('Gasolina','Diésel','Híbrido','Eléctrico','Gas') DEFAULT 'Gasolina',
    transmision ENUM('Manual','Automática') DEFAULT 'Manual',
    color VARCHAR(50),
    tipo ENUM('Automóvil','Camioneta','SUV','Pickup','Camión') NOT NULL,
    descripcion TEXT,
    estado ENUM('Disponible','Reservado','Vendido') DEFAULT 'Disponible',
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_modelo) REFERENCES modelo(id_modelo) ON DELETE RESTRICT,
    INDEX idx_precio (precio),
    INDEX idx_anio (anio),
    INDEX idx_tipo (tipo)
);

CREATE TABLE fotografia (
    id_foto INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT NOT NULL,
    url_imagen VARCHAR(500) NOT NULL,
    es_principal BOOLEAN DEFAULT FALSE,
    orden INT DEFAULT 0,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo) ON DELETE CASCADE
);
