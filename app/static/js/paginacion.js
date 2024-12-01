document.addEventListener("DOMContentLoaded", function () {
  const fixturesContainer = document.getElementById("fixtures-container");
  const paginationLinks = document.querySelectorAll(".pagination a");

  paginationLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault(); // Evitar recarga de página

      const url = this.getAttribute("href");

      fetch(url, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest", // Header para identificar solicitud AJAX
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error en la solicitud");
          }
          return response.text();
        })
        .then((html) => {
          // Actualizar el contenido de los fixtures
          fixturesContainer.innerHTML = html;

          // Re-inicializar los eventos de paginación
          attachPaginationEvents();
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Hubo un problema al cargar los fixtures");
        });
    });
  });

  function attachPaginationEvents() {
    const newPaginationLinks = document.querySelectorAll(".pagination a");
    newPaginationLinks.forEach((link) => {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        const url = this.getAttribute("href");

        fetch(url, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((response) => response.text())
          .then((html) => {
            fixturesContainer.innerHTML = html;
            attachPaginationEvents();
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Hubo un problema al cargar los fixtures");
          });
      });
    });
  }
});
