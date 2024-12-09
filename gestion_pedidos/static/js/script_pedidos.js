const socket = new WebSocket("ws://localhost:8000/ws/orders/"); // Conexión al websocket

//Manejo de información del pedido
function newOrder(order){
    const tableBody = document.querySelector("#pedidos tbody");
    const newRow = document.createElement("tr");
    newRow.setAttribute('id', `orden-${order.id_order}`);
    newRow.innerHTML = `
    <td>${order.id_order}</td>
    <td>${order.id_status.status}</td>
    <td>${order.order_date}</td>    
    <td>${order.id_address}</td>
    <td>${order.last_update}</td>
    <td>
        <a href="{% url 'order_detail' order_id=order.id_order %}">
            <button type="submit" class="btn btn-primary w-100">Ver pedido</button>
        </a>
    </td>
    <td>
        <a href="{% url 'edit_order' id_order=order.id_order %}">
            <button type="submit" class="btn btn-primary w-100">Editar pedido</button>
        </a>
    </td>
    `;
    tableBody.appendChild(newRow);
}

function updateOrder(order){
    const tableBody = document.querySelector("#pedidos tbody");
    const row = tableBody.querySelector(`#orden-${order.id_order}`);
    row.innerHTML = `
    <td>${order.id_order}</td>
    <td>${order.id_status.status}</td>
    <td>${order.order_date}</td>    
    <td>${order.id_address}</td>
    <td>${order.last_update}</td>
    <td>
        <a href="{% url 'edit_order' id_order=order.id_order %}">
            <button type="submit" class="btn btn-primary w-100">Ver pedido</button>
        </a>
    </td>
    <td>
        <a href="{% url 'order_detail' order_id=order.id_order %}">
            <button type="submit" class="btn btn-primary w-100">Editar pedido</button>
        </a>
    </td>
    `;
    tableBody.replaceChild(row, row);

    alert("Pedido actualizado: " +order.id_order);
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
    switch(tipo){
        case "NuevaOrden":
            newOrder(order);
            break;
        case "updateOrder":
            updateOrder(order);
            break;
    }
    
}