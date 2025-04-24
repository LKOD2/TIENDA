
// ------------------- carrusel -----------------------

let currentIndex = 0;
const intervalTime = 5000; // Tiempo en milisegundos (5000 ms = 5 segundos)

// Función para mover el slide manualmente
function moveSlide(direction) {
    const track = document.querySelector(".carousel-track");
    const items = document.querySelectorAll(".carousel-item");
    const totalItems = items.length;

    currentIndex = (currentIndex + direction + totalItems) % totalItems;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Función para mover el slide automáticamente
function autoSlide() {
    moveSlide(1);
}

// Temporizador para el cambio automático de imágenes
let slideInterval = setInterval(autoSlide, intervalTime);

// Pausar el carrusel cuando el usuario interactúa con los botones
document.querySelector(".carousel").addEventListener("mouseover", () => {
    clearInterval(slideInterval);
});

document.querySelector(".carousel").addEventListener("mouseleave", () => {
    slideInterval = setInterval(autoSlide, intervalTime);
});

// ------------------- MENU DESPLEGABLE -----------------------

function toggleMenu() {
    const sideMenu = document.getElementById('sideMenu');
    if (sideMenu.style.left === '0px') {
        sideMenu.style.left = '-250px';
    } else {
        sideMenu.style.left = '0px';
    }
}