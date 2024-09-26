

-- CREATE TABLE inventarios(
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     id_producto INT NOT NULL,
--     tipo_producto VARCHAR(100) NOT NULL,
--     stock INT NOT NULL,
--     INDEX indx_id_producto_tipo_producto(id_producto, tipo_producto)
-- )

CREATE TABLE usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(25),
    estado_usuario VARCHAR(10),
    username VARCHAR(25),
    password VARCHAR(25),
    email VARCHAR(25),
    telefono CHAR(10)    
);

SELECT * usuarios u WHERE u.id =

CREATE TABLE vehiculo(
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(10) UNIQUE, 
    marca VARCHAR(100),
    modelo VARCHAR(100), 
    tipo_vehiculo VARCHAR(100), 
    color VARCHAR(50),
    precio_de_venta DECIMAL(10, 2)
);

CREATE TABLE clientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_de_cedula VARCHAR(10) UNIQUE,
    nombres VARCHAR(200), 
    apellidos VARCHAR(200), 
    dirección VARCHAR(600), 
    ciudad VARCHAR(50),
    telefono VARCHAR(10), 
    estado VARCHAR(30)
);

SELECT vh.* 
FROM vehiculo vh
LEFT JOIN ventas vt ON vh.id = vt.id_vehiculo
WHERE vt.id_vehiculo IS NULL;

SELECT 
    vh.marca, 
    vh.modelo, 
    vh.color, 
    vh.precio_de_venta, 
    COUNT(vh.id) AS cantidad_disponible
FROM vehiculo vh
LEFT JOIN ventas vt ON vh.id = vt.id_vehiculo
WHERE vt.id_vehiculo IS NULL
GROUP BY vh.marca, vh.modelo, vh.color, vh.precio_de_venta;

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_vehiculo INT NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vehiculo FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id),
    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);


CREATE TABLE mantenimiento(
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_revision VARCHAR(50),
    tipo_vehiculo VARCHAR(50),    
    precio DECIMAL(10, 2)
);

INSERT INTO mantenimiento VALUES("cambio de filtro", 19.87,"Mediano"), ("cambio de aceite", 34, "Mediano"),("cambio de frenos", 23, "Mediano")

CREATE TABLE revisiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora_recepcion TIMESTAMP, 
    fecha_hora_entrega TIMESTAMP,
    id_mantenimiento INT,
    id_vehiculo INT,
    CONSTRAINT fk_mantenimiento FOREIGN KEY (id_mantenimiento) REFERENCES mantenimiento(id),
    CONSTRAINT fk_vehiculo FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id),
);

la fecha y hora de recepción, fecha y hora de entrega. Los vehículos pueden pasar
varias revisiones en el concesionario

Relaciones:
cliente 1-* compra(ventas) 1-* vehiculo
mantenimiento 1-* revisiones *-1 vehiculo 

-- Todas los vehiculo comprados por un cliente 
SELECT vh.* FROM clientes c, vehiculo vh, ventas vt 
WHERE c.id= vt.id_cliente AND vh.id=vt.id_producto AND c.numero_de_cedula=:numero_de_cedula;

-- Todas los vehiculo comprados por un cliente 
SELECT vh.* 
FROM vehiculo vh 
JOIN ventas vt ON vt.id_vehiculo=vh.id
JOIN clientes c ON c.id=vt.id_cliente
WHERE c.numero_de_cedula="1353224598";
-- todas las revisiones de un vehiculo en concreto por maticula ordenado por fecha

SELECT rv.fecha_hora_recepcion, rv.fecha_hora_entrega, 
m.tipo_revision, m.precio, 
vh.matricula, vh.marca, vh.modelo, vh.color
FROM revisiones rv, mantenimiento m, vehiculo vh 
WHERE rv.id_mantenimiento=m.id 
AND rv.id_vehiculo = vh.id 
AND vh.matricula='MAS-761'
ORDER BY rv.fecha_hora_recepcion, rv.fecha_hora_entrega;

SELECT rv.fecha_hora_recepcion, rv.fecha_hora_entrega, 
m.tipo_revision, m.precio, 
vh.matricula, vh.marca, vh.modelo, vh.color
FROM revisiones rv
JOIN mantenimiento m ON rv.id_mantenimiento = m.id
JOIN vehiculos vh ON rv.id_vehiculo = vh.id
AND vh.matricula='MAS-761'
ORDER BY rv.fecha_hora_recepcion, rv.fecha_hora_entrega;

