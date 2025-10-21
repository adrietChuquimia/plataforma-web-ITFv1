// Bloque de pie de página
const footerHTML = `
  <footer id="footer" class="footer">
        <section id="contact" class="contact section">
          <div class="footer-top">
            <div class="container">
              <div class="row gy-4">
                <div class="col-lg-4 col-md-6 footer-about">
                  <a href="index.html" class="logo d-flex align-items-center">
                    <span class="sitename">INSTITUTO<br>TECNOLÓGICO<br>FRANFER</span>
                  </a>
                  <div class="footer-contact pt-3">
                    <p>Zona Ballivian, Av. Alfonso Ugarte</p>
                    <p>Calle Sargento Carrasco #25</p>
                    <p class="mt-3"><strong>Nro de celular:</strong> <span>2845936 - 64213666</span></p>
                    <p><strong>Email:</strong> <span>institutotecnologicofranfer@gmail.com</span></p>
                  </div>
                </div>

                <!-- AGREGAR ENLACES DE LAS REDES OFICIALES (TAL COMO FACEBOOK)-->
                <div class="col-lg-4 col-md-6 footer-links">
                  <h4>REDES SOCIALES</h4>
                  <ul>
                    <li><i class="bi bi-chevron-right bi-facebook"></i> <a
                        href="https://www.facebook.com/profile.php?id=61553780056531&mibextid=ZbWKwL" target="_blank">
                        Facebook</a></li>

                    <li><i class="bi bi-chevron-right bi-instagram"></i> <a
                        href="https://www.instagram.com/inst_tec_franfer?igsh=MWI2OTZiN2c5eGtmMg==" target="_blank">
                        Instagram</a></li>
                    <li><i class="bi bi-chevron-right bi-whatsapp"></i> <a href="https://wa.me/message/3VMO564TW7DBP1"
                        target="_blank"> Whatsapp</a></li>
                    <li><i class="bi bi-chevron-right bi-tiktok"></i> <a
                        href="https://www.tiktok.com/@inst_tec_franfer?_t=8nuuoXrjO1W&_r=1" target="_blank"> TikTok</a>
                    </li>
                    <li><i class="bi bi-chevron-right bi-youtube"></i> <a
                        href="https://www.youtube.com/@INSTITUTOTECNOLOGICOFRANFER" target="_blank">YouTube</a></li>
                  </ul>
                </div>
                <div class="col-lg-4 col-md-6 footer-links"></div>
                <h2>Dirección</h2>
                <div class="s-f-col s-f-col-map cf">
                  <div class="b b-map b-s" style="margin-left:0%;margin-right:0%;">
                    <div class="b-c" id="wnd_MapBlock_549825834_container"
                      style="position:relative;padding-bottom:40%;">
                      <iframe
                        src="https://web-2022.webnode.it/widgets/googlemaps/?z=15&amp;a=INSTITUTO+TECNOLOGICO+FRANFER"
                        style="position:absolute;top:0%;left:0%;width:100%;height:100%;" loading="lazy"></iframe>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="copyright">
            <div class="container text-center">
              <p>© <span>Copyright</span> <strong class="px-1 sitename">ITF</strong> <span>All Rights Reserved</span>
              </p>
              <div class="credits">
                Designed by <a href="https://bootstrapmade.com/">Bootstrap</a>
              </div>
            </div>
          </div>

      </footer>
`;

// Función para cargar el bloque HTML en la página
function loadBlock(blockID, content) {
  document.getElementById(blockID).innerHTML = content;
}

// Cargar bloques cuando la página se carga
window.addEventListener('load', function() {
  loadBlock('footer-container', footerHTML);
});