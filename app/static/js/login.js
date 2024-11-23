document
  .getElementById("formLogin")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    let correo = document.querySelector("#correo").value;
    let contrasena = document.querySelector("#password").value;

    let datosLogin = {
      correo: correo,
      contrasena: contrasena,
    };

    try {
      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datosLogin),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.redirect_url) {
            window.location.href = data.redirect_url;
          } else {
            swal("Oops", data.error || "Credenciales incorrectas!", "error");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Ocurrió un error al enviar los datos");
        });
    } catch (error) {
      console.error("Error en la construcción del JSON:", error);
    }
  });
