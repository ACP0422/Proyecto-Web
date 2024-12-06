document.addEventListener('DOMContentLoaded', function () {
    filtrarProductos();
    document.querySelectorAll(".option").forEach(option => {
        option.addEventListener("change", filtrarProductos);
    });
});

function filtrarProductos() {
    let filtrosElegidos = {
        tipo_de_luz: [],
        tamaño: [],
        especie: []
    };

    document.querySelectorAll(".option").forEach(opcion => {
        const categoriaFiltro = opcion.name;
        const valorFiltro = opcion.value.toLowerCase();

        if (opcion.checked) {
            if (!filtrosElegidos[categoriaFiltro].includes(valorFiltro)) {
                filtrosElegidos[categoriaFiltro].push(valorFiltro);
            }
        } else {
            const index = filtrosElegidos[categoriaFiltro].indexOf(valorFiltro);
            if (index > -1) {
                filtrosElegidos[categoriaFiltro].splice(index, 1);
            }
        }
    });

    if (Object.values(filtrosElegidos).every(filtro => filtro.length === 0)) {
        filtrosElegidos = {}; 
    }

    fetch('filtrarProductos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: 'same-origin', 
        body: JSON.stringify(filtrosElegidos)
    })
    .then(response => response.json())
    .then(data => {
        actualizarProductos(data.productos); 
    })
    .catch(error => console.error('Error en la solicitud:', error));
}

function actualizarProductos(productos) {
    const contenedorProductos = document.querySelector(".productos");
    contenedorProductos.innerHTML = ""; 

    productos.forEach(producto => {
        const productoElemento = `
            <div class="producto">
                <a href="ficha?planta=${producto.nombre}">
                    <div class="image-wrapper">
                        <img src="${producto.imagen}" alt="${producto.nombre}">
                        <h4>${producto.nombre}</h4>
                        <p>${producto.descripcion}</p>
                    </div>
                </a>
            </div>
        `;
        contenedorProductos.innerHTML += productoElemento;
    });
}
