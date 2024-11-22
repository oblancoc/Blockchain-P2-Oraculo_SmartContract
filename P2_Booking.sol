// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Repositorio {
    // Estructura para almacenar los datos del espacio
    struct Datos {
        uint256 espaciosDisponibles;  // Número de espacios disponibles
        uint256 precio;              // Precio por hora del espacio en Gwei
    }

    address public owner;          // Propietario del contrato
    Datos public data;             // Datos del espacio (vienen del oráculo)
    uint256 public totalIngresos;  // Total de ingresos acumulados por arriendo. Renta acumulada

    // Eventos
    event EspacioReservado(address usuario, uint256 espaciosReservados, uint256 horas, uint256 monto);

    // Se almacena la dirección establece el propietario del contrato al desplegar
    constructor(uint256 _espaciosDisponibles, uint256 _precio) payable  {
        owner = msg.sender;
        data = Datos({
            espaciosDisponibles: _espaciosDisponibles,
            precio: _precio
        });
    }

    // Función para consultar disponibilidad y precio (accesible para todos)
    function consultarEspacio() public view returns (uint256, uint256) {
        return (data.espaciosDisponibles, data.precio);
    }

    // Función para reservar x cantidad de espacio
    function reservar(uint256 espaciosReservados, uint256 horas) public payable {

        uint256 montoTotalGwei = espaciosReservados * horas * data.precio;

        // Validaciones iniciales
        require(data.espaciosDisponibles >= espaciosReservados, "No hay suficientes espacios disponibles");
        require(horas >= 2 && horas <= 10, "Debes reservar entre 2 y 10 horas");
        require(msg.value / 1 gwei >= montoTotalGwei, "El monto enviado es menor del costo total para arrendar");

        // Descuenta los espacios reservados
        data.espaciosDisponibles -= espaciosReservados;

        // Suma los ingresos totales
        totalIngresos += montoTotalGwei;

        // Emite un evento para registrar la reserva
        emit EspacioReservado(msg.sender, espaciosReservados, horas, msg.value);
    }

    // Función para el propietario: consultar ingresos totales acumulados
    function consultarIngresos() public view returns (uint256) {
        require(msg.sender == owner, "Solo el propietario puede consultar los ingresos");
        return totalIngresos;
    }

    // Función para el propietario: retirar los ingresos acumulados
    function retirarIngresos() public {
        require(msg.sender == owner, "Solo el propietario puede retirar los ingresos");
        require(totalIngresos > 0, "No hay ingresos disponibles para retirar");
        
        
        uint256 montoRetirar = totalIngresos * 1 gwei;
        totalIngresos = 0;

        payable(owner).transfer(montoRetirar);

    }

    // Función para el oráculo: actualizar disponibilidad y precio (solo oráculo autorizado)
    function actualizarDatos(uint256 _espaciosDisponibles, uint256 _precio) public {
        require(msg.sender == owner, "Solo el propietario puede actualizar los datos");
        data.espaciosDisponibles = _espaciosDisponibles;
        data.precio = _precio;
    }
}
