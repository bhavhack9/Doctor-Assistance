$(document).ready(function () {
    let table = initializeDataTable('doctor_table');

    $('#image').change(function () {
        displayImage(this);
    });


    $('#doctorForm').submit(function (event) {
        event.preventDefault();
        // var formData = new FormData(this);
        // var checkboxValue = $('#is_active').is(':checked') ? 1 : 0;
        // formData.append('is_active', checkboxValue);
        var formData = new FormData(this);
        formData.append('is_active', 1);
        showConfirmation("Are you sure you want to add this doctor?",
            () => {
                doctor(formData);
            });
    });
});

function addEditDoctorModel(type) {
    $('#doctorForm')[0].reset();
    $('.offcanvas-title').text(`${type} Doctor`);
    var myOffcanvas = document.getElementById('offcanvasExample')
    var bsOffcanvas = new bootstrap.Offcanvas(myOffcanvas)
    bsOffcanvas.show()
}

const displayImage = (input) => {
    var previewImage = $('#previewImage')[0];

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function doctor(formData) {
    PostRequest(doctorApi, formData,
        (response) => {
            if (response.status) {
                showSuccess(response.message);
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                showError(response.message);
            }
        }, true
    );
}