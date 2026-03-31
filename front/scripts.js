const API_URL = window.location.origin;

// Carrega a lista de pacientes ao abrir a pagina
document.addEventListener("DOMContentLoaded", () => {
    carregarPacientes();
});

// Submissao do formulario
document.getElementById("pacienteForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("submitBtn");
    btn.disabled = true;
    btn.textContent = "Processando...";

    const form = e.target;
    const formData = new FormData(form);

    // Monta o body como JSON
    const dados = {};
    formData.forEach((value, key) => {
        dados[key] = key === "age" ? parseInt(value) : value;
    });

    try {
        const response = await fetch(`${API_URL}/paciente`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });

        const data = await response.json();

        if (response.ok) {
            exibirResultado(data.outcome);
            carregarPacientes();
            form.reset();
        } else {
            alert(data.message || "Erro ao cadastrar paciente.");
        }
    } catch (error) {
        alert("Erro de conexao com o servidor. Verifique se a API esta rodando.");
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.textContent = "Realizar Predicao";
    }
});

// Exibe o resultado da predicao
function exibirResultado(outcome) {
    const div = document.getElementById("resultado");
    const texto = document.getElementById("resultadoTexto");

    div.classList.remove("hidden", "needs-treatment", "no-treatment");

    if (outcome === "Yes") {
        div.classList.add("needs-treatment");
        texto.textContent = "O modelo sugere que esta pessoa PODE SE BENEFICIAR de tratamento de saude mental.";
    } else {
        div.classList.add("no-treatment");
        texto.textContent = "O modelo sugere que esta pessoa NAO NECESSITA de tratamento de saude mental no momento.";
    }
}

// Carrega todos os pacientes da API
async function carregarPacientes() {
    try {
        const response = await fetch(`${API_URL}/pacientes`);
        const data = await response.json();
        const tbody = document.getElementById("pacientesBody");
        const emptyMsg = document.getElementById("emptyMsg");

        tbody.innerHTML = "";

        if (data.pacientes && data.pacientes.length > 0) {
            emptyMsg.style.display = "none";
            document.getElementById("pacientesTable").style.display = "table";

            data.pacientes.forEach((p) => {
                const tr = document.createElement("tr");
                const badgeClass = p.outcome === "Yes" ? "badge-yes" : "badge-no";
                const badgeText = p.outcome === "Yes" ? "Tratamento" : "Sem tratamento";

                tr.innerHTML = `
                    <td>${p.name}</td>
                    <td>${p.age}</td>
                    <td>${p.gender}</td>
                    <td>${p.family_history}</td>
                    <td>${p.work_interfere}</td>
                    <td><span class="${badgeClass}">${badgeText}</span></td>
                    <td><button class="btn-delete" onclick="deletarPaciente('${p.name}')">Remover</button></td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            emptyMsg.style.display = "block";
            document.getElementById("pacientesTable").style.display = "none";
        }
    } catch (error) {
        console.error("Erro ao carregar pacientes:", error);
    }
}

// Remove um paciente
async function deletarPaciente(name) {
    if (!confirm(`Deseja remover o paciente "${name}"?`)) return;

    try {
        const response = await fetch(
            `${API_URL}/paciente?name=${encodeURIComponent(name)}`,
            { method: "DELETE" }
        );

        if (response.ok) {
            carregarPacientes();
        } else {
            const data = await response.json();
            alert(data.message || "Erro ao remover paciente.");
        }
    } catch (error) {
        alert("Erro de conexao com o servidor.");
        console.error(error);
    }
}
