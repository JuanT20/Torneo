document.addEventListener("DOMContentLoaded", function () {
  // Función para almacenar los datos del formulario en sessionStorage
  function guardarDatosEnSessionStorage() {
    const formData = {};
    const inputs = document.querySelectorAll(
      "#formPartidos input, #formPartidos select"
    );

    inputs.forEach((input) => {
      formData[input.id] = input.value;
    });

    const currentPage =
      document.querySelector(".page-link.active").textContent || "1";
    sessionStorage.setItem(
      `fixtures_pagina_${currentPage}`,
      JSON.stringify(formData)
    );
  }

  // Función para restaurar los datos desde sessionStorage
  function restaurarDatosDesdeSessionStorage() {
    const currentPage =
      document.querySelector(".page-link.active").textContent || "1";
    const savedData = sessionStorage.getItem(`fixtures_pagina_${currentPage}`);

    if (savedData) {
      const data = JSON.parse(savedData);
      const inputs = document.querySelectorAll(
        "#formPartidos input, #formPartidos select"
      );

      inputs.forEach((input) => {
        if (data[input.id]) {
          input.value = data[input.id];
        }
      });
    }
  }

  // Restaurar los datos cuando la página se cargue
  restaurarDatosDesdeSessionStorage();

  // Manejar los enlaces de paginación para no recargar la página
  const paginationLinks = document.querySelectorAll(".pagination a");
  paginationLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault(); // Evitar la recarga de la página

      // Guardar los datos actuales antes de cambiar de página
      guardarDatosEnSessionStorage();

      const url = this.getAttribute("href");

      // Usar AJAX para cargar el contenido de la siguiente página sin recargar la página completa
      fetch(url, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.text())
        .then((html) => {
          // Actualizar el contenido de la página actual con el nuevo HTML
          const fixturesContainer =
            document.getElementById("fixtures-container");
          fixturesContainer.innerHTML = html;

          // Restaurar los datos del formulario de la nueva página cargada
          restaurarDatosDesdeSessionStorage();
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Hubo un problema al cargar los fixtures.");
        });
    });
  });
});
