function getDownloadUrlForButton(frm) {
    const queryParams = new URLSearchParams({
        'doc_name': frm.doc.name,
    });
    return `/api/method/gad_management.gad_app_management.doctype.gad_memo.gad_memo.download_word?${queryParams}`;
}

function downloadDocumentInNewTab(frm) {
    window.open(getDownloadUrlForButton(frm), '_blank');
}

frappe.ui.form.on('Gad Memo', {
    refresh: function(frm) {
        if (!frm.doc.name.includes('new')) {
            frm.add_custom_button(__('Word'), function () {
                downloadDocumentInNewTab(frm);
            }, __('Descargar'));
        }
    },
    template: function(frm) {
        if (frm.doc.template) {
            frappe.model.with_doc('Gad Memo Template', frm.doc.template, function () {
                const template = frappe.model.get_doc('Gad Memo Template', frm.doc.template);
                if (!frm.doc.subject) {
                    frm.set_value('subject', template.subject);
                }

                if (!frm.doc.sender) {
                    frm.set_value('sender', template.sender);
                }

                if (!frm.doc.recipient) {
                    frm.set_value('recipient', template.recipient);
                }

                if (!frm.doc.content) {
                    frm.set_value('content', template.content);
                }

                if (template.attachments) {
                    template.attachments.forEach(function (attachment) {
                        frm.add_child('attachments', {
                            'attachment_name': attachment.attachment_name,
                        });
                        frm.refresh_field('attachments');
                    });
                }
            });
        }
    }
});