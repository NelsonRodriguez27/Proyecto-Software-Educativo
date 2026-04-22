
 /* 
   CONFIGURACIN
  */
 const owl     = document.getElementById('gaussBtnImg');
 const gaussMessage = document.getElementById('gaussMessage');
 const vozEstado  = document.getElementById('vozEstado');
 const vozTexto   = document.getElementById('vozTexto');
 const musica    = document.getElementById('musica'); // AUDIO DE FONDO

 const mensajes = {
  inicio:   "¡Hola! Soy Gauss. Te ayudaré a aprender matemáticas paso a paso.",
  general:   "Este es el objetivo general. Aquí aprenderás jugando con matemáticas.",
  especifico1: "Aquí aprenderás con ejemplos visuales sobre valor posicional, sumas y restas.",
  especifico2: "Aquí practicarás con ejercicios interactivos para aprender haciendo.",
  especifico3: "Aquí te motivarás con juegos, retos y recompensas para seguir aprendiendo."
 };
  let lastMessage = "";
  let gaussBubble = null;
  let gaussBtn = null;
  let gaussBtnImg = null;
  let gaussBubbleTitle = null;
  let gaussBubbleText = null;
  let hideTimer = null;

  function ponerGaussEnReposo() {
   if (!gaussBtnImg) return;
   gaussBtnImg.src = gaussBtnImg.dataset.idleSrc || gaussBtnImg.src;
   if (gaussBtn) gaussBtn.classList.remove("is-speaking");
  }

  function ponerGaussHablando() {
   if (!gaussBtnImg) return;
   gaussBtnImg.src = gaussBtnImg.dataset.speakingSrc || gaussBtnImg.src;
   if (gaussBtn) gaussBtn.classList.add("is-speaking");
  }

  function actualizarBurbujaGauss(texto, titulo = "Gauss te orienta") {
   if (!gaussBubbleText || !gaussBubbleTitle) return;
   gaussBubbleTitle.textContent = titulo;
   gaussBubbleText.textContent = texto || lastMessage || "Gauss está listo para ayudarte.";
  }

  function mostrarBurbujaGauss(tiempo = null) {
   if (!gaussBubble || !gaussBtn) return;
   if (hideTimer) {
    clearTimeout(hideTimer);
    hideTimer = null;
   }
   gaussBubble.classList.add("show");
   gaussBtn.classList.add("open");
   gaussBtn.setAttribute("aria-expanded", "true");
   if (typeof tiempo === "number" && tiempo > 0) {
    hideTimer = setTimeout(() => {
     ocultarBurbujaGauss();
    }, tiempo);
   }
  }

  function ocultarBurbujaGauss() {
   if (!gaussBubble || !gaussBtn) return;
   if (hideTimer) {
    clearTimeout(hideTimer);
    hideTimer = null;
   }
   gaussBubble.classList.remove("show");
   gaussBtn.classList.remove("open");
   gaussBtn.setAttribute("aria-expanded", "false");
  }

  function inicializarBotonFlotanteGauss() {
   gaussBubble = document.getElementById("gaussBubble");
   gaussBtn = document.getElementById("gaussBtn");
   gaussBtnImg = document.getElementById("gaussBtnImg");
   gaussBubbleTitle = document.getElementById("gaussBubbleTitle");
   gaussBubbleText = document.getElementById("gaussBubbleText");
   ponerGaussEnReposo();

   if (!gaussBtn || !gaussBubble) return;

   gaussBtn.addEventListener("click", () => {
    const yaVisible = gaussBubble.classList.contains("show");
    if (yaVisible) {
     ocultarBurbujaGauss();
     return;
    }
    actualizarBurbujaGauss(lastMessage || "Gauss está listo para ayudarte.", "¡Hola! Soy Gauss");
    mostrarBurbujaGauss(4000);
   });
  }

  document.addEventListener("DOMContentLoaded", inicializarBotonFlotanteGauss);

 /* 
   SISTEMA DE VOZ
  */
 let vozGauss = null;
 let vocesListas = false;
 let vozActivada = false;

 function actualizarEstadoVoz(estado, msg) {
  if (!vozEstado || !vozTexto) return;
  vozEstado.className = 'voz-estado ' + estado;
  vozTexto.textContent = msg;
 }

 function cargarVoces() {
  const lista = window.speechSynthesis.getVoices();
  if (lista.length === 0) return false;

  vozGauss =
   lista.find(v => /monica|paulina|helena|sandra|sofia|sabina|luciana/i.test(v.name) && /es/i.test(v.lang)) ||
   lista.find(v => /es-HN/i.test(v.lang)) ||
   lista.find(v => /es-MX/i.test(v.lang)) ||
   lista.find(v => /es-ES/i.test(v.lang)) ||
   lista.find(v => /es/i.test(v.lang)) ||
   lista[0];

  vocesListas = true;
  return true;
 }

 if ('speechSynthesis' in window) {
  if (!cargarVoces()) {
   window.speechSynthesis.onvoiceschanged = () => { cargarVoces(); };
   setTimeout(() => {
    if (!vocesListas) {
     const lista = window.speechSynthesis.getVoices();
     if (lista.length > 0) {
      vozGauss = lista.find(v => /es/i.test(v.lang)) || lista[0];
      vocesListas = true;
     }
    }
   }, 3000);
  }
  actualizarEstadoVoz('inactiva', 'Iniciando voz...');
 } else {
  actualizarEstadoVoz('inactiva', 'Tu navegador no soporta voz');
 }

 /* 
   MSICA DE FONDO
  */
 function iniciarMusica() {
  if (!musica) return;

  musica.loop = true;
  musica.volume = 0.35;

  const playPromise = musica.play();

  if (playPromise !== undefined) {
   playPromise
    .then(() => {
     console.log("Música de fondo iniciada correctamente");
    })
    .catch(err => {
     console.warn("El navegador bloqueó la reproducción automática:", err);

     // Reintento al primer clic del usuario en cualquier parte
     document.addEventListener('click', reintentarMusica, { once: true });
    });
  }
 }

 function reintentarMusica() {
  if (!musica) return;
  musica.play().catch(err => console.warn("No se pudo iniciar la música:", err));
 }

 /* 
   ESCRITURA EN BURBUJA
  */
 let escribiendoIntervalo = null;

 function escribirBurbuja(texto, velocidad = 20) {
  return new Promise(resolve => {
   if (!gaussMessage) {
    resolve();
    return;
   }

   if (escribiendoIntervalo) clearInterval(escribiendoIntervalo);

   gaussMessage.textContent = "";
   gaussMessage.classList.add("typing");
   let i = 0;

   escribiendoIntervalo = setInterval(() => {
    gaussMessage.textContent += texto.charAt(i);
    i++;

    if (i >= texto.length) {
     clearInterval(escribiendoIntervalo);
     escribiendoIntervalo = null;
     gaussMessage.classList.remove("typing");
     resolve();
    }
   }, velocidad);
  });
 }

 /* 
   CHISPAS
  */
 function crearChispas(x, y) {
  for (let i = 0; i < 8; i++) {
   const s = document.createElement("div");
   s.className = "spark";
   s.style.left = x + "px";
   s.style.top = y + "px";
   s.style.setProperty("--x", (Math.random() - 0.5) * 120 + "px");
   s.style.setProperty("--y", (Math.random() - 0.5) * 120 + "px");
   document.body.appendChild(s);
   setTimeout(() => s.remove(), 1000);
  }
 }

 /* 
   ESTADOS DEL BHO
  */
 function activarHabla() {
   if (owl) owl.classList.add("talking");
   ponerGaussHablando();
  }

  function desactivarHabla() {
   if (owl) owl.classList.remove("talking");
   ponerGaussEnReposo();
  }

 desactivarHabla();

 /* 
   FUNCIN PRINCIPAL DE HABLAR
  */
 let watchdogTimer = null;
 let resumeInterval = null;

 async function hablar(texto, elemento) {
  if (elemento) {
   elemento.scrollIntoView({ behavior: "smooth", block: "center" });
   const rect = elemento.getBoundingClientRect();
   crearChispas(rect.left + rect.width / 2, rect.top + rect.height / 2);
  }
   escribirBurbuja(texto);
   lastMessage = texto || lastMessage;
   actualizarBurbujaGauss(lastMessage);
   mostrarBurbujaGauss(4500);

   if (!vozActivada || !('speechSynthesis' in window)) return;

  window.speechSynthesis.cancel();
  await new Promise(r => setTimeout(r, 80));

  const msg = new SpeechSynthesisUtterance(texto);
  msg.lang  = vozGauss?.lang || "es-ES";
  msg.rate  = 1.0;
  msg.pitch = 1.5;
  msg.volume = 1;

  if (vozGauss) msg.voice = vozGauss;

  activarHabla();
  actualizarEstadoVoz('activa', 'Gauss está hablando...');

  if (watchdogTimer) clearTimeout(watchdogTimer);
  watchdogTimer = setTimeout(() => {
   desactivarHabla();
   actualizarEstadoVoz('activa', 'Voz lista');
   if (resumeInterval) clearInterval(resumeInterval);
  }, 8000);

  if (resumeInterval) clearInterval(resumeInterval);
  resumeInterval = setInterval(() => {
   if (window.speechSynthesis.paused) {
    window.speechSynthesis.resume();
   }
  }, 1000);

  msg.onend = () => {
   clearTimeout(watchdogTimer);
   clearInterval(resumeInterval);
   desactivarHabla();
   actualizarEstadoVoz('activa', 'Voz lista');
  };

  msg.onerror = (e) => {
   clearTimeout(watchdogTimer);
   clearInterval(resumeInterval);
   desactivarHabla();

   if (e.error !== 'interrupted' && e.error !== 'canceled') {
    actualizarEstadoVoz('inactiva', 'Error de voz intenta de nuevo');
   }
  };

  window.speechSynthesis.speak(msg);
 }

 /* 
   SPLASH arranque automático al cerrar
  */
 function arrancarDesdeGesto() {
  vozActivada = true;

  // ACTIVAR MSICA DE FONDO
  iniciarMusica();

  if ('speechSynthesis' in window) {
   const silencio = new SpeechSynthesisUtterance(" ");
   silencio.volume = 0;
   window.speechSynthesis.speak(silencio);

   if (!vocesListas) cargarVoces();
   actualizarEstadoVoz('activa', 'Voz lista');
  }

  setTimeout(() => {
   hablar(mensajes.inicio, document.querySelector(".general-box"));
  }, 300);
 }

 const splash = document.getElementById('splash');
 const splashBtn = document.querySelector('#splash .splash-btn');

 function cerrarSplashObjetivos() {
  if (!splash) return;
  splash.classList.add('salir');
  setTimeout(() => splash.remove(), 460);
  arrancarDesdeGesto();
 }

 if (splash) {
  splash.addEventListener('click', cerrarSplashObjetivos);
 }

 if (splashBtn) {
  splashBtn.addEventListener('click', (event) => {
   event.preventDefault();
   event.stopPropagation();
   cerrarSplashObjetivos();
  });
 }

 /* 
   OBSERVER hablar al aparecer cada sección
  */
 const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
   if (!entry.isIntersecting || !vozActivada) return;

   const texto = entry.target.innerText.toLowerCase();

   if (texto.includes("matemáticas divertidas tercer grado")) {
    hablar(mensajes.general, entry.target);
   } else if (texto.includes("informar")) {
    hablar(mensajes.especifico1, entry.target);
   } else if (texto.includes("guiar la práctica")) {
    hablar(mensajes.especifico2, entry.target);
   } else if (texto.includes("motivar mediante juegos")) {
    hablar(mensajes.especifico3, entry.target);
   }
  });
 }, { threshold: 0.65 });

 document.querySelectorAll(".general-box, .specific-item").forEach(el => observer.observe(el));

 /* 
   BOTN COMENZAR
  */
 const btnComenzar = document.getElementById('btnComenzar');
 if (btnComenzar) {
  btnComenzar.addEventListener('click', () => {
   hablar("¡Vamos a comenzar la aventura!", btnComenzar);

   setTimeout(() => {
    try {
     window.location.href = "../../Inicio_Retorno.html";
    } catch (e) {
     console.warn("No se encontró la ruta de navegación:", e);
    }
   }, 1500);
  });
 }
