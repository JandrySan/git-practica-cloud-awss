const API_URL = window.API_URL || "";

async function leerRespuesta(response) {
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json();
  }

  const text = await response.text();

  if (contentType.includes("text/html") || text.trim().startsWith("<!DOCTYPE")) {
    return {
      detail: `El servidor respondio con estado ${response.status}, pero no devolvio JSON.`,
    };
  }

  return {
    detail: text || `El servidor respondio con estado ${response.status}`,
  };
}

async function enviarReserva() {
  const nombre = document.getElementById("nombre").value.trim();
  const fecha = document.getElementById("fecha").value.trim();
  const personas = document.getElementById("personas").value.trim();
  const telefono = document.getElementById("telefono").value.trim();
  const btn = document.getElementById("btnReserva");
  const msg = document.getElementById("mensajeRespuesta");

  if (!nombre || !fecha || !personas || !telefono) {
    msg.className = "msg error";
    msg.textContent = "Por favor completa todos los campos.";
    return;
  }

  btn.disabled = true;
  btn.textContent = "Enviando...";
  msg.className = "msg";
  msg.textContent = "";

  try {
    const response = await fetch(`${API_URL}/reserva`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, fecha, personas, telefono }),
    });

    const data = await leerRespuesta(response);

    if (!response.ok) {
      throw new Error(data.detail || data.mensaje || "Error del servidor");
    }

    msg.className = "msg success";
    msg.textContent = data.mensaje || "Reserva enviada correctamente.";

    document.getElementById("nombre").value = "";
    document.getElementById("fecha").value = "";
    document.getElementById("personas").value = "";
    document.getElementById("telefono").value = "";
  } catch (error) {
    msg.className = "msg error";
    msg.textContent = `No se pudo enviar la reserva: ${error.message}`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Solicitar reserva";
  }
}

window.enviarReserva = enviarReserva;
