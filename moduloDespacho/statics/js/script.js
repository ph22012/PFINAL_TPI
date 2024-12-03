document.addEventListener("DOMContentLoaded", () => {
    const tableRows = document.querySelectorAll("tbody tr");

    tableRows.forEach(row => {
        row.addEventListener("click", () => {
            const orderId = row.children[0].innerText; // Obtener el ID de la orden (primera columna)
            alert(`Seleccionaste la orden con ID: ${orderId}`);
        });
    });
});
