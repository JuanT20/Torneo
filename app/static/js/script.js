document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll("a[data-page]");
  const contentDiv = document.getElementById("dynamic-content");

  links.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const page = link.getAttribute("data-page");

      fetch(`/${page}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.text();
        })
        .then((html) => {
          contentDiv.innerHTML = html;
        })
        .catch((err) => console.error("Error cargando la página:", err));
    });
  });
});
