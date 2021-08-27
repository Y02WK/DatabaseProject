// Switches corresponding navbar section to active
(function activeNavbar() {
    let navbar = document.getElementById('classes');
    navbar.classList.add('active');
})();

function updateClassForm(clicked) {
    // Check if updateForm exists and removes existing form if found
    let existForm = document.getElementById('updateForm')
    if ( existForm != null) {
        existForm.remove();
    }

    let currentRow = clicked.parentNode.parentNode;
    let insertForm = document.getElementById('insertForm');

    // Create new Form for updating Class data
    let updateForm = document.createElement('form');
    updateForm.action = '/update_class';
    updateForm.method = 'POST';
    updateForm.id = 'updateForm';

    let formField = document.createElement('fieldset');
    let updateHeader = document.createElement('p');
    updateHeader.textContent = 'Update a Class';
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
        inputField.type = 'text';
        inputField.value = currentRow.childNodes[inputNodes[i]].textContent;
        inputField.name = 'update' + inputList[i]

        // Required attribute for name
        if (i != 0) {
            inputField.required = true;
        }
        // Hidden attribute for id
        else {
            inputField.hidden = true;
        }

        formField.appendChild(inputField);
    }
    const copyFields = ['dept', 'term', 'inst']
    const labels = [' Department: ', ' Term: ', ' Instructor: ']
    const fieldContent = [5, 7, 9]
    for (let i = 0; i < copyFields.length; i++) {
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
    // let selectDept = document.getElementById('dept')
    // let updateDept = selectDept.cloneNode(true);
    // updateDept.name = 'updateDept';
    // formField.appendChild(updateDept);

    // Create submit button
    let formSubmit = document.createElement('input')
    formSubmit.type = 'submit'
    formField.appendChild(formSubmit)
    updateForm.appendChild(formField);
    insertForm.after(updateForm);
}