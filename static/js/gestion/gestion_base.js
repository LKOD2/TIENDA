

//-------------------------------- LOGOUT ---------------------------------------


document.addEventListener('DOMContentLoaded', ()=>{
    const botonLogout = document.getElementById('menu-user');
    botonLogout.addEventListener('change', ()=>{
    
        if (botonLogout.value == 'logout'){

        
            fetch('/logout')
            .then(respuesta => respuesta.json())
            .then(data => {
                if(data.estado){
                    alert(data.mensaje);
                    window.location.href = '/login'
                }else{
                    alert(data.mensaje);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }

    })

})



//-------------------------------- MENU ---------------------------------------



// Manejo del click en los items del menú
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', () => {
        const id = item.getAttribute('id'); 
        localStorage.setItem('select_menu', id);
        
        document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('activo'));
        item.classList.add('activo');
    });
});

// Al cargar el documento, aplica la clase 'activo' al item seleccionado
document.addEventListener('DOMContentLoaded', () => {
    const selectedMenuId = localStorage.getItem('select_menu');
    if (selectedMenuId) {
        const selectItem = document.getElementById(selectedMenuId);
        if (selectItem) {
            selectItem.classList.add('activo');
        }
    }
});



//----------------------------- botones laterales--------------------

document.getElementById('boton-menu-cerrar').addEventListener('click', function() {
    document.querySelector('.gral').classList.toggle('menu-hidden');
    console.log('cerrar');
    
});
document.getElementById('boton-menu-abrir').addEventListener('click', function() {
    document.querySelector('.gral').classList.toggle('menu-hidden');
});

document.getElementById('boton-dis-cerrar').addEventListener('click', function() {
    document.querySelector('.gral').classList.toggle('dis-hidden');
});
document.getElementById('boton-dis-abrir').addEventListener('click', function() {
    document.querySelector('.gral').classList.toggle('dis-hidden');
});



