let nameField = $('#name');
let contactField = $('#contact');
let genderField = $('#gender');
let emailField = $('#email');
let passwordField = $('#password');
let conf_password = $('#conf_password');
let imageField = $('#image');
let addressField = $('#address');
let dobField = $('#dob');
let weightField = $('#weight');




$(document).ready(function () {
    //registration
    $('#register_form').submit(function (event) {
        event.preventDefault();
        if (validateRegister()) {
            var formData = new FormData(this);
            UserRegistration(formData);
        }
    });

    //login
    $('#login_form').submit(function (event) {
        event.preventDefault();
        if (validateLogin) {
            var formData = new FormData(this);
            UserLogin(formData);
        }
    });
    //forgot password
    $('#forgot_password_form').submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        forgotPassword(formData);
    });

});


const UserRegistration = (formData) => {
    // let formObj = Object.fromEntries(formData);
    PostRequest(registerApiUrl, formData,
        (response) => {
            console.log(response);
            if (response.status) {
                showSuccess(response.message);
                setTimeout(() => {
                    window.location.href = loginUrl;
                }, 2000);
            } else {
                showError(response.message);
            }
        }, true
    );
}

const UserLogin = (formData) => {
    let formObj = Object.fromEntries(formData);
    PostRequest(loginApiUrl, formObj,
        (response) => {
            if (response.status) {
                showSuccess(response.message);
                setTimeout(() => {
                    window.location.href = homeUrl;
                }, 2000);
            } else {
                showError(response.message);
            }
        },
    );
}

const validateRegister = () => {
    const namePattern = /^[a-zA-Z]+(?:\s+[a-zA-Z]+)*$/;
    const contactPattern = /^\d{10}$/;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (nameField.val() === '') {
        showError('Name Field is required');
        return false;
    }
    if (!namePattern.test(nameField.val())) {
        showError('Please enter a valid name');
        return false;
    }
    if (genderField.val() === '-1') {
        showError('Please select gender');
        return false;
    }
    if (dobField.val() === '') {
        showError('Date of Birth is required');
        return false;
    }
    if (weightField.val() === '') {
        showError('Weight is required');
        return false;
    }
    if (contactField.val() === '') {
        showError('Phone Number is required');
        return false;
    }
    if (!contactPattern.test(contactField.val())) {
        showError('Please enter a valid 10-digit contact number.');
        return false;
    }
    if (emailField.val() === '') {
        showError('Email ID is required');
        return false;
    }
    if (!emailPattern.test(emailField.val())) {
        showError('Please enter a valid email address.');
        return false;
    }
    if (addressField.val() === '') {
        showError('Address is required');
        return false;
    }
    if (passwordField.val() === '') {
        showError('Password is required');
        return false;
    }
    if (!passwordPattern.test(passwordField.val())) {
        showError('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.');
        return false;
    }

    // If all validations pass
    return true;
};






const validateLogin = () => {
    return true;
}


const forgotPassword = (formData) => {
    showProcessingAlert('Please wait');
    PostRequest(forgotPasswordApiUrl, formData,
        (response) => {
            if (response.status) {
                closeProcessingAlert();
                showSuccess(response.message);
                setTimeout(() => {
                    window.location.href = loginUrl;
                }, 2000);
            } else {
                showError(response.message);
            }
        },
        true
    );
}