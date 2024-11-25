// Capturar clic en los botones de "Registrar Jugadores"
document.querySelectorAll("#btnRegistro").forEach((boton) => {
  boton.addEventListener("click", function () {
    const idEquipo = this.dataset.id; // Obtener el ID del equipo desde data-id
    localStorage.setItem("idEquipo", idEquipo); // Guardar el ID en localStorage (opcional)

    // Redirigir al formulario de registro con el ID del equipo como parámetro en la URL
    window.location.href = `/register-jugadores?id_equipo=${idEquipo}`;
  });
});

// Capturar el formulario y gestionar su envío
const formJugadores = document.getElementById("formJugadores");
if (formJugadores) {
  formJugadores.addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar el envío tradicional del formulario

    // Obtener los valores del formulario
    const idEquipo = document.querySelector("#idEquipo").value;
    const idJugador = document.querySelector("#identificacion").value;
    const nombre = document.querySelector("#nombre").value;
    const posicion = document.querySelector("#posicion").value;
    const fechaNac = document.querySelector("#fechaNac").value;
    const edad = document.querySelector("#edad").value;
    const nacionalidad = document.querySelector("#nacionalidad").value;
    const sexo = document.querySelector("#hombre").checked ? "hombre" : "mujer";

    // Crear el objeto con los datos a enviar
    const datosJugador = {
      idEquipo: idEquipo, // Incluyendo el ID del equipo
      idJugador: idJugador,
      nombre: nombre,
      posicion: posicion,
      fechaNac: fechaNac,
      edad: edad,
      nacionalidad: nacionalidad,
      sexo: sexo,
    };

    // Enviar los datos al backend usando Fetch API
    fetch("/register-jugadores", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(datosJugador),
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
}
