document.addEventListener("DOMContentLoaded", () => {

  const taskSelect = document.querySelector("#task_type");
  const amountInput = document.querySelector("#amount");

  if (taskSelect && amountInput) {
    taskSelect.addEventListener("change", () => {
      const opt = taskSelect.options[taskSelect.selectedIndex];
      const val = opt.dataset.amount || 0;
      amountInput.value = `R$ ${parseFloat(val).toFixed(2)}`;
    });
  }

  document.querySelectorAll("[data-confirm]").forEach(el => {
    el.addEventListener("click", e => {
      if (!confirm(el.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

});

document.querySelectorAll(".confirm-remove").forEach(btn => {
  btn.addEventListener("click", () => {
    currentForm = btn.closest("form");
    const taskName = btn.dataset.task;

    // Cria o conteúdo do modal dinamicamente
    const modalContent = `
      <h3>⚠️ Confirmar remoção</h3>
      <p>Tem certeza que deseja remover esta tarefa?</p>
      <span class="modal-highlight">"${taskName}"</span>
      <p style="margin-top: 16px; font-size: 13px;">Esta ação não pode ser desfeita.</p>
    `;

    document.querySelector(".modal-content").innerHTML = modalContent + `
      <div class="modal-actions">
        <button id="cancel-btn" class="btn subtle">Cancelar</button>
        <button id="confirm-btn" class="btn danger">Remover</button>
      </div>
    `;

    document.getElementById("confirm-modal").classList.remove("hidden");

    // Re-adiciona os event listeners aos novos botões
    document.getElementById("cancel-btn").onclick = () => {
      currentForm = null;
      document.getElementById("confirm-modal").classList.add("hidden");
    };

    document.getElementById("confirm-btn").onclick = () => {
      if (currentForm) {
        currentForm.submit();
      }
    };
  });
});

// Fecha modal ao clicar fora
document.getElementById("confirm-modal")?.addEventListener("click", (e) => {
  if (e.target.id === "confirm-modal") {
    currentForm = null;
    document.getElementById("confirm-modal").classList.add("hidden");
  }
});

let currentForm = null;

document.querySelectorAll(".confirm-remove").forEach(btn => {
  btn.addEventListener("click", () => {
    currentForm = btn.closest("form");

    document.getElementById("modal-text").innerText =
      `Tem certeza que deseja remover a tarefa "${btn.dataset.task}"?`;

    document.getElementById("confirm-modal").classList.remove("hidden");
  });
});

document.getElementById("cancel-btn").onclick = () => {
  currentForm = null;
  document.getElementById("confirm-modal").classList.add("hidden");
};

document.getElementById("confirm-btn").onclick = () => {
  if (currentForm) {
    currentForm.submit();
  }
};
