// Capturar el formulario y gestionar su envío
const formPartidos = document.getElementById("formPartidos");
if (formPartidos) {
  formPartidos.addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar el envío tradicional del formulario

    // Obtener el ID del torneo
    const idTorneo = document.querySelector("#idTorneo").value;
    if (!idTorneo) {
      console.error("El ID del torneo no se ha proporcionado correctamente");
      return; // Detener el envío si no se tiene el ID del torneo
    }

    // Inicializamos un array para los partidos
    const partidos = [];

    // Recorrer todas las filas de la tabla de partidos
    const rows = document.querySelectorAll("tbody tr");
    rows.forEach((row) => {
      const idLocal = row.querySelector("#idLocal").value;
      const idVisitante = row.querySelector("#idVisitante").value;
      const fecha = row.querySelector("#fecha").value;
      const hora = row.querySelector("#hora").value;
      const ubicacion = row.querySelector("#ubicacion").value; // Solo capturamos el ID de la ubicación
      const arbitro = row.querySelector("#arbitro").value; // Solo capturamos el ID del árbitro

      // Agregar el partido a la lista
      partidos.push({
        idLocal,
        idVisitante,
        fecha,
        hora,
        ubicacion, // ID de la ubicación
        arbitro, // ID del árbitro
      });
    });

    // Crear el objeto con los datos a enviar
    const datosPartido = {
      idTorneo: idTorneo,
      partidos: partidos,
    };
    console.log(datosPartido); // Verificar los datos antes de enviarlos

    // Enviar los datos al backend usando Fetch API
    fetch("/guardar_partidos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(datosPartido),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.mensaje) {
          swal("Exitoso!", "¡Partido registrado exitosamente!", "success"); // Mensaje de éxito
          formPartidos.reset(); // Resetear el formulario
        } else if (data.error) {
          swal("Oops!", data.error, "error"); // Mensaje de error
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Ocurrió un error al enviar los datos.");
      });
  });
}
