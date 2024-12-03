// Formulario de ubicaciones
const formUbicacion = document.getElementById("formUbicaciones");
formUbicacion.addEventListener("submit", function (event) {
  event.preventDefault();
  const idTorneo = formUbicacion.getAttribute("data-id");
  const lugar = document.querySelector("#lugar").value;
  const cancha = document.querySelector("#cancha").value;

  if (lugar === "" || cancha === "") {
    alert("Todos los campos son obligatorios");
    return;
  }

  const datosUbicacion = {
    lugar: lugar,
    cancha: cancha,
    id_torneo: idTorneo,
  };

  fetch(`/ubicacion/${idTorneo}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datosUbicacion),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        swal("Exitoso!", "¡Registro de la ubicación exitoso!", "success");
        formUbicacion.reset();
      } else {
        alert(data.error || "Error al registrar la ubicación");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocurrió un error al enviar los datos.");
    });
});
