document.addEventListener("DOMContentLoaded", () => {
  const taskSelect = document.querySelector("#task_id");
  const amountInput = document.querySelector("#amount");
  const amountHidden = document.querySelector("#amount_hidden");

  if (taskSelect && amountInput && amountHidden) {
    taskSelect.addEventListener("change", () => {
      const opt = taskSelect.options[taskSelect.selectedIndex];
      const val = parseFloat(opt.dataset.amount || 0);

      amountInput.value = `R$ ${val.toFixed(2)}`;
      amountHidden.value = val;
    });
  }

  document.querySelectorAll("[data-confirm]").forEach((el) => {
    el.addEventListener("click", (e) => {
      if (!confirm(el.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  let currentForm = null;
  const confirmModal = document.getElementById("confirm-modal");
  const modalContent = document.querySelector(".modal-content");

  document.querySelectorAll(".confirm-remove").forEach((btn) => {
    btn.addEventListener("click", () => {
      currentForm = btn.closest("form");
      const taskName = btn.dataset.task;

      if (!confirmModal || !modalContent) {
        return;
      }

      modalContent.innerHTML = `
        <h3>Confirmar remoção</h3>
        <p>Tem certeza que deseja remover esta tarefa?</p>
        <span class="modal-highlight">"${taskName}"</span>
        <p style="margin-top: 16px; font-size: 13px;">Esta ação não pode ser desfeita.</p>
        <div class="modal-actions">
          <button id="cancel-btn" class="btn subtle">Cancelar</button>
          <button id="confirm-btn" class="btn danger">Remover</button>
        </div>
      `;

      confirmModal.classList.remove("hidden");

      document.getElementById("cancel-btn").onclick = () => {
        currentForm = null;
        confirmModal.classList.add("hidden");
      };

      document.getElementById("confirm-btn").onclick = () => {
        if (currentForm) {
          currentForm.submit();
        }
      };
    });
  });

  document.querySelectorAll(".open-reject-modal").forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      const taskName = btn.dataset.task;

      if (!confirmModal || !modalContent || !action) {
        return;
      }

      modalContent.innerHTML = `
        <h3>Informar motivo da reprovação</h3>
        <p>Explique por que a tarefa abaixo foi reprovada.</p>
        <span class="modal-highlight">"${taskName}"</span>
        <form id="reject-form" class="form" method="post" action="${action}">
          <input
            type="text"
            name="rejection_reason"
            placeholder="Ex.: a tarefa não foi concluída"
            required
            autofocus
          >
          <div class="modal-actions">
            <button type="button" id="cancel-btn" class="btn subtle">Cancelar</button>
            <button type="submit" class="btn danger">Confirmar reprovação</button>
          </div>
        </form>
      `;

      confirmModal.classList.remove("hidden");

      document.getElementById("cancel-btn").onclick = () => {
        confirmModal.classList.add("hidden");
      };
    });
  });

  confirmModal?.addEventListener("click", (e) => {
    if (e.target.id === "confirm-modal") {
      currentForm = null;
      confirmModal.classList.add("hidden");
    }
  });

  document.querySelectorAll(".password-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const wrapper = button.closest(".password-field");
      const input = wrapper?.querySelector(".password-input");

      if (!input) {
        return;
      }

      const nextType = input.type === "password" ? "text" : "password";
      input.type = nextType;
      button.textContent = nextType === "password" ? "Mostrar" : "Ocultar";
    });
  });
});
