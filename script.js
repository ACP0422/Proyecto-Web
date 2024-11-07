document.addEventListener('DOMContentLoaded', function() {
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

            if (categoriaFiltro === "tipo_de_luz") {
                filtrosElegidos.tipo_de_luz.push(valorFiltro);
            } else if (categoriaFiltro === "tamaño") {
                filtrosElegidos.tamaño.push(valorFiltro);
            } else if (categoriaFiltro === "especie") {
                filtrosElegidos.especie.push(valorFiltro);
            }
        }
    });

    const sinFiltrosElegidos = filtrosElegidos.tipo_de_luz.length === 0 && 
                              filtrosElegidos.tamaño.length === 0 && 
                              filtrosElegidos.especie.length === 0;

    document.querySelectorAll(".producto").forEach(product => {
        if (sinFiltrosElegidos) {
            product.style.display = "block";
            return;
        }

        const productoTipoDeLuz = product.querySelector('input[name="tipo_de_luz"]')?.value.toLowerCase();
        const productoTamaño = product.querySelector('input[name="tamaño"]')?.value.toLowerCase();
        const productoEspecie = product.querySelector('input[name="especie"]')?.value.toLowerCase();

        const coincideTipoDeLuz = filtrosElegidos.tipo_de_luz.includes(productoTipoDeLuz);
        const coincideTamaño = filtrosElegidos.tamaño.includes(productoTamaño);
        const coincideEspecie = filtrosElegidos.especie.includes(productoEspecie);

        product.style.display = (coincideTipoDeLuz || coincideTamaño || coincideEspecie) ? "block" : "none";
    });
}
