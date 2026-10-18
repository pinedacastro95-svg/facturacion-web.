from pathlib import Path
import re

p = Path("src/App.jsx")
s = p.read_text()

if "from 'jspdf'" not in s:
    s = s.replace(
        "import React, { useEffect, useMemo, useState } from 'react';",
        "import React, { useEffect, useMemo, useState } from 'react';\nimport { jsPDF } from 'jspdf';",
        1
    )

helpers = '''
function makeInvoicePdf(i) {
  const pdf = new jsPDF();
  const paid = (i.payments || []).reduce((s,p) => s + Number(p.amount || 0), 0);
  const total = Number(i.total || 0);
  pdf.setFontSize(20);
  pdf.text('FACTURA', 20, 20);
  pdf.setFontSize(12);
  const lines = [
    'Numero: ' + (i.invoice_number || i.id),
    'Fecha: ' + (i.invoice_date || ''),
    'Cliente: ' + (i.clients?.name || '—'),
    'Servicio: ' + (i.description || ''),
    'Vencimiento: ' + (i.due_date || '—'),
    'Total: ' + money(total),
    'Abonado: ' + money(paid),
    'Saldo: ' + money(Math.max(0,total-paid)),
    'Estado: ' + (total-paid <= 0 ? 'Pagada' : 'Pendiente')
  ];
  let y = 35;
  lines.forEach(line => { pdf.text(pdf.splitTextToSize(line,170),20,y); y += 10; });
  return pdf;
}
function downloadInvoicePdf(i) {
  makeInvoicePdf(i).save('Factura-' + (i.invoice_number || i.id) + '.pdf');
}
function shareInvoiceWhatsApp(i) {
  downloadInvoicePdf(i);
  const msg = 'Factura ' + (i.invoice_number || '') + ' - ' + (i.clients?.name || '');
  window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank');
  alert('PDF descargado. Adjunta el archivo de la factura en WhatsApp.');
}
function printInvoice(i) {
  const url = URL.createObjectURL(makeInvoicePdf(i).output('blob'));
  const w = window.open(url, '_blank');
  if (!w) {
    downloadInvoicePdf(i);
    alert('PDF descargado. Ábrelo y selecciona Imprimir.');
  } else {
    setTimeout(() => { try { w.print(); } catch(e) {} }, 1000);
  }
}
'''

if "function makeInvoicePdf(i)" not in s:
    s = re.sub(r'function InvoiceTable\\(', helpers + '\\nfunction InvoiceTable(', s, count=1)

start = s.find("function InvoiceTable(")
if start == -1:
    raise SystemExit("No encontre InvoiceTable. No se modifico el archivo.")

ends = [x for x in (s.find("\\nfunction ",start+1), s.find("\\nconst ",start+1), s.find("\\nexport default",start+1)) if x != -1]
end = min(ends) if ends else len(s)

table = r'''function InvoiceTable({ invoices, busy, deleteInvoice }) {
  return <div className="table-wrap"><table><thead><tr><th>Fecha</th><th>Cliente</th><th>Servicio</th><th>Tipo</th><th>Vence</th><th>Total</th><th>Abonado</th><th>Saldo</th><th>Estado</th><th>Acción</th></tr></thead><tbody>{invoices.map(i => { const paid = (i.payments || []).reduce((s,p) => s + Number(p.amount || 0), 0); const balance = Math.max(0, Number(i.total || 0) - paid); return <tr key={i.id}><td>{i.invoice_date}</td><td>{i.clients?.name || '—'}</td><td>{i.description}</td><td>{i.service_type === 'recurrente' ? `Recurrente (${i.recurrence || 'mensual'})` : 'Ocasional'}</td><td>{i.due_date || '—'}</td><td className="amount">{money(i.total)}</td><td>{money(paid)}</td><td className="amount">{money(balance)}</td><td><span className={`status ${balance <= 0 ? 'paid' : 'pending'}`}>{balance <= 0 ? 'pagada' : 'pendiente'}</span></td><td><div style={{display:'flex',gap:5,flexWrap:'wrap'}}><button type="button" className="secondary" onClick={() => downloadInvoicePdf(i)}>PDF</button><button type="button" className="secondary" onClick={() => shareInvoiceWhatsApp(i)}>WhatsApp</button><button type="button" className="secondary" onClick={() => printInvoice(i)}>Imprimir</button><button type="button" className="secondary" disabled={busy} onClick={() => deleteInvoice(i)}>Eliminar</button></div></td></tr>; })}{!invoices.length && <tr><td colSpan="10" className="empty">No hay facturas todavía.</td></tr>}</tbody></table></div>;
}
'''
s = s[:start] + table + s[end:]
p.write_text(s)
print("Cambios guardados correctamente.")
