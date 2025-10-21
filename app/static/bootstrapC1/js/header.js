const headerHTML = `<header id="header" class="header d-flex align-items-center fixed-top bg-dark">
    <div class="container-fluid container-xl position-relative d-flex align-items-center justify-content-between">
      <a href="../index.html" class="logo d-flex align-items-center me-auto me-lg-0">
        <h1>INSTITUTO<br>TECNOLÓGICO<br>FRANFER</h1>
      </a>
      <nav id="navmenu" class="navmenu">
        <ul>
          <li><a href="../index.html">Página Principal<br></a></li>
          <li><a href="#inicio">Volver al inicio</a></li>
          <li><a href="#sobre">Sobre la carrera</a></li>
          <li><a href="#malla">Malla Curricular</a></li>
          <li><a href="#perfil">Perfil Profesional</a></li>
          <li><a href="#contactos">Contactos</a></li>
        </ul>
        <i class="mobile-nav-toggle d-xl-none bi bi-list"></i>
      </nav>
    </div>
  </header>

  <div id="inicio" class="page-title bg-dark" data-aos="zoom-in" data-aos-duration="1500">
    <div style="width: 100vw; height: 55vh; overflow: hidden; position: relative;">
      <img src="../galeria/imagenes/carreras.jpg" alt="Fondo"
        style="width: 100%; height: auto; position: absolute; top: 36%; left: 0;">
    </div>
  </div>
  `;


// Función para cargar el bloque HTML en la página
function loadBlock(blockID, content) {
  document.getElementById(blockID).innerHTML = content;
}

// Cargar bloques cuando la página se carga
window.addEventListener('load', function() {
  loadBlock('header-container', footerHTML);
});