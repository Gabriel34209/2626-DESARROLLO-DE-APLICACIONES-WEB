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

    // Elementos del Spinner y Botón
    const btnEnviar = document.getElementById("btn-enviar");
    const spinnerCarga = document.getElementById("spinner-carga");
    const textoBoton = document.getElementById("texto-boton");

    // Instancia del Modal de Bootstrap
    const modalConfirmacion = new bootstrap.Modal(document.getElementById('modalConfirmacion'));

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

    // --- ASIGNACIÓN DE EVENTOS EN TIEMPO REAL ---

    inputNombre.addEventListener("input", validarNombre);
    inputNombre.addEventListener("blur", validarNombre);

    selectCategoria.addEventListener("change", validarCategoria);
    selectCategoria.addEventListener("blur", validarCategoria);

    txtDescripcion.addEventListener("input", validarDescripcion);
    txtDescripcion.addEventListener("blur", validarDescripcion);


    // --- MANEJO DEL EVENTO SUBMIT ---

    formulario.addEventListener("submit", (evento) => {
        evento.preventDefault(); 

        const esNombreValido = validarNombre();
        const esCategoriaValida = validarCategoria();
        const esDescripcionValida = validarDescripcion();

        if (esNombreValido && esCategoriaValida && esDescripcionValida) {
            
            // 1. Activar Spinner Bootstrap y deshabilitar botón
            spinnerCarga.classList.remove("d-none");
            btnEnviar.disabled = true;
            textoBoton.textContent = " Procesando...";

            // Captura de datos antes del reset del formulario
            const nombreVal = inputNombre.value.trim();
            const categoriaVal = selectCategoria.value;
            const descripcionVal = txtDescripcion.value.trim();

            // 2. Simular un retraso de procesamiento en red (1.2 segundos)
            setTimeout(() => {
                // Agregar tarjeta dinámica
                agregarRegistro(nombreVal, categoriaVal, descripcionVal);
                
                // Mostrar alerta Bootstrap de éxito
                mostrarMensajeGlobal("¡Registro completado y guardado con éxito!", "alert-success");
                
                // Inyectar datos en el Modal y mostrarlo
                document.getElementById("modal-resumen-nombre").textContent = nombreVal;
                document.getElementById("modal-resumen-categoria").textContent = categoriaVal;
                document.getElementById("modal-resumen-descripcion").textContent = descripcionVal;
                modalConfirmacion.show();

                // Restaurar el botón y el formulario
                formulario.reset();
                limpiarEstilosValidacion();
                spinnerCarga.classList.add("d-none");
                btnEnviar.disabled = false;
                textoBoton.textContent = "Enviar y Registrar";

            }, 1200);

        } else {
            mostrarMensajeGlobal("Por favor, corrige los errores en los campos resaltados.", "alert-danger");
        }
    });

    // --- CREACIÓN Y GESTIÓN DE REGISTROS DINÁMICOS ---

    function agregarRegistro(nombre, categoria, descripcion) {
        const columna = document.createElement("div");
        columna.className = "col-12 opacity-100"; // Asegura visibilidad sin dependencias externas

        const tarjeta = document.createElement("div");
        tarjeta.className = "card p-3 border-start border-danger border-4 shadow-sm";

        const cuerpoTarjeta = document.createElement("div");
        cuerpoTarjeta.className = "card-body p-1";

        const titulo = document.createElement("h5");
        titulo.className = "card-title text-danger fw-bold mb-1";
        titulo.textContent = nombre;

        const sub_etiqueta = document.createElement("span");
        sub_etiqueta.className = "badge bg-secondary mb-2";
        sub_etiqueta.textContent = categoria;

        const detalle = document.createElement("p");
        detalle.className = "card-text text-muted small text-justify mb-3";
        detalle.textContent = descripcion;

        const botonEliminar = document.createElement("button");
        botonEliminar.className = "btn btn-outline-dark btn-sm fw-bold";
        botonEliminar.textContent = "Eliminar";

        botonEliminar.addEventListener("click", () => {
            columna.remove();
            actualizarContador(-1);
        });

        cuerpoTarjeta.appendChild(titulo);
        cuerpoTarjeta.appendChild(sub_etiqueta); 
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