// ==========================================================================
// FUNCIONALIDAD DINÁMICA CON JAVASCRIPT - PROYECTO COCA-COLA
// ==========================================================================

// 1. Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    
    // VARIABLES Y SELECTORES
    const formulario = document.getElementById("formulario-sugerencias");
    const contenedorRegistros = document.getElementById("contenedor-registros");
    const contadorTotal = document.getElementById("contador-total");
    const mensajeAlerta = document.getElementById("mensaje-alerta");
    
    let totalElementos = 0;

    // 2. CAPTURAR EL EVENTO SUBMIT DEL FORMULARIO
    formulario.addEventListener("submit", (evento) => {
        // Evitar que la página se recargue por defecto
        evento.preventDefault();

        // Obtener los valores de los inputs
        const nombre = document.getElementById("nombre-item").value.trim();
        const categoria = document.getElementById("categoria-item").value;
        const descripcion = document.getElementById("descripcion-item").value.trim();

        // 3. VALIDACIÓN DE CAMPOS VACÍOS
        if (nombre === "" || categoria === "" || descripcion === "") {
            mostrarAlerta("¡Por favor, completa todos los campos del formulario!", "danger");
            return; // Detiene la ejecución si hay campos vacíos
        }

        // Si pasa la validación, mostrar mensaje de éxito
        mostrarAlerta("¡Registro agregado correctamente!", "success");

        // 4. CREACIÓN DINÁMICA DE ELEMENTOS HTML (createElement)
        // Crear columna contenedora de Bootstrap
        const columna = document.createElement("div");
        columna.className = "col-12 animate__animated animate__fadeIn";

        // Crear la tarjeta (Card)
        const tarjeta = document.createElement("div");
        tarjeta.className = "card p-3 border-start border-danger border-4 shadow-sm";

        // Cuerpo de la tarjeta
        const tarjetaContenido = document.createElement("div");
        tarjetaContenido.className = "card-body p-1";

        // Título (Nombre)
        const tituloCard = document.createElement("h5");
        tituloCard.className = "card-title text-danger fw-bold mb-1";
        tituloCard.textContent = nombre;

        // Subtítulo (Categoría)
        const subtituloCard = document.createElement("span");
        subtituloCard.className = "badge bg-secondary mb-2";
        subtituloCard.textContent = categoria;

        // Texto (Descripción)
        const textoCard = document.createElement("p");
        textoCard.className = "card-text text-muted small text-justify mb-3";
        textoCard.textContent = descripcion;

        // Botón de eliminar con evento de clic integrado
        const botonEliminar = document.createElement("button");
        botonEliminar.className = "btn btn-outline-dark btn-sm fw-bold";
        botonEliminar.textContent = "Eliminar Registro";

        // 5. EVENTO CLICK PARA ELIMINAR EL REGISTRO
        botonEliminar.addEventListener("click", () => {
            columna.remove(); // Remueve el elemento de la pantalla
            actualizarContador(-1); // Decrementa el contador global
        });

        // 6. ENSAMBLAR E INYECTAR ELEMENTOS EN LA PÁGINA (appendChild)
        tarjetaContenido.appendChild(tituloCard);
        tarjetaContenido.appendChild(subtituloCard);
        tarjetaContenido.appendChild(textoCard);
        tarjetaContenido.appendChild(botonEliminar);
        
        tarjeta.appendChild(tarjetaContenido);
        columna.appendChild(tarjeta);
        
        contenedorRegistros.appendChild(columna);

        // 7. ACTUALIZAR EL CONTADOR TOTAL
        actualizarContador(1);

        // Limpiar el formulario para un nuevo ingreso
        formulario.reset();
    });

    // FUNCIÓN PARA ACTUALIZAR EL CONTADOR EN PANTALLA
    function actualizarContador(valor) {
        totalElementos += valor;
        contadorTotal.textContent = totalElementos;
    }

    // FUNCIÓN PARA MOSTRAR MENSAJES DINÁMICOS DE VALIDACIÓN
    function mostrarAlerta(mensaje, tipo) {
        // Limpiar alertas previas
        mensajeAlerta.innerHTML = "";

        const alerta = document.createElement("div");
        alerta.className = `alert alert-${tipo} alert-dismissible fade show fw-semibold small py-2`;
        alerta.role = "alert";
        alerta.textContent = mensaje;

        mensajeAlerta.appendChild(alerta);

        // Auto-eliminar la alerta después de 3.5 segundos
        setTimeout(() => {
            alerta.remove();
        }, 3500);
    }
});