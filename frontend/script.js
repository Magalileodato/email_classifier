// ===========================
// Listener do botão de envio
// ===========================
document.getElementById('sendButton').addEventListener('click', async () => {
    try {
        // ===========================
        // Captura o texto do input
        // ===========================
        const text = document.getElementById('emailText').value.trim();

        if (!text) {
            alert("Por favor, insira algum texto para processar.");
            return;
        }

        // ===========================
        // Define a URL do backend dinamicamente
        // ===========================
        let backendURL;
        if (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost") {
            backendURL = "http://127.0.0.1:5000/process"; // Ambiente local
        } else {
            backendURL = "https://email-classificacao.onrender.com/process"; // Produção Render
        }

        // ===========================
        // Faz a requisição POST para o backend
        // ===========================
        const response = await fetch(backendURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include", // necessário se backend usar supports_credentials
            body: JSON.stringify({ text: text })
        });

        // ===========================
        // Verifica se a resposta foi OK
        // ===========================
        if (!response.ok) {
            throw new Error(`Erro do servidor: ${response.status} ${response.statusText}`);
        }

        // ===========================
        // Converte a resposta em JSON
        // ===========================
        const data = await response.json();

        // ===========================
        // Mostra os resultados no frontend
        // ===========================
        document.getElementById('category').innerText = data.category;
        document.getElementById('response').innerText = data.suggested_response;
        document.getElementById('preprocessed').innerText = data.preprocessed || "";

    } catch (error) {
        // ===========================
        // Tratamento de erros
        // ===========================
        console.error("Erro ao processar o email:", error);
        alert("Erro ao processar o email: " + error.message);
    }
});
