const botonesEliminar = document.querySelectorAll('.boton-eliminar');
const csrfToken = document.getElementById("csrf-token").value;
console.log('se carga carrito');


botonesEliminar.forEach(boton => {
    boton.addEventListener('click', () => {
        const productId = boton.getAttribute('carr-prod-id');
        
        fetch(`/carrito/eliminar/${productId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            }
        })
        .then(response => response.json())
        .then(data => {
            const mensajeDiv = document.getElementById("mensaje");
            mensajeDiv.textContent = data.message;
            mensajeDiv.style.color = data.status === "success" ? "green" : "red";
            alert(data.message);
            console.log(data);

            // Actualiza el carrito después de eliminar
            verCarrito();
        })
        .catch(error => console.error("Error:", error));
    });
});
