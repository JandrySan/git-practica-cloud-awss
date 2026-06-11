// ⚠️ IMPORTANTE: Cuando tengas la URL de AWS, reemplaza este valor
// Por ahora apunta al backend local para pruebas
const API_URL = "http://Restaurante-v2-env.eba-yimwd639.us-east-2.elasticbeanstalk.com";

async function enviarReserva() {
  const nombre   = document.getElementById("nombre").value.trim();
  const fecha    = document.getElementById("fecha").value.trim();
  const personas = document.getElementById("personas").value.trim();
  const telefono = document.getElementById("telefono").value.trim();
  const btn      = document.getElementById("btnReserva");
  const msg      = document.getElementById("mensajeRespuesta");

  // Validación básica
  if (!nombre || !fecha || !personas || !telefono) {
    msg.className = "msg error";
    msg.textContent = "⚠️ Por favor completa todos los campos.";
    return;
  }

  // Deshabilitar botón mientras espera respuesta
  btn.disabled = true;
  btn.textContent = "Enviando...";
  msg.className = "msg";

  try {
    const response = await fetch(`${API_URL}/reserva`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, fecha, personas, telefono })
    });

    const data = await response.json();

    if (response.ok) {
      msg.className = "msg success";
      msg.textContent = `✅ ${data.mensaje}`;
      // Limpiar formulario tras éxito
      document.getElementById("nombre").value   = "";
      document.getElementById("fecha").value    = "";
      document.getElementById("personas").value = "";
      document.getElementById("telefono").value = "";
    } else {
      throw new Error(data.detail || "Error del servidor");
    }

  } catch (error) {
    msg.className = "msg error";
    msg.textContent = `❌ No se pudo enviar la reserva: ${error.message}`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Solicitar reserva →";
  }
}
