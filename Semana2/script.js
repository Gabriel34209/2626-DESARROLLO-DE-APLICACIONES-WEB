// ==========================================================================
// VALIDACIONES EN TIEMPO REAL Y LOGICA MODULAR - PROYECTO COCA-COLA
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    // Selectores principales
    const formulario = document.getElementById("formulario-sugerencias");
    const inputNombre = document.getElementById("nombre-item");
    const selectCategoria = document.getElementById("categoria-item");
    const txtDescripcion = document.getElementById("descripcion-item");
    
    const contenedorRegistros = document.getElementById("contenedor-registros");
    const contadorTotal = document.getElementById("contador-total");
    const mensajeAlerta = document.getElementById("mensaje-alerta");

    let totalElementos = 0;

    // --- FUNCIONES DE VALIDACIÓN REUTILIZABLES ---

    function validarNombre() {
        const valor = inputNombre.value.trim();
        if (valor === "" || valor.length < 3) {
            marcarInvalido(inputNombre);
            return false;
        } else {
            marcarValido(inputNombre);
            return true;
        }
    }

    function validarCategoria() {
        const valor = selectCategoria.value;
        if (valor === "") {
            marcarInvalido(selectCategoria);
            return false;
        } else {
            marcarValido(selectCategoria);
            return true;
        }
    }

    function validarDescripcion() {
        const valor = txtDescripcion.value.trim();
        if (valor === "" || valor.length < 10) {
            marcarInvalido(txtDescripcion);
            return false;
        } else {
            marcarValido(txtDescripcion);
            return true;
        }
    }

    // Funciones auxiliares para aplicar clases Bootstrap
    function marcarInvalido(elemento) {
        elemento.classList.remove("is-valid");
        elemento.classList.add("is-invalid");
    }

    function marcarValido(elemento) {
        elemento.classList.remove("is-invalid");
        elemento.classList.add("is-valid");
    }

    function limpiarEstilosValidacion() {
        [inputNombre, selectCategoria, txtDescripcion].forEach(elemento => {
            elemento.classList.remove("is-valid", "is-invalid");
        });
    }

    // --- ASIGNACIÓN DE EVENTOS EN TIEMPO REAL (input y blur) ---

    inputNombre.addEventListener("input", validarNombre);
    inputNombre.addEventListener("blur", validarNombre);

    selectCategoria.addEventListener("change", validarCategoria);
    selectCategoria.addEventListener("blur", validarCategoria);

    txtDescripcion.addEventListener("input", validarDescripcion);
    txtDescripcion.addEventListener("blur", validarDescripcion);


    // --- MANEJO DEL EVENTO SUBMIT ---

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault(); // Evita la recarga de la página

        // Ejecutar todas las validaciones antes de registrar
        const esNombreValido = validarNombre();
        const esCategoriaValida = validarCategoria();
        const esDescripcionValida = validarDescripcion();

        // Permitir registro ÚNICAMENTE si todas las validaciones son correctas
        if (esNombreValido && esCategoriaValida && esDescripcionValida) {
            agregarRegistro(inputNombre.value.trim(), selectCategoria.value, txtDescripcion.value.trim());
            mostrarMensajeGlobal("¡Registro completado y guardado con éxito!", "alert-success");
            formulario.reset();
            limpiarEstilosValidacion();
        } else {
            mostrarMensajeGlobal("Por favor, corrige los errores en los campos resaltados.", "alert-danger");
        }
    });

    // --- CREACIÓN Y GESTIÓN DE REGISTROS DINÁMICOS ---

    function agregarRegistro(nombre, categoria, descripcion) {
        // Crear elementos dinámicos mediante createElement()
        const columna = document.createElement("div");
        columna.className = "col-12 animate__animated animate__fadeIn";

        const tarjeta = document.createElement("div");
        tarjeta.className = "card p-3 border-start border-danger border-4 shadow-sm";

        const cuerpoTarjeta = document.createElement("div");
        cuerpoTarjeta.className = "card-body p-1";

        const titulo = document.createElement("h5");
        titulo.className = "card-title text-danger fw-bold mb-1";
        titulo.textContent = nombre;

        // CORRECCIÓN AQUÍ: Se usa guion bajo (_) para evitar errores de sintaxis en JS
        const sub_etiqueta = document.createElement("span");
        sub_etiqueta.className = "badge bg-secondary mb-2";
        sub_etiqueta.textContent = categoria;

        const detalle = document.createElement("p");
        detalle.className = "card-text text-muted small text-justify mb-3";
        detalle.textContent = descripcion;

        const botonEliminar = document.createElement("button");
        botonEliminar.className = "btn btn-outline-dark btn-sm fw-bold";
        botonEliminar.textContent = "Eliminar";

        // Evento click independiente para eliminar registros
        botonEliminar.addEventListener("click", () => {
            columna.remove();
            actualizarContador(-1);
        });

        // Ensamblar la estructura utilizando appendChild()
        cuerpoTarjeta.appendChild(titulo);
        cuerpoTarjeta.appendChild(sub_etiqueta); // CORRECCIÓN AQUÍ
        cuerpoTarjeta.appendChild(detalle);
        cuerpoTarjeta.appendChild(botonEliminar);
        tarjeta.appendChild(cuerpoTarjeta);
        columna.appendChild(tarjeta);

        contenedorRegistros.appendChild(columna);
        actualizarContador(1);
    }

    function actualizarContador(valor) {
        totalElementos += valor;
        contadorTotal.textContent = totalElementos;
    }

    function mostrarMensajeGlobal(mensaje, claseBootstrap) {
        mensajeAlerta.innerHTML = "";
        const alerta = document.createElement("div");
        alerta.className = `alert ${claseBootstrap} alert-dismissible fade show fw-semibold small py-2 text-center`;
        alerta.role = "alert";
        alerta.textContent = mensaje;
        mensajeAlerta.appendChild(alerta);

        setTimeout(() => alerta.remove(), 4000);
    }
});