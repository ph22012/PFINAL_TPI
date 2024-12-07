document.addEventListener('DOMContentLoaded', function() {
    // Cerrar sesión
    

    // Modal de Agregar Productos
    var agregarModal = document.getElementById('agregarModal');
    var openAgregarModal = document.getElementById('openAgregarModal');
    var closeAgregarModal = document.getElementById('closeAgregarModal');
    var buscarProducto = document.getElementById('buscarProducto');
    var agregarAlCatalogo = document.getElementById('agregarAlCatalogo');
    var cerrarModal = document.getElementById('cerrarModal');
    var tablaProductos = document.getElementById('tablaProductos');
    var idProductoInput = document.getElementById('id_producto');

    // Modal de Eliminar Productos
    var eliminarModal = document.getElementById('eliminarModal');
    var openEliminarModal = document.getElementById('openEliminarModal');
    var closeEliminarModal = document.getElementById('closeEliminarModal');
    var eliminarProducto = document.getElementById('eliminarProducto');
    var cerrarEliminarModal = document.getElementById('cerrarEliminarModal');
    var idProductoEliminarInput = document.getElementById('id_producto_eliminar');

    // Abrir Modal de Agregar Productos
    openAgregarModal.onclick = function() {
        agregarModal.style.display = "block";
    }

    // Cerrar Modal de Agregar Productos
    closeAgregarModal.onclick = function() {
        agregarModal.style.display = "none";
    }

    // Cerrar Modal de Agregar Productos con "Salir"
    cerrarModal.onclick = function() {
        agregarModal.style.display = "none";
    }

    // Función para buscar el producto por ID
    buscarProducto.onclick = function() {
        var idProducto = idProductoInput.value.trim();
        if (idProducto) {
            // Aquí va la lógica para buscar el producto, por ejemplo, una petición AJAX al servidor
            // Simulación de producto encontrado:
            var tr = document.createElement('tr');
            tr.innerHTML = `<td>${idProducto}</td><td>Producto ${idProducto}</td><td><input type="number" value="1" min="1" class="cantidad"></td>`;
            tablaProductos.querySelector('tbody').appendChild(tr);
            idProductoInput.value = '';  // Limpiar el campo de búsqueda
        } else {
            alert("Por favor ingresa un ID de producto.");
        }
    }

    // Agregar el producto al catálogo
    agregarAlCatalogo.onclick = function() {
        var productos = [];
        var rows = tablaProductos.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            var idProducto = row.cells[0].textContent;
            var cantidad = row.querySelector('.cantidad').value;
            productos.push({ idProducto, cantidad });
        });

        if (productos.length > 0) {
            // Lógica para agregar productos al catálogo (puede ser una solicitud AJAX)
            console.log("Productos a agregar al catálogo:", productos);
            alert('Productos agregados al catálogo');
            agregarModal.style.display = "none";  // Cerrar el modal
        } else {
            alert("No hay productos seleccionados para agregar.");
        }
    }

    // Abrir Modal de Eliminar Productos
    openEliminarModal.onclick = function() {
        eliminarModal.style.display = "block";
    }

    // Cerrar Modal de Eliminar Productos
    closeEliminarModal.onclick = function() {
        eliminarModal.style.display = "none";
    }

    // Cerrar Modal de Eliminar Productos con "Salir"
    cerrarEliminarModal.onclick = function() {
        eliminarModal.style.display = "none";
    }

    // Eliminar el producto
    eliminarProducto.onclick = function() {
        var idProductoEliminar = idProductoEliminarInput.value.trim();
        if (idProductoEliminar) {
            // Lógica para eliminar el producto por ID, por ejemplo, una petición AJAX
            console.log("Producto a eliminar con ID:", idProductoEliminar);
            alert('Producto con ID ' + idProductoEliminar + ' eliminado');
            eliminarModal.style.display = "none";  // Cerrar el modal
            idProductoEliminarInput.value = '';  // Limpiar el campo de ID para eliminar
        } else {
            alert("Por favor ingresa un ID de producto para eliminar.");
        }
    }

    // Cerrar ambos modales si se hace clic fuera de ellos
    window.onclick = function(event) {
        if (event.target === agregarModal) {
            agregarModal.style.display = "none";
        }
        if (event.target === eliminarModal) {
            eliminarModal.style.display = "none";
        }
    }
});
