const socket = new WebSocket("ws://localhost:8000/ws/orders/");

function newOrder(order){
    const tableBody = document.querySelector("#pedidos-asignados tbody");
    const newRow = document.createElement("tr");
    newRow.setAttribute('id', `orden-asignada-${order.id_order}`);
    newRow.innerHTML = `
    <td>${order.id_order}</td>
    <td>${order.id_cart.customer.firstName }{ order.id_cart.customer_id.lastName }</td>
    <td>${order.id_address.address}</td>
    <td>${order.id_address.Distrito.id_municipio.id_departamento.name}</td>
    <td>${order.id_address.Distrito.id_municipio.name}</td>
    <td>${order.id_address.Distrito.name}</td>
    <td>${order.total}</td>    
    <td>
        <a href="{% url 'repartidores:entregar' item.pedido.id_order %}" class="btn btn-success btn-sm">Marcar como Entregado</a>
        <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal" data-bs-target="#detallePedido{{ item.pedido.id }}">Ver Detalles</button>
    </td>
    `;
    tableBody.appendChild(newRow);
}

socket.onopen= () => {
    console.log("Conectado repartidor");
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
        case "updateOrderStatus":
            updateOrder(order);
            break;
    }
}