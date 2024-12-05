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




// Función para obtener el parámetro de la URL
function obtenerParametroUrl(nombre) {
    const params = new URLSearchParams(window.location.search);
    return params.get(nombre);
}

// Función para cargar los datos de la planta desde el servidor
async function cargarPlanta() {
    const plantaId = obtenerParametroUrl('planta'); // Lee el parámetro 'planta' de la URL
    if (!plantaId) {
        alert('Planta no especificada');
        return;
    }

    try {
        // Realiza la petición al servidor
        const response = await fetch(`/ficha/obtener-planta/?planta=${plantaId}`);
        if (!response.ok) {
            throw new Error('Error al obtener los datos de la planta');
        }

        const planta = await response.json();
        if (planta.error) {
            alert(planta.error);
            return;
        }

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
                <button><a href="#">Adoptar</a></button>
            </div>

            <div class="imagen-planta-contenedor">
                <img src="${planta.imagenPrincipal}" class="imagen-principal">
                <div class="imagenes-relacionadas">
                    ${planta.imagenesRelacionadas.map(imagen => `<img src="${imagen}" class="imagen-pequena">`).join('')}
                </div>
                <!-- Download Button -->
                <a href="/descargar_qr/${planta.id}/" class="boton-descargar-qr">
                    <button>Descargar QR</button>
                </a>
            </div>
        `;

        // Insertar la plantilla HTML en el contenedor de la planta
        document.getElementById('ficha-planta').innerHTML = fichaPlantaHTML;

    } catch (error) {
        alert('Ocurrió un error al cargar los datos de la planta.');
        console.error(error);
    }
}

// Llamar a la función cargarPlanta cuando se cargue la página
window.onload = cargarPlanta;
