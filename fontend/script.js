// ==========================================
// Frontend para envio de texto ou arquivo ao backend Flask
// Funciona localmente (localhost) e no Render (URL pública)
// ==========================================

// Variável que irá armazenar a URL do backend
let BACKEND_URL;

// ================================
// 1️⃣ Detecta ambiente e define URL do backend
// ================================
if (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost") {
    BACKEND_URL = "http://127.0.0.1:5000"; // backend local Flask
    console.log("Frontend em localhost → usando backend local:", BACKEND_URL);
} else {
    BACKEND_URL = "https://classificador-de-email.onrender.com"; // backend Render
    console.log("Frontend em produção → usando backend Render:", BACKEND_URL);
}

// ================================
// 2️⃣ Seleciona o botão de envio e adiciona evento de clique
// ================================
document.getElementById('submitBtn').addEventListener('click', async () => {
    try {
        // Captura os dados do usuário
        const emailText = document.getElementById('emailText').value;
        const emailFile = document.getElementById('emailFile').files[0];
        let response;

        // Caso 1: texto digitado
        if (emailText) {
            console.log("Enviando texto para:", BACKEND_URL + "/process");
            response = await fetch(`${BACKEND_URL}/process`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: emailText })
            });

        // Caso 2: arquivo enviado
        } else if (emailFile) {
            console.log("Enviando arquivo para:", BACKEND_URL + "/process-file");
            const formData = new FormData();
            formData.append('file', emailFile);

            response = await fetch(`${BACKEND_URL}/process-file`, {
                method: 'POST',
                body: formData
            });

        } else {
            alert("Por favor, insira o texto ou envie um arquivo.");
            return;
        }

        // Checa se o backend retornou erro
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Erro desconhecido do backend.");
        }

        const data = await response.json();

        // Mostra os resultados
        document.getElementById('category').innerText = data.category;
        document.getElementById('response').innerText = data.suggested_response;

    } catch (error) {
        console.error("Erro ao processar o email:", error);
        alert("Erro ao processar o email: " + error);
    }
});
