// Switches corresponding navbar section to active
(function activeNavbar() {
    let navbar = document.getElementById('instructors');
    navbar.classList.add('active');
})();

function updateInstructorForm(clicked) {
    // Check if updateForm exists and removes existing form if found
    let existForm = document.getElementById('updateForm')
    if ( existForm != null) {
        existForm.remove();
    }

    let currentRow = clicked.parentNode.parentNode;
    let insertForm = document.getElementById('insertForm');

    // Create new Form for updating Instructor data
    let updateForm = document.createElement('form');
    updateForm.action = '/update_instructor';
    updateForm.method = 'POST';
    updateForm.id = 'updateForm';

    let formField = document.createElement('fieldset');
    let updateHeader = document.createElement('p');
    updateHeader.textContent = 'Update an Instructor';
    formField.appendChild(updateHeader);

    const inputList = ['id', 'fname', 'mname', 'lname'];
    const inputLabel = [null, 'First name*: ', 'Middle name: ', 'Last name*: '];
    const inputNodes = [1, 3, 5, 7];

    // Create inputs
    for (let i = 0; i < 4; i++) {
        if (inputLabel[i] != null) {
            let formLabel = document.createElement('label');
            formLabel.for = inputList[i];
            formLabel.textContent = inputLabel[i];
            formField.appendChild(formLabel);
        }

        let inputField = document.createElement('input');
        inputField.type = 'text';
        if (currentRow.childNodes[inputNodes[i]].textContent != '-') {
            inputField.value = currentRow.childNodes[inputNodes[i]].textContent;
        }
        inputField.name = 'update' + inputList[i];

        // Required attribute for name
        if (i != 0 && i != 2) {
            inputField.required = true;
        }
        // Hidden attribute for id
        else if (i == 0) {
            inputField.hidden = true;
        }

        formField.appendChild(inputField);
    }
    const copyFields = ['dept'];
    const labels = [' Department: ']
    const fieldContent = [9];
    for (let i = 0; i < 1; i++) {
        // Create labels for select fields
        let label = document.createElement('label')
        label.for = 'update' + copyFields[i]
        label.textContent = labels[i]

        // Clone select fields
        let selectField = document.getElementById(copyFields[i])
        let updateField = selectField.cloneNode(true);
        updateField.name = 'update' + copyFields[i]

        // Selects the existing option
        updateField.childNodes.forEach(option => {
            if (option.textContent == currentRow.childNodes[fieldContent[i]].textContent) {
                option.selected = true;
                return false;
            }
        })

        formField.appendChild(label)
        formField.appendChild(updateField)
    }


    // Create submit button
    let formSubmit = document.createElement('input')
    formSubmit.type = 'submit'
    formField.appendChild(formSubmit)
    updateForm.appendChild(formField);
    insertForm.after(updateForm);
}