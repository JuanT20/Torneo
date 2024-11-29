const formPartidos = document.getElementById("form-partidos");
formPartidos.addEventListener("submit", (event) => {
  event.preventDefault();

  let fecha = document.querySelector("#fecha").value;
  let hora = document.querySelector("#hora").value;
  let ubicacion = document.querySelector("#ubicacion").value;
  let arbitro = document.querySelector("#arbitro").value;

  const datosPartidos = {
    fecha: fecha,
    hora: hora,
    ubicacion: ubicacion,
    arbitro: arbitro,
  };

  // Enviar los datos al backend usando Fetch API
  fetch("/partidos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datosPartidos),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.mensaje) {
        swal("Exitoso!", "¡Registro del Jugador exitoso!", "success"); // Mensaje de éxito
        formJugadores.reset(); // Resetear el formulario
      } else if (data.error) {
        swal("Oops!", "Ocurrió un error en el registro.", "error"); // Mensaje de error
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocurrió un error al enviar los datos.");
    });
});
