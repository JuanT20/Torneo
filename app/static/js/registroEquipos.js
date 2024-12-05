document.addEventListener("DOMContentLoaded", function () {
  // Obtener el ID del torneo (asumiendo que lo tienes disponible en algún elemento del DOM)
  const idTorneo = document.getElementById("id_torneo").value;

  // Solicitar el número de equipos al servidor
  fetch(`/numero-equipos/${idTorneo}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Verifica la respuesta aquí
      if (data.numero_equipos > 0) {
        const numeroEquipos = data.numero_equipos; // Accede directamente al número de equipos
        const contenedorEquipos = document.getElementById("contenedorEquipos");

        for (let i = 1; i <= numeroEquipos; i++) {
          // Código para crear los inputs para los equipos
          const formGroup = document.createElement("div");
          formGroup.classList.add("mb-3");

          formGroup.innerHTML = `
          <div class="row mb-3 align-items-center">
            <div class="col-1">
              <label for="equipo${i}" class="form-label">${i}</label>
            </div>
            <div class="col">
              <input
                type="text"
                id="equipo${i}"
                name="equipo${i}"
                class="form-control"
                placeholder="Nombre del equipo ${i}"
                required
              />
            </div>
            <div class="col">
              <input
                type="file"
                id="escudo${i}"
                name="escudo${i}"
                class="form-control"
                accept="image/*"
              />
            </div>
          </div>
          `;

          contenedorEquipos.appendChild(formGroup);
        }
      } else {
        alert(
          "No se encontró el número de equipos. Por favor, regresa al formulario anterior."
        );
      }
    })
    .catch((error) => {
      console.error("Error al obtener el número de equipos:", error);
      alert("Hubo un problema al cargar los equipos.");
    });
});

document.getElementById("rEquipos").addEventListener("click", function (event) {
  event.preventDefault();

  const formEquipos = document.getElementById("formEquipos");
  const formData = new FormData(formEquipos);

  // Obtener el id del torneo desde el formulario o el DOM
  const idTorneo = document.getElementById("id_torneo").value;

  // Validar que todos los nombres de los equipos no estén vacíos
  const numeroEquipos = formEquipos.querySelectorAll("input[type='text']");
  let formularioValido = true;

  numeroEquipos.forEach((input) => {
    if (input.value.trim() === "") {
      formularioValido = false;
      input.classList.add("is-invalid"); // Agregar clase para resaltar el error
    } else {
      input.classList.remove("is-invalid"); // Quitar clase si es válido
    }
  });

  if (!formularioValido) {
    alert("Por favor, completa todos los nombres de los equipos.");
    return; // Salir de la función si la validación falla
  }

  try {
    fetch(`/register-equipos/${idTorneo}`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          window.location.href = data.redirect_url;
        } else {
          alert(data.error);
        }
      })
      .catch((error) => console.error("Error:", error));
  } catch (error) {
    console.error("Error:", error, data);
  }
});
