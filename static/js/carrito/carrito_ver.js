    


// ------------------- VER CARRITO -----------------------

const CarritoBtn = document.querySelector('.carrito-boton');
const carrito = document.querySelector('.carrito');

CarritoBtn.addEventListener('click', () => {
    
    verCarrito();
});

const botonCarritoCerrar = document.querySelector('.boton-cerrar');

botonCarritoCerrar.addEventListener('click', ()=>{

    carrito.classList.toggle('activo');
})


function verCarrito() {

    const carrito = document.querySelector('.carrito');
    carrito.classList.add('activo');

    fetch('/carrito/ver/', {
        method: "GET",
        headers: {
            "Content-Type": "text/html",
        }
    })
    .then(response => {
        if (!response.ok) {
            console.log(response);
            
            throw new Error("No se pudo cargar el carrito");
        }
        return response.text();  // Obtener el HTML como texto
    })
    .then(html => {
        const carritoProductos = document.getElementById('carrito-contenido');
        carritoProductos.innerHTML = html; 
        elimiarCarrito();
        actualizarCarrito();
    })
    .catch(error => console.error("Error:", error));
}


function elimiarCarrito() {
    const botonesEliminar = document.querySelectorAll('.carr-boton-eliminar');
    const csrfToken = document.getElementById("csrf-token").value;

    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', () => {
            const productId = boton.getAttribute('carr-prod-id');

            console.log('se carga carrito', productId);
            
            fetch(`/carrito/eliminar/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                console.log(data);

                // Actualiza el carrito después de eliminar
                verCarrito();
            })
            .catch(error => console.error("Error:", error));
        });
    });

}


function actualizarCarrito() {
    document.querySelectorAll('.carr.boton-cantidad').forEach(boton => {
        boton.addEventListener('click', () => {
            const action = boton.getAttribute('action');

            // Encuentra el elemento cantidad relativo al botón presionado
            const cantidadEl = boton.parentElement.querySelector('.cantidad');
            const productoId = cantidadEl.getAttribute('carr-prod-id');
            let cantidadActual = parseInt(cantidadEl.textContent);

            // Determina la nueva cantidad
            let nuevaCantidad = action === "sumar" ? cantidadActual + 1 : cantidadActual - 1;

            if (nuevaCantidad < 1) {
                alert("La cantidad no puede ser menor a 1.");
                return;
            }

            console.log('Producto ID:', productoId, 'Nueva cantidad:', nuevaCantidad);

            // Actualizar la cantidad en el DOM inmediatamente
            cantidadEl.textContent = nuevaCantidad;

            // Enviar solicitud para actualizar la cantidad
            fetch(`/carrito/actualizar/${productoId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.getElementById("csrf-token").value
                },
                body: JSON.stringify({ cantidad: nuevaCantidad })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    cantidadEl.textContent = nuevaCantidad; // Actualiza la cantidad en el frontend
                    document.querySelector('.subtotal .monto').textContent = `$${data.total}`; // Actualiza el total
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
}
