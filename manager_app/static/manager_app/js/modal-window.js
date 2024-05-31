// function initModalDialog(event, modal_element) {
//     /*
//         You can customize the modal layout specifing optional "data" attributes
//         in the element (either <a> or <button>) which triggered the event;
//         "modal_element" identifies the modal HTML element.

//         Sample call:

//         <a href=""
//            data-title="Set value"
//            data-subtitle="Insert the new value to be assigned to the Register"
//            data-dialog-class="modal-lg"
//            data-icon="fa-keyboard-o"
//            data-button-save-label="Save"
//            onclick="openModalDialog(event, '#modal_generic'); return false;">
//             <i class="fa fa-keyboard-o" style="pointer-events: none;"></i> Open generic modal (no contents)
//         </a>
//     */
//     var modal = $(modal_element);
//     var target = $(event.target);

//     var title = target.data('title') || '';
//     var subtitle = target.data('subtitle') || '';
//     // either "modal-lg" or "modal-sm" or nothing
//     var dialog_class = (target.data('dialog-class') || '') + ' modal-dialog';
//     var icon_class = (target.data('icon') || 'fa-laptop') + ' fa modal-icon';
//     var button_save_label = target.data('button-save-label') || 'Save changes';

//     modal.find('.modal-dialog').attr('class', dialog_class);
//     modal.find('.modal-title').text(title);
//     modal.find('.modal-subtitle').text(subtitle);
//     modal.find('.modal-header .title-wrapper i').attr('class', icon_class);
//     modal.find('.modal-footer .btn-save').text(button_save_label);
//     modal.find('.modal-body').html('');

//     // Annotate with target (just in case)
//     modal.data('target', target);

//     return modal;
// }

// function openModalDialog(event, modal_element) {
//     var modal = initModalDialog(event, modal_element);
//     modal.modal('show');
// }


// var modal = document.getElementById('modal');
// function openModal() {
    // event.preventDefault(); 
    // modal.style.display = 'block'; // Показати модальне вікно
// }
// function openModal(id) {
//     var modal = document.getElementById('modal');
//     var item = document.querySelector(`[data-id="${id}"]`);

//     var modalContent = modal.querySelector('.mw-item-detail-content');
//     modalContent.querySelector('h1').textContent = item.dataset.name;
//     modalContent.querySelector('.modal-text').innerHTML = `
//         <p>ID: ${item.dataset.id}</p>
//         <p>Model: ${item.dataset.model}</p>
//         <p>Size: ${item.dataset.size}</p>
//         <p>Color: ${item.dataset.color}</p>
//         <p>Count: ${item.dataset.count}</p>
//         <p>Manufacturer: ${item.dataset.manufacturer}</p>
//         <p>Price: £${item.dataset.price}</p>
//     `;

//     modal.style.display = 'block'; // Показати модальне вікно
// }

function openModal(event) {
event.preventDefault(); // Зупинити типову поведінку посилання
var modal = document.getElementById('modal');
var url = event.target.dataset.action; // Отримати URL для AJAX-запиту

// AJAX-запит на сервер для отримання даних
fetch(url)
    .then(response => response.text())
    .then(data => {
        // Оновлюємо вміст модального вікна з отриманими даними
        modal.querySelector('.mw-item-detail-content').innerHTML = data;
        modal.style.display = 'block'; // Показати модальне вікно
    })
    .catch(error => {
        console.error('Error:', error);
        alert('SERVER ERROR');
    });}
function closeModal() {
    var modal = document.getElementById('modal');
    modal.style.display = 'none'; // Pf,hfnb модальне вікно
}
closeModal();

// function openModalForm(event) {
// event.preventDefault(); // Зупинити типову поведінку посилання
// var modal = document.getElementById('modal-form');
// var url = event.target.dataset.action; // Отримати URL для AJAX-запиту

// // AJAX-запит на сервер для отримання даних
// fetch(url)
//     .then(response => response.text())
//     .then(data => {
//         // Оновлюємо вміст модального вікна з отриманими даними
//         modal.querySelector('.mw-form-content').innerHTML = data;
//         modal.style.display = 'block'; // Показати модальне вікно
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('SERVER ERROR');
//     });}
// function closeModalForm() {
//     modal.style.display = 'none'; // Pf,hfnb модальне вікно
// }
// closeModalForm();