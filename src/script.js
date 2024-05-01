function showFileTypes() {
    var fileTypesMessage = "Tipos de arquivo permitidos: PDF, DOC, DOCX";
    alert(fileTypesMessage);
}

async function handleFileSelect() {
    const nome = document.getElementById('nomeInput').value;
    const email = document.getElementById('emailInput').value;
    const matricula = document.getElementById('matriculaInput').value;
    const fileInput = document.getElementById('fileInput');

    if (fileInput.files.length === 0) {
        alert('Selecione um arquivo para upload.');
        return;
    }

    const file = fileInput.files[0];

    try {
        const preSignedUrl = await getPreSignedUrl(file, nome, email, matricula);
        await uploadFileToS3(file, preSignedUrl);
        displaySuccessMessage('Arquivo enviado com sucesso!');
    } catch (error) {
        displayErrorMessage('Falha ao enviar o arquivo.', error);
        console.error(error);
    }
}

async function getPreSignedUrl(file, nome, email, matricula) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('nome', nome);
    formData.append('email', email);
    formData.append('matricula', matricula);

    const response = await fetch('https://pw2ocxrucg.execute-api.us-east-1.amazonaws.com', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    if (!data.preSignedUrl) {
        throw new Error('Falha ao obter URL pré-assinada.');
