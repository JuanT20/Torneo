document.addEventListener("DOMContentLoaded", () => {
  const formArbitro = document.getElementById("formArbitros");

  formArbitro.addEventListener("submit", function (event) {
    event.preventDefault();

    const idTorneo = formArbitro.getAttribute("data-id");
    const identificacion = document.querySelector("#id_arbitro").value;
    const nombre = document.querySelector("#nombre").value;
    const experiencia = document.querySelector("#experiencia").value;

    // Validación más detallada
    if (!identificacion.trim() || !nombre.trim() || !experiencia.trim()) {
      swal("Error", "Todos los campos son obligatorios", "error");
      return;
    }

    const datosArbitro = {
      identificacion: identificacion,
      nombre: nombre,
      experiencia: experiencia,
      id_torneo: idTorneo,
    };

    fetch(`/arbitro/${idTorneo}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest", // Para identificar solicitudes AJAX
      },
      body: JSON.stringify(datosArbitro),
    })
      .then((response) => {
        // Verificar el estado de la respuesta
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          swal("Exitoso!", "¡Registro del árbitro exitoso!", "success");
          formArbitro.reset();
        } else {
          alert("Ocurrió un error al registrar el arbitro.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Ocurrió un error al enviar los datos.");
      });
  });
});
