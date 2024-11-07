function toggleDetalles() {
    const detallesDiv = document.querySelector('.detalles');
    detallesDiv.classList.toggle('show');
}

let currentIndex = 0;

function moveCarousel(direction) {
    const carousel = document.getElementById('carousel');
    const totalItems = carousel.children.length;
    const itemWidth = carousel.children[0].offsetWidth; // Ancho de cada imagen

    // Ajusta el índice
    currentIndex += direction;

    // Controla los límites del carrusel
    if (currentIndex < 0) {
        currentIndex = totalItems - 1; // Va al último elemento si es menor que 0
    } else if (currentIndex >= totalItems) {
        currentIndex = 0; // Vuelve al primer elemento si es mayor que el último
    }

    // Mueve el carrusel usando transform
    const offset = -currentIndex * itemWidth;
    carousel.style.transform = `translateX(${offset}px)`;
}

// Datos de las plantas
const plantasData = {
    monstera: {
        nombre: "Monstera Deliciosa",
        nombreCientifico: "(Costilla de Adán)",
        descripcion: "La Monstera Deliciosa es una planta de interior popular, conocida por sus grandes hojas verdes con cortes distintivos...",
        detalles: {
            familia: "Araceae / Monstera",
            luz: "Luz indirecta brillante, tolera semisombra.",
            tamano: "Hasta 3 metros",
            riego: "Moderado.",
            clima: "Temperatura: 18-27°C | No tolera heladas.",
            uso: "Ideal para interiores.",
            cuidados: "Limpia sus hojas con un paño húmedo."
        },
        imagenPrincipal: "plant.png",
        imagenesRelacionadas: ["plant.png", "plant.png"]
    },
    loto: {
        nombre: "Flor de Loto",
        nombreCientifico: "(Nelumbo Nucifera)",
        descripcion: "La Flor de Loto es una planta acuática con flores grandes y hermosas que crecen en estanques y aguas tranquilas...",
        detalles: {
            familia: "Nelumbonaceae / Nelumbo",
            luz: "Luz directa.",
            tamano: "Hasta 1.5 metros.",
            riego: "Abundante.",
            clima: "Temperatura: 20-30°C.",
            uso: "Ideal para estanques.",
            cuidados: "Requiere un lugar soleado."
        },
        imagenPrincipal: "plant.png",
        imagenesRelacionadas: ["plant.png", "plant.png"]
    }
};

// Función para obtener el parámetro de la URL
function obtenerParametroUrl(nombre) {
    const params = new URLSearchParams(window.location.search);
    return params.get(nombre);
}

// Función para cargar los datos de la planta según el parámetro de la URL
function cargarPlanta() {
    const plantaId = obtenerParametroUrl('planta'); // lee el parámetro 'planta' de la URL
    if (!plantaId || !plantasData[plantaId]) {
        // Si no se pasa un parámetro válido, podemos cargar una planta por defecto o mostrar un error
        alert('Planta no encontrada');
        return;
    }

    const planta = plantasData[plantaId];

    // Crear la plantilla HTML y sustituir los valores dinámicos
    const fichaPlantaHTML = `
        <div class="descripcion-planta">
            <h1>${planta.nombre} <br> ${planta.nombreCientifico}</h1>
            <p>${planta.descripcion}</p>
            <div class="detalles">
                <h3>
                    Más detalles
                    <button class="flecha" onclick="toggleDetalles()">&#10094;</button>
                </h3>
                <ul id="detalles-content">
                    <li><span>Familia y Especie</span> ${planta.detalles.familia}</li>
                    <li><span>Tipo de luz</span> ${planta.detalles.luz}</li>
                    <li><span>Tamaño</span> ${planta.detalles.tamano}</li>
                    <li><span>Riego</span> ${planta.detalles.riego}</li>
                    <li><span>Clima ideal</span> ${planta.detalles.clima}</li>
                    <li><span>Uso</span> ${planta.detalles.uso}</li>
                    <li><span>Cuidados especiales</span> ${planta.detalles.cuidados}</li>
                </ul>
            </div>
            <a href="#" class="btn">Adoptar</a>
        </div>

        <div class="imagen-planta-contenedor">
            <img src="${planta.imagenPrincipal}" class="imagen-principal">
            <div class="imagenes-relacionadas">
                ${planta.imagenesRelacionadas.map(imagen => `<img src="${imagen}" class="imagen-pequena">`).join('')}
            </div>
        </div>
    `;

    // Insertar la plantilla HTML en el contenedor de la planta
    document.getElementById('ficha-planta').innerHTML = fichaPlantaHTML;
}

// Llamar a la función cargarPlanta cuando se cargue la página
window.onload = cargarPlanta;
