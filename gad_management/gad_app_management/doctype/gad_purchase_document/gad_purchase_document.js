// Copyright (c) 2023, Luis Pillaga and contributors
// For license information, please see license.txt
const PARAMS_MAPPING = {
    'download_doc_1': {
        'template_field_name': 'po_template_1',
    }
}

function getQueryParamsForButton(buttonName) {
    const params = PARAMS_MAPPING[buttonName];

    if (!params) {
        frappe.ui.msgprint(`No se encontraron parámetros para el botón ${buttonName}`);
    }

    return new URLSearchParams(params);
}

function getDownloadUrlForButton(buttonName, frm) {
    const queryParams = getQueryParamsForButton(buttonName);
    queryParams.append('doc_name', frm.doc.name);
    return `/api/method/gad_management.documents.download_word?${queryParams}`;
}

function showPdfDialog(buttonName, frm) {
    const queryParams = getQueryParamsForButton(buttonName);
    queryParams.append('doc_name', frm.doc.name);
    const pdfUrl = `/api/method/gad_management.documents.download_pdf?${queryParams}`;

    const iframe = `<iframe src="${pdfUrl}" style="width: 100%; height: 500px;"></iframe>`;

    const d = new frappe.ui.Dialog({
        title: 'Ver PDF',
        size: 'large',
        primary_action_label: 'Close',
        primary_action() {
            d.hide();
        }
    });

    d.$body.html(iframe);
    d.show();
}

function downloadDocumentInNewTab(buttonName, frm) {
    window.open(getDownloadUrlForButton(buttonName, frm), '_blank');
}

frappe.ui.form.on('Gad Purchase Document', {
    view_doc_1: function (frm) {
        showPdfDialog('download_doc_1', frm);
    },
    download_doc_1: function (frm) {
        downloadDocumentInNewTab('download_doc_1', frm);
    }
});
