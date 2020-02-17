(function() {
    'use strict';

    const DISABLED = 'disabled';

    window.addEventListener('load', () => {
        window.document.querySelectorAll('button.gen-report').forEach((el) => {
            el.addEventListener('click', (e) => {
                const button = e.target;

                // if the button is disabled, bail
                if (button.getAttribute(DISABLED) === DISABLED)
                    return;

                const reportType = button.getAttribute('data-type');

                button.setAttribute(DISABLED, DISABLED);
                request('/report', { report_type: reportType }, (data) => {
                    if (data.report_title)
                        window.location.href = data.report_title;
                    // else
                    //      otherwise show an error message

                    button.setAttribute(DISABLED, '');
                }, (e) => {
                    button.setAttribute(DISABLED, '');
                    console.error(e);
                });
            });
        });
    });
})();