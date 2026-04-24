function downloadCodes() {
    const dataElement = document.getElementById('code-data');
    if (!dataElement) return;

    const codes: string[] = dataElement.getAttribute('data-codes')?.split(',') || [];

    const blob = new Blob([codes.join('\n')], {type: 'text/plain'});
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.href = url;
    link.download = 'backup_codes.txt';
    link.click();
    
    window.URL.revokeObjectURL(url);
}