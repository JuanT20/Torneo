document
  .getElementById("formSingUp")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    let nombre = document.querySelector("#nombre").value;
    let correo = document.querySelector("#correo").value;
    let contraseña = document.querySelector("#password").value;

    let datoSingUp = {
      nombre: nombre,
      correo: correo,
      password: contraseña,
    };

    try {
      fetch("/singUp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datoSingUp),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.redirect_url) {
            window.location.href = data.redirect_url;
          } else {
            console.error(data.error);
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
