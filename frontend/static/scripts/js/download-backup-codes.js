function downloadCodes() {
    var _a;
    var dataElement = document.getElementById('code-data');
    if (!dataElement)
        return;
    var codes = ((_a = dataElement.getAttribute('data-codes')) === null || _a === void 0 ? void 0 : _a.split(',')) || [];
    var blob = new Blob([codes.join('\n')], { type: 'text/plain' });
    var url = window.URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = 'backup_codes.txt';
    link.click();
    window.URL.revokeObjectURL(url);
}
