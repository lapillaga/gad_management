// Copyright (c) 2023, Luis Pillaga and contributors
// For license information, please see license.txt

function getDownloadUrlForButton(frm, template_field_name) {
    const queryParams = new URLSearchParams({
        'doc_name': frm.doc.name,
        'template_field_name': template_field_name,
    });
    return `/api/method/gad_management.gad_app_management.doctype.gad_payment_justification.gad_payment_justification.download_word?${queryParams}`;
}

function downloadDocumentInNewTab(frm, template_field_name) {
    window.open(getDownloadUrlForButton(frm, template_field_name), '_blank');
}

frappe.ui.form.on('Gad Payment Justification', {
    refresh: function(frm) {
        if (!frm.doc.name.includes('new')) {
            frm.add_custom_button(__('1. Disponibilidad presupuestaria'), function () {
                downloadDocumentInNewTab(frm, 'pj_template_1');
            }, __('Descargar'));
            frm.add_custom_button(__('2. Certificación presupuestaria'), function () {
                downloadDocumentInNewTab(frm, 'pj_template_2');
            }, __('Descargar'));
            frm.add_custom_button(__('3. Orden de pago'), function () {
                downloadDocumentInNewTab(frm, 'pj_template_3');
            }, __('Descargar'));
            frm.add_custom_button(__('4. Evaluación de documentos'), function () {
                downloadDocumentInNewTab(frm, 'pj_template_4');
            }, __('Descargar'));
        }
    },
});

frappe.ui.form.on('Gad Payment Justification Party', {
    parties_add(frm, cdt, cdn) {
        const spiNumber = frm.doc.spi_number;
        if (!spiNumber) {
            frappe.msgprint(__("Por favor, ingrese el número de SPI, luego elimine la fila agregada y vuelva a intentarlo."));
            return;
        }

        generateCode(frm);
    }
});


function generateCode(frm) {
    const prefix = 'GPRJ-';
    const year = new Date().getFullYear();
    const spiNumber = frm.doc.spi_number;
    const filledZerosCode = fillPrefix(spiNumber);

    const partiesNumber = frm.doc.parties.length;
    if (partiesNumber > 1) {
        frm.doc.parties.forEach(function (party, index) {
            const letter = NUMBER_MAPPING[index + 1] || 'XYZ';
            const code = `${prefix}${filledZerosCode}.${letter}-${year}`;
            frappe.model.set_value(party.doctype, party.name, 'code', code);
        });

        return;
    }

    const code = `${prefix}${filledZerosCode}-${year}`;
    const lastParty = frm.doc.parties[frm.doc.parties.length - 1];
    frappe.model.set_value(lastParty.doctype, lastParty.name, 'code', code);
}

/**
 * Fill the number with zeros to the left.
 * @param {number} number
 * @param {number} prefixZeros
 * @returns {string}
 * @example
 * fillPrefix(1, 5) // '00001'
*/
function fillPrefix(number, prefixZeros = 5) {
  const numberString = String(number);
  const numZeros = prefixZeros - numberString.length;
  const zeros = '0'.repeat(numZeros);
  return zeros + numberString;
}

const NUMBER_MAPPING = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H',
    9: 'I',
    10: 'J',
    11: 'K',
    12: 'L',
    13: 'M',
    14: 'N',
    15: 'O',
    16: 'P',
    17: 'Q',
    18: 'R',
    19: 'S',
    20: 'T',
    21: 'U',
    22: 'V',
    23: 'W',
    24: 'X',
    25: 'Y',
    26: 'Z',
};
