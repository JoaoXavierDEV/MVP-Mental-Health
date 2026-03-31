const API_URL = window.location.origin;

// Mapeamento de valores internos para exibição em pt-BR
const LABELS = {
    gender: { Male: "Masculino", Female: "Feminino", Other: "Outro" },
    family_history: { Yes: "Sim", No: "Não" },
    work_interfere: {
        Never: "Nunca",
        Rarely: "Raramente",
        Sometimes: "Às vezes",
        Often: "Com frequência"
    }
};

// Carrega a lista de registros ao abrir a página
document.addEventListener("DOMContentLoaded", () => {
    carregarPacientes();
});

// Submissão do formulário
document.getElementById("pacienteForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("submitBtn");
    btn.disabled = true;
    btn.textContent = "Processando...";

    const formData = new FormData(e.target);
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
            exibirResultado(data.outcome, dados.name);
            carregarPacientes();
            e.target.reset();
            document.getElementById("resultado").scrollIntoView({ behavior: "smooth" });
        } else {
            alert(data.message || "Erro ao cadastrar registro.");
        }
    } catch (error) {
        alert("Erro de conexão com o servidor. Verifique se a API está em execução.");
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.textContent = "Realizar Predição";
    }
});

// Exibe o resultado da predição
function exibirResultado(outcome, nome) {
    const div = document.getElementById("resultado");
    const texto = document.getElementById("resultadoTexto");

    div.classList.remove("hidden", "needs-treatment", "no-treatment");

    if (outcome === "Yes") {
        div.classList.add("needs-treatment");
        texto.innerHTML = `<strong>${nome}</strong>: o modelo sugere que esta pessoa <strong>pode se beneficiar</strong> de acompanhamento ou tratamento de saúde mental.`;
    } else {
        div.classList.add("no-treatment");
        texto.innerHTML = `<strong>${nome}</strong>: o modelo sugere que esta pessoa <strong>não apresenta</strong> indicativo de necessidade de tratamento de saúde mental no momento.`;
    }
}

// Traduz valor interno para exibição amigável
function traduzir(campo, valor) {
    return LABELS[campo]?.[valor] ?? valor;
}

// Carrega todos os registros da API
async function carregarPacientes() {
    try {
        const response = await fetch(`${API_URL}/pacientes`);
        const data = await response.json();
        const tbody = document.getElementById("pacientesBody");
        const emptyMsg = document.getElementById("emptyMsg");
        const table = document.getElementById("pacientesTable");

        tbody.innerHTML = "";

        if (data.pacientes && data.pacientes.length > 0) {
            emptyMsg.style.display = "none";
            table.style.display = "table";

            data.pacientes.forEach((p) => {
                const tr = document.createElement("tr");
                const badgeClass = p.outcome === "Yes" ? "badge-yes" : "badge-no";
                const badgeText = p.outcome === "Yes" ? "Indicativo" : "Sem indicativo";

                tr.innerHTML = `
                    <td>${p.name}</td>
                    <td>${p.age} anos</td>
                    <td>${traduzir("gender", p.gender)}</td>
                    <td>${traduzir("family_history", p.family_history)}</td>
                    <td>${traduzir("work_interfere", p.work_interfere)}</td>
                    <td><span class="${badgeClass}">${badgeText}</span></td>
                    <td><button class="btn-delete" onclick="deletarPaciente('${p.name.replace(/'/g, "\\'")}')">Remover</button></td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            emptyMsg.style.display = "block";
            table.style.display = "none";
        }
    } catch (error) {
        console.error("Erro ao carregar registros:", error);
    }
}

// Remove um registro
async function deletarPaciente(nome) {
    if (!confirm(`Deseja remover o registro de "${nome}"?`)) return;

    try {
        const response = await fetch(
            `${API_URL}/paciente?name=${encodeURIComponent(nome)}`,
            { method: "DELETE" }
        );

        if (response.ok) {
            carregarPacientes();
        } else {
            const data = await response.json();
            alert(data.message || "Erro ao remover registro.");
        }
    } catch (error) {
        alert("Erro de conexão com o servidor.");
        console.error(error);
    }
}
