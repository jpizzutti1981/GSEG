document.addEventListener("DOMContentLoaded", function () {
    // 🔹 Remove completamente a seção "Ações Recentes"
    let recentActions = document.querySelector("div.recent-actions");
    if (recentActions) {
        recentActions.remove();
    }

    // 🔹 Remove a versão do Jazzmin do rodapé
    let jazzminVersion = document.querySelector("div.jazzmin-version");
    if (jazzminVersion) {
        jazzminVersion.remove();
    }

    // 🔹 Oculta possíveis divs indesejadas
    let alertMessages = document.querySelectorAll("div.alert");
    alertMessages.forEach(alert => alert.remove());
});
