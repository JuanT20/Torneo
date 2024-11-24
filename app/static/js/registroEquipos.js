// Al cargar la página, obtener el número de equipos desde localStorage
document.addEventListener("DOMContentLoaded", function () {
  const numeroEquipos = localStorage.getItem("numeroEquipos"); // Leer el valor guardado
  const contenedorEquipos = document.getElementById("contenedorEquipos");

  if (numeroEquipos) {
    for (let i = 1; i <= numeroEquipos; i++) {
      // Crear un grupo de inputs para cada equipo
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
});
document.getElementById("rEquipos").addEventListener("click", function (event) {
  event.preventDefault();

  const formEquipos = document.getElementById("formEquipos");
  const formData = new FormData(formEquipos);

  try {
    fetch("/register-equipos", {
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
