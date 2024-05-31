document.getElementById('headerCheckbox').addEventListener('click', function() {
    var isChecked = this.checked;
    var dataCheckboxes = document.querySelectorAll('input[name="dataCheckbox"]');
    dataCheckboxes.forEach(function(checkbox) {
        checkbox.checked = isChecked;
    });
});