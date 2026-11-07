/**
 * Ball Without Boundaries: Sports Money DNA → Google Sheet
 *
 * Setup (5 minutes):
 * 1. Create a Google Sheet named "BWB Sports Money DNA Responses".
 * 2. Extensions → Apps Script. Paste this whole file. Save.
 * 3. Deploy → New deployment → type "Web app".
 *      Execute as: Me    ·    Who has access: Anyone
 * 4. Copy the Web app URL and paste it into SUBMIT_URL at the top of the
 *    form's <script> section (form/src/money-dna.html), then rebuild.
 *
 * Every submission adds one row. New answer fields automatically get new columns.
 */
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = JSON.parse(e.postData.contents);
  data.received_at = new Date().toISOString();

  // Flatten arrays (multi-select answers) into "a | b | c"
  Object.keys(data).forEach(function (k) {
    if (Array.isArray(data[k])) data[k] = data[k].join(" | ");
  });

  let headers = sheet.getLastRow() ? sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0] : [];
  Object.keys(data).forEach(function (k) {
    if (headers.indexOf(k) === -1) headers.push(k);
  });
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight("bold");
  sheet.appendRow(headers.map(function (h) { return data[h] !== undefined ? data[h] : ""; }));

  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
