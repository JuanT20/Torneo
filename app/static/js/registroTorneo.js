const formTorneo = document.getElementById("formTorneo");
formTorneo.addEventListener("submit", function (event) {
  event.preventDefault(); // Evita el envío tradicional del formulario

  // Obtener los valores del formulario
  const nombreTorneo = document.querySelector("#nombreTorneo").value;
  const tipoTorneo = document.querySelector("#tipoTorneo").value;
  const formatoTorneo = document.querySelector("#formatoTorneo").value;
  const numeroEquipos = document.querySelector("#nEquipos").value;
  const fechaInicio = document.querySelector("#fechaIni").value;
  const fechaFin = document.querySelector("#fechaFin").value;

  // Crear el objeto con los datos a enviar
  const datosTorneo = {
    nombreTorneo: nombreTorneo,
    tipoTorneo: tipoTorneo,
    formatoTorneo: formatoTorneo,
    numeroEquipos: numeroEquipos,
    fechaInicio: fechaInicio,
    fechaFin: fechaFin,
  };

  // Enviar los datos al backend usando Fetch API
  fetch("/register-torneo", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datosTorneo),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.mensaje) {
        swal("Exitoso!", "Registro del Torneo!", "success"); // mensaje de éxito
        formTorneo.reset();
      } else if (data.error) {
        swal("Oops!", "Ocurrió un error en el registro!", "error"); //mensaje de error
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocurrió un error al enviar los datos");
    });
});
