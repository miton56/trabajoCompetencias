create database trabajo;

use trabajo;

CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(15),
    nombre VARCHAR(100)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(500),
    precio INT,
    cantidad_stock INT,
    categoria VARCHAR(100),
    nombre VARCHAR(100),
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(12),
    nombre VARCHAR(100),
    direccion VARCHAR(500),
    telefono INT
);

CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha DATE,
    monto_total INT,
    estado ENUM('pendiente', 'pagado', 'cancelado') DEFAULT 'pendiente',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE detalle_ventas (
    id_detalle_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    id_venta INT,
    cantidad INT,
    precio_unitario INT,
    subtotal INT,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
);

CREATE TABLE metodo_de_pago (
    id_metodo_pago INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    descuento INT
);

CREATE TABLE detalle_metodo_pago (
    id_detalle_metodo INT AUTO_INCREMENT PRIMARY KEY,
    id_metodo_pago INT,
    id_venta INT,
    monto_pagado INT,
    FOREIGN KEY (id_metodo_pago) REFERENCES metodo_de_pago(id_metodo_pago),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
);

-- Insertar proveedores
INSERT INTO proveedores (rut, nombre) VALUES
('76451234-5', 'Distribuidora El Sol'),
('76342345-6', 'Importadora Andes'),
('76123456-7', 'Comercial Santa Marta'),
('76567890-1', 'Proveedora La Esperanza'),
('76890123-4', 'Suministros Patagonia'),
('76987654-3', 'Distribuciones Norte'),
('76765432-1', 'Logística Central'),
('76234567-8', 'Mayorista Sur Ltda.'),
('76112233-4', 'Mercantil Los Lagos'),
('76551234-2', 'Comercial Altura');

-- Insertar productos
INSERT INTO productos (descripcion, precio, cantidad_stock, categoria, nombre, id_proveedor) VALUES
('Smartphone Android 6.5" 128GB', 180000, 25, 'Tecnología', 'Samsung Galaxy A14', 1),
('Notebook Intel i5 8GB RAM 256SSD', 450000, 12, 'Computación', 'Lenovo IdeaPad 3', 2),
('Zapatillas deportivas hombre talla 42', 45000, 30, 'Calzado', 'Nike Revolution 6', 3),
('Aspiradora 1800W ciclónica', 65000, 10, 'Electrodomésticos', 'Thomas Turbo Compact', 4),
('Televisor LED 43" Full HD', 220000, 8, 'Tecnología', 'LG Smart TV 43LF6300', 5),
('Set de ollas acero inoxidable 7 piezas', 58000, 20, 'Hogar', 'Urbano Home Pro', 6),
('Silla ergonómica oficina con respaldo malla', 72000, 15, 'Muebles', 'ErgoFit Pro', 7),
('Parlante Bluetooth portátil resistente al agua', 39000, 18, 'Tecnología', 'JBL GO 3', 8),
('Polera algodón unisex talla M', 9500, 50, 'Vestuario', 'Polera Básica H&M', 9),
('Mochila escolar con diseño ergonómico', 27000, 22, 'Accesorios', 'Totto Urban Pack', 10);

-- Insertar clientes
INSERT INTO clientes (rut, nombre, direccion, telefono) VALUES
('20123456-7', 'Camila Reyes', 'Av. Providencia 2345, Santiago', 987654321),
('20234567-8', 'Martín Rojas', 'Calle Condell 123, Viña del Mar', 912345678),
('20345678-9', 'Lucía Fuentes', 'Av. O''Higgins 456, Rancagua', 934567890),
('20456789-0', 'Diego Contreras', 'Calle Balmaceda 321, La Serena', 923456789),
('20567890-1', 'Javiera Paredes', 'Pasaje Los Robles 789, Chillán', 987123456),
('20678901-2', 'Tomás Sepúlveda', 'Av. Alemania 999, Temuco', 976543210),
('20789012-3', 'Catalina Saavedra', 'Camino Real 1234, Valdivia', 954321987),
('20890123-4', 'Benjamín Lagos', 'Callejón Aurora 555, Calama', 963258741),
('20901234-5', 'Isidora Aravena', 'Av. Argentina 101, Antofagasta', 987654987),
('21012345-6', 'Matías Herrera', 'Calle Los Pinos 777, Osorno', 912312312);

-- Insertar ventas
INSERT INTO ventas (id_cliente, fecha, monto_total, estado) VALUES
(1, '2025-04-01', 180000, 'pagado'),
(2, '2025-04-02', 450000, 'pendiente'),
(3, '2025-04-03', 9500, 'cancelado'),
(4, '2025-04-04', 220000, 'pagado'),
(5, '2025-04-05', 39000, 'pendiente'),
(6, '2025-04-06', 65000, 'pagado'),
(7, '2025-04-07', 27000, 'pendiente'),
(8, '2025-04-08', 72000, 'pagado'),
(9, '2025-04-09', 58000, 'cancelado'),
(10, '2025-04-10', 45000, 'pagado');

-- Insertar detalle de ventas
INSERT INTO detalle_ventas (id_producto, id_venta, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 180000, 180000),
(2, 2, 1, 450000, 450000),
(9, 3, 1, 9500, 9500),
(5, 4, 1, 220000, 220000),
(8, 5, 1, 39000, 39000),
(4, 6, 1, 65000, 65000),
(10, 7, 1, 27000, 27000),
(7, 8, 1, 72000, 72000),
(6, 9, 1, 58000, 58000),
(3, 10, 1, 45000, 45000);

-- Insertar métodos de pago
INSERT INTO metodo_de_pago (nombre, descuento) VALUES
('Efectivo', 10),
('Tarjeta de Crédito', 5),
('Tarjeta de Débito', 3),
('Transferencia Bancaria', 0),
('Cheque', 2),
('PayPal', 4),
('Criptomonedas', 15),
('Tarjeta de Regalo', 20),
('Aplicación móvil', 8),
('Pago contra entrega', 0);

-- Insertar detalle de métodos de pago
INSERT INTO detalle_metodo_pago (id_metodo_pago, id_venta, monto_pagado) VALUES
(1, 1, 180000),
(2, 2, 450000),
(3, 3, 9500),
(4, 4, 220000),
(5, 5, 39000),
(6, 6, 65000),
(7, 7, 27000),
(8, 8, 72000),
(9, 9, 58000),
(10, 10, 45000);

