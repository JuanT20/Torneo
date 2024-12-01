// Capturar el formulario y gestionar su envío
const formPartidos = document.getElementById("formPartidos");
if (formPartidos) {
  formPartidos.addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar el envío tradicional del formulario

    // Obtener los valores del formulario
    const idTorneo = document.querySelector("#idTorneo").value;
    const idLocal = document.querySelector("#idLocal").value;
    const idVisitante = document.querySelector("#idVisitante").value;
    const fecha = document.querySelector("#fecha").value;
    const hora = document.querySelector("#hora").value;
    const ubicacion = document.querySelector("#ubicacion").value;
    const arbitro = document.querySelector("#arbitro").value;

    if (!idTorneo) {
      console.error("El ID del torneo no se ha proporcionado correctamente");
      return; // Detener el envío si no se tiene el ID del torneo
    }
    console.log(idTorneo);
    console.log(idLocal);
    console.log(idVisitante);

    // Crear el objeto con los datos a enviar
    const datosPartido = {
      idTorneo: idTorneo,
      partidos: [
        {
          idLocal: idLocal,
          idVisitante: idVisitante,
          fecha: fecha,
          hora: hora,
          ubicacion: ubicacion,
          arbitro: arbitro,
        },
      ],
    };
    console.log(datosPartido);
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
