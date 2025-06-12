document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            if (!valid) {
                e.preventDefault();
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger alert-dismissible fade show mt-3';
                alert.innerHTML = 'Por favor, preencha todos os campos obrigatórios.<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
                form.prepend(alert);
                setTimeout(() => alert.remove(), 3000);
            }
        });
    });

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('btn-success') && !this.disabled) {
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
                this.disabled = true;
                setTimeout(() => {
                    this.innerHTML = this.dataset.originalText || this.innerHTML;
                    this.disabled = false;
                }, 2000);
            }
        });
    });

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});