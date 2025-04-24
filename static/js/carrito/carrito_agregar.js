    // ------------------- AGREGAR AL CARRITO -----------------------
    

function modificarCantidad(cambio) {
    const cantidadEl = document.getElementById('prod-cantidad');
    let cantidad = parseInt(cantidadEl.textContent);

    const nuevaCantidad = cantidad + cambio;

    if (nuevaCantidad < 1) {
        alert('La cantidad no debe ser menor a 1');
        return;
    }

    cantidadEl.textContent = nuevaCantidad;
}

document.getElementById('prod-btn-restar').addEventListener('click', function() {
    modificarCantidad(-1);
});

document.getElementById('prod-btn-sumar').addEventListener('click', function() {
    modificarCantidad(1);
});

// Manejo del envío del formulario
document.getElementById('producto-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío predeterminado del formulario

    const form = event.target;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const cantidad = parseInt(document.getElementById('prod-cantidad').textContent);

    console.log('Cantidad enviada:', cantidad);

    fetch(form.action, { // Usar la acción del formulario como URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ cantidad: cantidad })
    })
    .then(response => response.json())
    .then(data => {
        const mensajeDiv = document.getElementById('mensaje');
        mensajeDiv.textContent = data.message;
        mensajeDiv.style.color = data.status === 'success' ? 'green' : 'red';
        alert(data.message);
        console.log(data);

        // Llamar a una función para actualizar el carrito si existe
        if (typeof verCarrito === 'function') {
            verCarrito();
        }
    })
    .catch(error => console.error('Error:', error));
});
