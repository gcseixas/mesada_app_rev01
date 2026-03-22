document.addEventListener("DOMContentLoaded", () => {

  const taskSelect  = document.querySelector("#task_id");      
  const amountInput = document.querySelector("#amount");
  const amountHidden = document.querySelector("#amount_hidden");

  if (taskSelect && amountInput && amountHidden) {
    taskSelect.addEventListener("change", () => {
      const opt = taskSelect.options[taskSelect.selectedIndex];
      const val = parseFloat(opt.dataset.amount || 0);

      amountInput.value  = `R$ ${val.toFixed(2)}`;
      amountHidden.value = val;
    });
  }

  document.querySelectorAll("[data-confirm]").forEach(el => {
    el.addEventListener("click", e => {
      if (!confirm(el.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  let currentForm = null;
  const confirmModal   = document.getElementById("confirm-modal");
  const modalContent   = document.querySelector(".modal-content");

  document.querySelectorAll(".confirm-remove").forEach(btn => {
    btn.addEventListener("click", () => {
      currentForm = btn.closest("form");
      const taskName = btn.dataset.task;

      modalContent.innerHTML = `
        <h3>⚠️ Confirmar remoção</h3>
        <p>Tem certeza que deseja remover esta tarefa?</p>
        <span class="modal-highlight">"${taskName}"</span>
        <p style="margin-top: 16px; font-size: 13px;">Esta ação não pode ser desfeita.</p>
        <div class="modal-actions">
          <button id="cancel-btn" class="btn subtle">Cancelar</button>
          <button id="confirm-btn" class="btn danger">Remover</button>
        </div>
      `;

      confirmModal?.classList.remove("hidden");

      document.getElementById("cancel-btn").onclick = () => {
        currentForm = null;
        confirmModal?.classList.add("hidden");
      };

      document.getElementById("confirm-btn").onclick = () => {
        if (currentForm) currentForm.submit();
      };
    });
  });

  confirmModal?.addEventListener("click", (e) => {
    if (e.target.id === "confirm-modal") {
      currentForm = null;
      confirmModal.classList.add("hidden");
    }
  });

});