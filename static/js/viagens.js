function duplaConfirmacao(botao, evento) {
    if (botao.getAttribute("data-estado") !== "pronto") {
        evento.preventDefault(); 

        const textoOriginal = botao.innerHTML;
        const corOriginal = botao.style.backgroundColor;
        const corTextOriginal = botao.style.color
        
        botao.setAttribute("data-estado", "pronto");
        botao.innerHTML = '<span class="material-symbols-outlined">warning</span>Tem certeza?';
        botao.style.backgroundColor = "#dc3545"; 
        botao.style.color = "white";

        setTimeout(() => {
            botao.setAttribute("data-estado", "");
            botao.innerHTML = textoOriginal;
            botao.style.backgroundColor = corOriginal;
            botao.style.color = corTextOriginal
        }, 4000);

        return false; 
    }
    botao.style.backgroundColor = corOriginal;
    botao.style.color = corTextOriginal
    botao.innerHTML = '<span class="material-symbols-outlined">check</span>Tentando confirmar...';
    return true; 
}