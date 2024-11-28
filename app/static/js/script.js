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

//Script para los checkBox
//CheckBox Sing uP
const yesTorneo = document.querySelector("#yesTorneo");
const noTorneo = document.querySelector("#noTorneo");
yesTorneo.checked = false;
noTorneo.checked = false;

// Desabilitar el check cuando se selecciona uno de los roles.
yesTorneo.addEventListener("change", (event) => {
  noTorneo.disabled = event.target.checked;
  //checkEstudiante.disabled = document.querySelector("#profesor").checked;
});
noTorneo.addEventListener("change", (event) => {
  yesTorneo.disabled = event.target.checked;
  //checkEstudiante.disabled = document.querySelector("#profesor").checked;
});

//CheckBox Juadores
