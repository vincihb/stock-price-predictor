(function() {
    window.addEventListener('load', () => {
        window.document.querySelectorAll('button.gen-report').forEach((el) => {
            el.addEventListener('click', (e) => {
                const button = e.target;
                const reportType = button.getAttribute('data-type');

                request('/report', { report_type: reportType }, (data) => {
                    window.location.href = data.report_title
                }, console.error);
            });
        });
    });
})();