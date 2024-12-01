const formUbicacion = document.getElementById("formUbicaciones");

formUbicacion.addEventListener("submit", function (event) {
  event.preventDefault(); // Evitar el envío tradicional del formulario

  const lugar = document.querySelector("#lugar").value;
  const cancha = document.querySelector("#cancha").value;

  // Validar los campos
  if (lugar === "" || cancha === "") {
    alert("Todos los campos son obligatorios");
    return;
  }

  // Crear el objeto con los datos a enviar
  const datosUbicacion = {
    lugar: lugar,
    cancha: cancha,
  };

  // Enviar los datos al backend
  fetch("/arb-ubi", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datosUbicacion),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        alert("Ubicación registrada correctamente");
        formUbicacion.reset(); // Limpiar el formulario
      } else {
        alert("Hubo un error al registrar la ubicación");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocurrió un error al enviar los datos.");
    });
});

const formArbitro = document.getElementById("formArbitros");
formArbitro.addEventListener("submit", function (event) {
  event.preventDefault(); // Evitar el envío tradicional del formulario

  const identificacion = document.querySelector("#id_arbitro").value;
  const nombre = document.querySelector("#nombre").value;
  const experiencia = document.querySelector("#experiencia").value;

  // Validar los campos
  if (lugar === "" || cancha === "") {
    alert("Todos los campos son obligatorios");
    return;
  }

  // Crear el objeto con los datos a enviar
  const datosArbitro = {
    identificacion: identificacion,
    nombre: nombre,
    experiencia: experiencia,
  };

  // Enviar los datos al backend
  fetch("/arb-ubi", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datosArbitro),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        alert("Ubicación registrada correctamente");
        formUbicacion.reset(); // Limpiar el formulario
      } else {
        alert("Hubo un error al registrar la ubicación");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocurrió un error al enviar los datos.");
    });
});
