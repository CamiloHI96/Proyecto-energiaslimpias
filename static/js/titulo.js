// Importar el archivo JavaScript de typed.js
var script = document.createElement('script');
script.src = 'https://unpkg.com/typed.js@2.1.0/dist/typed.umd.js';

// Esperar a que se cargue typed.js antes de continuar
script.onload = function() {
  // Inicializar Typed para el título
  var typed = new Typed(".auto-type", {
    strings: ["Energia Renovable", "100% Limpia", "La Energia del Futuro"],
    cursorChar: ' /',
    startDelay: 1000,
    tySpeed: 1000,
    backSpeed: 100,
    loop: true
  });
};
document.head.appendChild(script);