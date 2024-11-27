function toggleDetalles() {
    const detallesDiv = document.querySelector('.detalles');
    detallesDiv.classList.toggle('show');
}


let currentIndex = 0; // Empieza en el primer grupo visible
let itemWidth; // Ancho de un elemento
let visibleItems = 3; // Cantidad de imágenes visibles a la vez
let autoCarouselInterval;

function setupCarousel() {
    const carousel = document.getElementById('carousel');
    const items = Array.from(carousel.children);

    // Clona las primeras y últimas imágenes visibles
    for (let i = 0; i < visibleItems; i++) {
        const firstClone = items[i].cloneNode(true);
        const lastClone = items[items.length - 1 - i].cloneNode(true);

        carousel.appendChild(firstClone);
        carousel.insertBefore(lastClone, carousel.firstChild);
    }
}

function initializeCarousel() {
    const carousel = document.getElementById('carousel');
    const items = Array.from(carousel.children);
    itemWidth = carousel.children[0].offsetWidth + parseFloat(getComputedStyle(carousel).gap);

    // Ajusta el carrusel para mostrar el primer grupo real
    carousel.style.transform = `translateX(${-itemWidth * visibleItems}px)`;
    currentIndex = visibleItems; // Primer elemento real después de los clones
}

function moveCarousel(direction) {
    const carousel = document.getElementById('carousel');
    const items = Array.from(carousel.children);
    const totalItems = items.length;

    // Ajusta el índice según la dirección
    currentIndex += direction;

    // Movimiento del carrusel
    const offset = -currentIndex * itemWidth;
    carousel.style.transition = 'transform 0.5s ease';
    carousel.style.transform = `translateX(${offset}px)`;

    // Ajusta el índice para mantener el efecto circular
    setTimeout(() => {
        if (currentIndex < visibleItems) {
            currentIndex = totalItems - 2 * visibleItems; // Salta al final real
            carousel.style.transition = 'none';
            carousel.style.transform = `translateX(${-currentIndex * itemWidth}px)`;
        } else if (currentIndex >= totalItems - visibleItems) {
            currentIndex = visibleItems; // Salta al inicio real
            carousel.style.transition = 'none';
            carousel.style.transform = `translateX(${-currentIndex * itemWidth}px)`;
        }
    }, 500); // Tiempo coincide con la duración de la transición
}

function startAutoCarousel() {
    autoCarouselInterval = setInterval(() => {
        moveCarousel(1); // Mueve hacia la derecha automáticamente
    }, 2000);
}

function stopAutoCarousel() {
    clearInterval(autoCarouselInterval);
}

window.addEventListener('load', () => {
    setupCarousel(); // Configura los clones
    initializeCarousel(); // Ajusta el carrusel al primer grupo real
    startAutoCarousel(); // Inicia el movimiento automático
});




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
        imagenPrincipal: "recursos/plant.png",
        imagenesRelacionadas: ["recursos/plant.png", "recursos/plant.png"]
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
        imagenPrincipal: "recursos/plant.png",
        imagenesRelacionadas: ["recursos/plant.png", "recursos/plant.png"]
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
                    <button class="flecha" onclick="toggleDetalles(this)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down">
                                <path d="m6 9 6 6 6-6"/>
                            </svg>
                        </button>
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
