/**Dinamismo del formulario den registro de Equipos */
document.getElementById("nEquipos").addEventListener("change", function () {
  const numEquipos = this.value;
  const formEqupos = document.getElementById("form-equipos");
  formGroup.innerHTML = ""; // Limpiar el formulario anterior

  for (let i = 1; i <= numEquipos; i++) {
    // Crear un grupo de inputs para cada materia
    const formtorneo = document.createElement("div");
    formGroup.classList.add("mb-3");

    formGroup.innerHTML = `
              <h5>Equipos ${i}</h5>
              
          `;

    formtorneo.appendChild(formGroup);
  }
});
