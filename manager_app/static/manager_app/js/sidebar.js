// const btn = document.getElementById('btn_burger');
// const sidebar = document.getElementById('aside');
// document.addEventListener("DOMContentLoaded", function() {
//     sidebar.classList.toggle('active');
// })
// btn.onclick = function() {
//     sidebar.classList.toggle('active');
//   }; 
const btn = document.getElementById('btn_burger');
const sidebar = document.getElementById('aside');

// Змінюємо клас "active" при кліку на кнопку
btn.onclick = function() {
  sidebar.classList.toggle('active');

  // Перевіряємо, чи є бічна панель активною і змінюємо значок кнопки
  if (sidebar.classList.contains('active')) {
    // Якщо бічна панель активна, змінюємо значок на "xmark"
    btn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
  } else {
    // Якщо бічна панель не активна, змінюємо значок на "bars"
    btn.innerHTML = '<i class="fa-solid fa-bars"></i>';
  }
};

// Змінюємо клас "active" при наведенні курсора на меню
// sidebar.addEventListener("mouseenter", function() {
//   sidebar.classList.add('active');
// });

// Змінюємо клас "active" при відведенні курсора від меню
// sidebar.addEventListener("mouseleave", function() {
//   sidebar.classList.remove('active');
// });

