// Switches corresponding navbar section to active
(function activeNavbar() {
    let navbar = document.getElementById('departments');
    navbar.classList.add('active');
})();

function updateDeptForm(clicked) {
    // Check if updateForm exists and removes existing form if found
    let existForm = document.getElementById('updateForm')
    if ( existForm != null) {
        existForm.remove();
    }

    let currentRow = clicked.parentNode.parentNode;
    let insertForm = document.getElementById('insertForm');

    // Create new Form for updating Department data
    let updateForm = document.createElement('form');
    updateForm.action = '/update_dept';
    updateForm.method = 'POST';
    updateForm.id = 'updateForm';

    let formField = document.createElement('fieldset');
    let updateHeader = document.createElement('p');
    updateHeader.textContent = 'Update a Department';
    formField.appendChild(updateHeader);

    // Create input fields for id and name
    const inputList = ['id', 'name'];
    const inputLabel = [null, 'Name*: '];
    const inputNodes = [1, 3];

    for (let i = 0; i < 2; i++) {
        if (inputLabel[i] != null) {
            let formLabel = document.createElement('label');
            formLabel.for = inputList[i];
            formLabel.textContent = inputLabel[i];
            formField.appendChild(formLabel);
        }

        let inputField = document.createElement('input')
        inputField.type = 'text'
        if (currentRow.childNodes[inputNodes[i]].textContent != '-') {
            inputField.value = currentRow.childNodes[inputNodes[i]].textContent;
        }
        inputField.name = inputList[i]
        // Required attribute for name
        if (i != 1) {
            inputField.required = true;
        }
        // Hides field for deptID
        if (i == 0) {
            inputField.hidden = true;
        }

        formField.appendChild(inputField);
    };

    // Create submit button
    let formSubmit = document.createElement('input')
    formSubmit.type = 'submit'
    formField.appendChild(formSubmit)
    updateForm.appendChild(formField);
    insertForm.after(updateForm);
}