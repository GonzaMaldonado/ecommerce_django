// Alert
let alertButton = document.querySelector('[close]');
let alerta = document.getElementById('alerta');

if (alertButton) {
alertButton.addEventListener('click', () => {
    alerta.classList.toggle('hidden')
})
}
