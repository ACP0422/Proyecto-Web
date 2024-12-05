document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".option").forEach(option => {
        option.addEventListener("change", filtrarProductos);
    });
});

function filtrarProductos() {
    const filtrosElegidos = {
        tipo_de_luz: [],
        tamaño: [],
        especie: []
    };

    document.querySelectorAll(".option").forEach(opcion => {
        if (opcion.checked) {
            const categoriaFiltro = opcion.name;
            const valorFiltro = opcion.value.toLowerCase();

            filtrosElegidos[categoriaFiltro].push(valorFiltro);
        }
    });

    fetch("filtrarProductos/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify(filtrosElegidos)
    })
    .then(response => response.json())
    .then(data => {
        actualizarProductos(data.productos);
    })
    .catch(error => console.error('Error:', error));
}

function actualizarProductos(productos) {
    const contenedorProductos = document.querySelector(".productos");
    contenedorProductos.innerHTML = ""; // Limpiar los productos actuales

    productos.forEach(producto => {
        const productoElemento = `
            <div class="producto">
                <a href="/ficha/${producto.id}">
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
