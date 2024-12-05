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
    console.log(tableBody);
    const newRow = document.createElement("tr");
    newRow.setAttribute('id', `orden-enProceso-${order.id_order}`);
    newRow.innerHTML = `
        <td>${order.id_order}</td>
        <td>${order.id_cart}</td>
        <td>${order.id_address}</td>
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
        }))
        console.log("enviado el id:",idOrden);
        limpiarOrden(idOrden, "#ordenes-pendientes");
    }
});
        

function limpiarOrden(idOrder, tabla){
    const tableBody = document.querySelector(tabla + " tbody");
    const row = tableBody.querySelector(`#orden-pendiente-${idOrder}`);
    tableBody.removeChild(row);
    
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
