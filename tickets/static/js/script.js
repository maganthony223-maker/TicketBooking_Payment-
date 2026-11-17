
const ticketPrices = { regular: 10000, VIP: 25000, premium: 50000 };

const ticketInput = document.getElementById("id_tickets");
const ticketType = document.getElementById("id_ticket_type");
const totalDisplay = document.getElementById("total");

function calculateTotal() {
    const numberOfTickets = parseInt(ticketInput.value) || 0;
    const pricePerTicket = ticketPrices[ticketType.value];
    totalDisplay.textContent = "UGX " + (numberOfTickets * pricePerTicket).toLocaleString();
}

ticketInput.addEventListener("input", calculateTotal);
ticketType.addEventListener("change", calculateTotal);
calculateTotal();
