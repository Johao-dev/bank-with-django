// funcion general para hacer una peticion POST al backend (auth_view.py y operations_view.py)
function makePostRequest(url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // incluye el token CSRF
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            alert(`Error: ${response.statusText}`);
            return;
        }
        return response.json();
    })
    .catch(err => {
        console.error(`Error en la petición: ${err.message}`);
    });
}

// función para obtener el token de seguridad
function getCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith(name))
        ?.split('=')[1];
    return cookieValue;
}

/*
    Todas las siguientes funciones llaman a la funcion general para hacer
    peticiones al backend, simplificando el codigo.
*/

// función para la consulta de saldo
function consultar() {
    makePostRequest('/banco/consultar/')
    .then(data => {
        if (data) alert(data.saldo);
    });
}

// función para la transferencia
function transferir() {
    const num_tarjeta_receptor = prompt("Ingrese el numero de tarjeta del receptor:");
    const nombre_receptor = prompt("Ingrese el nombre del receptor:");
    const cantidad = prompt("Ingrese la cantidad a transferir:");

    if (confirm("¿Estás seguro de realizar la transferencia?")) {
        if (num_tarjeta_receptor && nombre_receptor && cantidad) {
            makePostRequest('/banco/transferir/', {
                tarjeta_receptor: num_tarjeta_receptor,
                nombre_receptor: nombre_receptor,
                cantidad: parseFloat(cantidad)
            })
            .then(data => {
                alert(data?.mensaje || "Ocurrió un error al realizar la transferencia.");
            });
        }
    }
}

// función para el depósito
function depositar() {
    const cantidad = prompt("Ingrese la cantidad a depositar:");

    if (cantidad) {
        makePostRequest('/banco/depositar/', {
            cantidad: parseFloat(cantidad)
        })
        .then(data => {
            alert(data?.mensaje || "Ocurrió un error al realizar el depósito.");
        });
    }
}

// función para el retiro
function retirar() {
    const cantidad = prompt("Ingrese la cantidad a retirar:");

    if (cantidad) {
        makePostRequest('/banco/retirar/', {
            cantidad: parseFloat(cantidad)
        })
        .then(data => {
            alert(data?.mensaje || "Ocurrió un error al realizar el retiro.");
        });
    }
}

// funcion para cerrar sesion
function logout() {
    makePostRequest('/banco/logout/')
    .then(() => {
        alert("Has cerrado sesión correctamente.");
        window.location.href = "/banco/";
    });
}