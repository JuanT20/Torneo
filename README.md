# ⚽️ Sistema de Gestión de Torneos de Fútbol

Bienvenido a **Sistema de Gestión de Torneos de Fútbol**, una plataforma diseñada para organizar y gestionar torneos de fútbol en diferentes modalidades: 11, 9, 8, 7 y salón. Este sistema ofrece funcionalidades tanto para organizadores como para espectadores, adaptándose a las necesidades de cada usuario.

---

## 🌟 Características del Proyecto

### 🔐 Tipos de Cuenta

1. **Cuenta Free**:

   - Permite organizar torneos básicos con funcionalidades limitadas.
   - Estadísticas generales de los torneos.

2. **Cuenta Premium**:

   - Acceso a herramientas avanzadas como:
     - Gestión detallada de fases y partidos.
     - Análisis estadístico completo de equipos y jugadores.
     - Reportes personalizados.

3. **Cuenta Espectador**:
   - Registro obligatorio para acceder al seguimiento de torneos.
   - Visualización de estadísticas y posiciones.

### 🛠 Funcionalidades Principales

- **Creación de Torneos**:

  - Configuración de modalidades (11, 9, 8, 7, salón).
  - Organización de fases y partidos.

- **Gestión de Equipos y Jugadores**:

  - Registro de equipos participantes.
  - Detalle de jugadores por equipo.

- **Estadísticas y Posiciones**:

  - Estadísticas detalladas de jugadores (goles, tarjetas, etc.).
  - Tabla de posiciones actualizada en tiempo real.

- **Visualización para Espectadores**:
  - Seguimiento completo del torneo.
  - Interfaz amigable para consultar estadísticas y horarios.

---

## 🌐 Tecnologías Utilizadas

| **Tecnología** | **Uso**                                     |
| -------------- | ------------------------------------------- |
| **HTML & CSS** | Estructura y diseño de la interfaz.         |
| **Bootstrap**  | Framework de diseño para estilos avanzados. |
| **JavaScript** | Dinamismo y manejo de interacciones.        |
| **Python**     | Lógica backend y gestión de la aplicación.  |
| **MySQL**      | Almacenamiento de datos.                    |

---

## 📂 Estructura del Proyecto

📁 torneos-futbol
├── 📂 app/ # Lógica principal de la aplicación
│ ├── main.py # Archivo principal para iniciar la aplicación
│ ├── routes.py # Definición de las rutas de la aplicación
│ ├── services.py # Lógica de negocio y cálculos específicos
│ └── utils.py # Funciones auxiliares y reutilizables
├── 📂 templates/ # Archivos HTML para la interfaz
│ ├── base.html # Plantilla base para reutilizar estructura
│ ├── index.html # Página principal
│ ├── torneo.html # Detalle del torneo
│ └── equipo.html # Detalle del equipo
├── 📂 static/ # Archivos estáticos
│ ├── css/
│ │ ├── styles.css # Estilos personalizados
│ │ └── bootstrap.min.css # Framework Bootstrap
│ ├── js/
│ │ ├── scripts.js # Funciones dinámicas de la interfaz
│ │ └── helpers.js # Funciones auxiliares de JavaScript
│ └── img/ # Imágenes del proyecto
│ ├── logo.png
│ └── fondo.jpg
├── 📂 db/ # Archivos relacionados con la base de datos
│ ├── connection.py # Conexión a la base de datos MySQL
│ └── queries.sql # Consultas SQL utilizadas en el proyecto
├── 📂 tests/ # Archivos para pruebas
│ ├── test_routes.py # Pruebas para las rutas
│ ├── test_services.py # Pruebas para lógica de negocio
│ └── test_db.py # Pruebas para la base de datos
├── 📂 docs/ # Documentación del proyecto
│ ├── API.md # Documentación de las rutas de la API
│ ├── requirements.md # Detalles de los requisitos
│ └── changelog.md # Registro de cambios del proyecto
├── requirements.txt # Dependencias de Python necesarias
├── config.py # Configuración general del proyecto
├── .gitignore # Archivos y carpetas a ignorar en Git
├── LICENSE # Licencia del proyecto
└── README.md # Documentación general del proyecto
