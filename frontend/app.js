console.log("EchoCrew Frontend initialized.");

fetch("http://localhost:8000/health")
  .then(res => res.json())
  .then(data => {
    const statusEl = document.getElementById("status");
    if (statusEl) {
      statusEl.textContent = `Backend Status: ${data.status.toUpperCase()} (${data.environment})`;
    }
  })
  .catch(err => {
    const statusEl = document.getElementById("status");
    if (statusEl) {
      statusEl.textContent = "Backend Offline / Disconnected";
      statusEl.style.backgroundColor = "#dc2626";
    }
  });
