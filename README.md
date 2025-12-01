PLATAFORMA WEB EDUCATIVA POTENCIADA CON VISION COMPUTACIONAL Y SISTEMA EXPERTO DIFUSO PARA EL APRENDIZAJE DE COMPONENTES AUTOMOTRICES
---Descripción
Plataforma web para el aprendizaje de componentes automotricesa travez de trivia experta, vision computacional de componentes automotrices, diccionario de componentes automotrices
y modelos 3d automovilísticos. Enfocado en principiantes del área automotriz fomentando el aprendizaje autonomo.
---Tecnologías
gunicorn==23.0.0
firebase_admin==7.1.0
Pyrebase4==4.8.0
opencv-python-headless==4.11.0.86
numpy==1.24.3
scikit-fuzzy==0.5.0
pillow==11.1.0
tensorflow==2.13.0
keras==2.13.1
huggingface-hub==0.29.3
---Uso del sistema
1. La plataforma inicia con la página principal, disponible para todo público con información institucional
2. En la parte superior derecha cuenta con un boton "acceder al sistema" entrar ahí
3. Se habilita el login, solo usuarios registrados podrán ingresar con su correo electronico y contraseña
4. Se habilita el panel de estudiante, que presenta las opciones de trivia, vision computacional, diccionario, modelos 3d y para ti
5. TRIVIA: Inicia el juego con 5 vidas, el sistema evalua los errores, aciertos, tiempo y precision para adaptarse al nivel del jugador, la subida de nivel dependerá de la racha.
          NIVEL 1: Preguntas de opción múltiple
          NIVEL 2: Preguntas de opcion múltiple con límite de tiempo
          NIVEL 3: Se debe ingresar la respuesta por teclado
          NIVEL 4: Aleatoriamente se muestran preguntas de los anteriores 3 niveles
          NIVEL 5: Se debe ingresar la respuesta por teclado con límite de tiempo
6. VISION COMPUTACIONAL: Se saca una foto en tiempo real de la pieza que se desee y mostrará las caracteristicas si la prediccion es mayor al 80%. Tambien se puede subir una imagen desde
   el dispositivo. En caso de que sea menor la predicción, no se mostrará ninguna caracteristica.
7. DICCIONARIO: Repositorio general que muestra todas las piezas registradas con sus características en formato tarjeta
8. MODELO 3D: Muestra una liena del tiempo automotriz con historia de autos por décadas
9. PARA TI: Mensaje motivacional para los usuarios
10. Para salir en la parte superior derecha en todo momento se muestra el boton de "Cerrar Sesión" que retornará al login y de ahi se pude retornar a la página principal
---Fuentes de plataformas utilizadas
•	Flaticon. (2023). Iconos gratis de HTML[Sitio web]https://www.flaticon.es/ico
•	nos-gratis/html
•	Google. (2023). Firebase: Plataforma para desarrollo de aplicaciones web y móviles [Sitio web]. https://firebase.google.com/
•	Google. (2023). Teachable Machine [Sitio Web].https://teachablemachine.withgoogle.com/
•	Hugging Face. (2023). Hugging Face Hub [Sitio web]. https://huggingface.com
•	Poly Pizza. (2023). Poly Pizza: Descarga de modelos 3D [Sitio web]. https://poly.pizza/
•	Render. (2023). Render: Plataforma de despliegue web [Sitio web]. https://render.com/
•	Responsible AI. (2023). Responsible.app [Sitio web]. https://responsible.app/
---Autora
Adriet Daniela Chuquimia Centeno - 2025
Estado: Estable con uso educativo
