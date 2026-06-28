// script.js
// CSi - CoFre Sistemas Informáticos
// Funcionalidad dinámica: registro, validación, conteo y eliminación de solicitudes de servicio

document.addEventListener('DOMContentLoaded', function () {

  // Referencias a elementos del DOM
  const formSolicitud = document.getElementById('formSolicitud');
  const nombreCliente = document.getElementById('nombreCliente');
  const categoriaServicio = document.getElementById('categoriaServicio');
  const descripcionServicio = document.getElementById('descripcionServicio');
  const mensajeValidacion = document.getElementById('mensajeValidacion');
  const listaSolicitudes = document.getElementById('listaSolicitudes');
  const contadorSolicitudes = document.getElementById('contadorSolicitudes');

  // Contador de solicitudes registradas
  let totalSolicitudes = 0;

  // Función para mostrar mensajes de validación al usuario
  function mostrarMensaje(texto, tipo) {
    mensajeValidacion.textContent = texto;
    mensajeValidacion.classList.remove('d-none', 'alert-danger', 'alert-success');
    mensajeValidacion.classList.add(tipo === 'error' ? 'alert-danger' : 'alert-success');

    // El mensaje desaparece automáticamente después de unos segundos
    setTimeout(function () {
      mensajeValidacion.classList.add('d-none');
    }, 3000);
  }

  // Función para actualizar el contador de registros en pantalla
  function actualizarContador() {
    contadorSolicitudes.textContent = totalSolicitudes;
  }

  // Función para crear y agregar una nueva solicitud a la lista
  function crearSolicitud(nombre, categoria, descripcion) {

    // Elemento contenedor de la solicitud (li de Bootstrap)
    const item = document.createElement('li');
    item.className = 'list-group-item d-flex justify-content-between align-items-start flex-wrap';

    // Contenedor del texto de la solicitud
    const contenido = document.createElement('div');
    contenido.className = 'me-auto';

    const tituloNombre = document.createElement('strong');
    tituloNombre.textContent = nombre;

    const badgeCategoria = document.createElement('span');
    badgeCategoria.className = 'badge bg-secondary ms-2';
    badgeCategoria.textContent = categoria;

    const textoDescripcion = document.createElement('p');
    textoDescripcion.className = 'mb-0 text-muted';
    textoDescripcion.textContent = descripcion;

    contenido.appendChild(tituloNombre);
    contenido.appendChild(badgeCategoria);
    contenido.appendChild(textoDescripcion);

    // Botón para eliminar la solicitud
    const botonEliminar = document.createElement('button');
    botonEliminar.className = 'btn btn-outline-danger btn-sm';
    botonEliminar.textContent = 'Eliminar';

    // Evento click para eliminar el registro
    botonEliminar.addEventListener('click', function () {
      listaSolicitudes.removeChild(item);
      totalSolicitudes--;
      actualizarContador();
      mostrarMensaje('Solicitud eliminada correctamente.', 'success');
    });

    item.appendChild(contenido);
    item.appendChild(botonEliminar);

    // Agregar la nueva solicitud a la lista en pantalla
    listaSolicitudes.appendChild(item);

    totalSolicitudes++;
    actualizarContador();
  }

  // Captura del evento submit del formulario
  formSolicitud.addEventListener('submit', function (evento) {

    // Evita que la página se recargue
    evento.preventDefault();

    const nombre = nombreCliente.value.trim();
    const categoria = categoriaServicio.value;
    const descripcion = descripcionServicio.value.trim();

    // Validación de campos vacíos
    if (nombre === '' || categoria === '' || descripcion === '') {
      mostrarMensaje('Por favor complete todos los campos antes de registrar la solicitud.', 'error');
      return;
    }

    // Si la validación es correcta, se crea el registro
    crearSolicitud(nombre, categoria, descripcion);
    mostrarMensaje('Solicitud registrada exitosamente.', 'success');

    // Limpiar el formulario para un nuevo registro
    formSolicitud.reset();
    nombreCliente.focus();
  });

});
