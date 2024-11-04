CREATE DATABASE IF NOT EXISTS banco;
USE banco;

-- Tabla de Usuarios
CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE
);

-- Tabla de Tarjetas
CREATE TABLE tarjetas (
    tarjeta_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    cvv VARCHAR(4) NOT NULL,
    tipo_tarjeta ENUM('credito', 'debito') NOT NULL,
    fecha_caducidad DATE NOT NULL,
    fecha_emision DATE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de Cuentas
CREATE TABLE cuentas (
    cuenta_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tarjeta_id INT,
    numero_cuenta VARCHAR(20) NOT NULL,
    clave_4digitos CHAR(4) NOT NULL,
    clave_6digitos CHAR(6) NOT NULL,
    saldo DECIMAL(15, 2) DEFAULT 0.0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (tarjeta_id) REFERENCES tarjetas(tarjeta_id) ON DELETE SET NULL
);

-- Tabla de Depósitos
CREATE TABLE depositos (
    deposito_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_depo DATE NOT NULL,
    cantidad_depo DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de Transferencias
CREATE TABLE transferencias (
    transferencia_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    receptor INT NOT NULL, -- ID del usuario receptor
    fecha_transf DATE NOT NULL,
    cantidad_transf DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (receptor) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de Consultas
CREATE TABLE consultas (
    consulta_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_consulta DATE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de Retiros
CREATE TABLE retiros (
    retiro_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_retiro DATE NOT NULL,
    cantidad_retiro DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Población de la tabla Usuarios
INSERT INTO usuarios (dni, nombres, apellido_paterno, apellido_materno, fecha_nacimiento) VALUES
('12345678', 'Carlos', 'Pérez', 'Gómez', '1985-02-15'),
('87654321', 'María', 'López', 'Fernández', '1990-05-25'),
('45612378', 'José', 'Martínez', 'Ramos', '1987-11-07'),
('78945612', 'Ana', 'Sánchez', 'Morales', '1992-03-20');

-- Población de la tabla Tarjetas
INSERT INTO tarjetas (usuario_id, numero, cvv, tipo_tarjeta, fecha_caducidad, fecha_emision) VALUES
(1, '1234123412341234', '123', 'credito', '2025-12-31', '2023-01-01'),
(2, '5678567856785678', '456', 'debito', '2024-10-20', '2022-03-01'),
(3, '8765876587658765', '789', 'credito', '2026-08-15', '2023-07-10'),
(4, '2345234523452345', '234', 'debito', '2023-11-01', '2020-02-20');

-- Población de la tabla Cuentas
INSERT INTO cuentas (usuario_id, tarjeta_id, numero_cuenta, clave_4digitos, clave_6digitos, saldo) VALUES
(1, 1, '1111222233334444', '1234', '123456', 1500.50),
(2, 2, '5555666677778888', '4321', '654321', 2000.00),
(3, 3, '9999000011112222', '5678', '789012', 300.75),
(4, 4, '3333444455556666', '8765', '098765', 5000.25);

-- Población de la tabla Depósitos
INSERT INTO depositos (usuario_id, fecha_depo, cantidad_depo) VALUES
(1, '2024-01-15', 500.00),
(2, '2024-02-10', 1000.00),
(3, '2024-03-20', 200.00),
(4, '2024-04-25', 750.00);

-- Población de la tabla Transferencias
INSERT INTO transferencias (usuario_id, receptor, fecha_transf, cantidad_transf) VALUES
(1, 2, '2024-05-10', 150.00),
(2, 3, '2024-06-15', 300.00),
(3, 4, '2024-07-25', 200.00),
(4, 1, '2024-08-05', 500.00);

-- Población de la tabla Consultas
INSERT INTO consultas (usuario_id, fecha_consulta) VALUES
(1, '2024-01-05'),
(2, '2024-02-12'),
(3, '2024-03-15'),
(4, '2024-04-20');

-- Población de la tabla Retiros
INSERT INTO retiros (usuario_id, fecha_retiro, cantidad_retiro) VALUES
(1, '2024-01-10', 100.00),
(2, '2024-02-18', 250.00),
(3, '2024-03-25', 50.00),
(4, '2024-04-30', 300.00);
