document.getElementById("logout").addEventListener("click", function (event) {
  event.preventDefault(); // Evita que el enlace recargue la página

  fetch("/logout", { method: "GET" }) // Llama a la ruta del backend para cerrar sesión
    .then((response) => response.json())
    .then((data) => {
      alert(data.mensaje); // Muestra un mensaje al usuario
      window.location.href = "/login"; // Redirige al login tras cerrar sesión
    })
    .catch((error) => console.error("Error al cerrar sesión:", error));
});
