document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('id_image');
    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (!file) return;

            const fileNameElement = document.querySelector('.file-name');
            if (fileNameElement) {
                fileNameElement.textContent = file.name;
            }

            if (file.type.match('image.*')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const previewElement = document.getElementById('image-preview');
                    if (previewElement) {
                        previewElement.src = e.target.result;
                        previewElement.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});