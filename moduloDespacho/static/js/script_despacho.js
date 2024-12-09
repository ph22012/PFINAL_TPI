document.addEventListener("DOMContentLoaded", () => {
    const tableRows = document.querySelectorAll("tbody tr");

    tableRows.forEach(row => {
        row.addEventListener("click", () => {
            const orderId = row.children[0].innerText; // Obtener el ID de la orden (primera columna)
            alert(`Seleccionaste la orden con ID: ${orderId}`);
        });
    });
});

//Conexion al websocket
const socket = new WebSocket("ws://localhost:8000/ws/orders/");
//funciones:

//funcion para cuando se recibe un nuevo pedido
function newOrder(order){
    const tableBody = document.querySelector("#ordenes-pendientes tbody");
    const newRow = document.createElement("tr");
    newRow.setAttribute('id', `orden-pendiente-${order.id_order}`);
    newRow.innerHTML = `
    <td>${order.id_order}</td>
    <td>${order.id_cart}</td>
    <td>${order.id_address}</td>
        <td>${order.id_cupon}</td>
        <td>${order.id_employee}</td>
        <td>${order.id_status.status}</td>
        <td>${order.order_date}</td>    
        <td><button type="button" class="btn btn-warning btn-sm" id="btn-procesar">Marcar como "En proceso"</button></td>
    `;
    tableBody.appendChild(newRow);
}

//funcion para cuando se actualiza el estado de un pedido
function updateOrder(order){
    if (order.id_status.id_status == 2){
    const tableBody = document.querySelector("#ordenes-enProceso tbody");
    const newRow = document.createElement("tr");
    newRow.setAttribute('id', `orden-enProceso-${order.id_order}`);
    
    newRow.innerHTML = `
        <td>${order.id_order}</td>
        <td>${order.id_cart}</td>
        <td>${ order.id_address.address},
            ${ order.id_address.distrito },
            ${ order.id_address.municipio },
            ${ order.id_address.departamento}</td>
        <td>${order.id_cupon}</td>
        <td>${order.id_employee}</td>
        <td>${order.id_status.status}</td>
        <td>${order.order_date}</td>
        <td><button type="button" class="btn btn-success btn-sm" id="btn-listar">Marcar como "Lista"</button></td>
     `;
    tableBody.appendChild(newRow); 
    }
}

//logica para cuando se marca una orden como "En proceso"
document.querySelector("#contenedor-principal").addEventListener("click", function(event){
    if(event.target && event.target.id === "btn-procesar"){
        const button = event.target;
        const row =  button.closest("tr");
        console.log(row);
        const idOrden = row.id.split("-")[2];
        socket.send(JSON.stringify({
            'type': "procesarOrden",
            'idOrden': idOrden,
            'status': 2
        }))
        console.log("enviado el id:",idOrden);
        limpiarOrden(idOrden, "#ordenes-pendientes");
    }
});
//logica para cuando se marca una orden como "Lista"
document.querySelector("#contenedor-principal").addEventListener("click", function(event){
    if(event.target && event.target.id === "btn-lista"){
        const button = event.target;
        const row =  button.closest("tr");
        console.log(row);
        const idOrden = row.id.split("-")[2];
        socket.send(JSON.stringify({
            'type': "procesarOrden",
            'idOrden': idOrden,
            'status': 3
        }))
        console.log("enviado el id:",idOrden);
        limpiarOrden(idOrden, "#ordenes-enProceso");
    }
});
        

function limpiarOrden(idOrder, tabla){
    const tableBody = document.querySelector(tabla + " tbody");
    switch(tabla){
        case "#ordenes-pendientes":
            var row = tableBody.querySelector(`#orden-pendiente-${idOrder}`);
            tableBody.removeChild(row);
            break;
        case "#ordenes-enProceso":
            var row = tableBody.querySelector(`#orden-enProceso-${idOrder}`);
            tableBody.removeChild(row);
            break;
    }
    
    
}

function obtenerDatosOrden(idOrden){
    fetch('../get_datos_ordenes/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Incluir token CSRF para proteger la solicitud
        },
        body: JSON.stringify(idOrden),
    })
    .then(response => response.json())
    
}
    //funcionalidad del websocket

socket.onopen = () => {
    console.log("Conectado");
}

socket.onerror = (error) => {
    console.log(error);
}

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const order = data.order;
    const tipo = data.type;

    console.log(tipo);
    console.log(order);
    
    switch(tipo){
        case "NuevaOrden":
            newOrder(order);
            break;
        case "updateOrderStatus":
            updateOrder(order);
            break;
    }
    
}
