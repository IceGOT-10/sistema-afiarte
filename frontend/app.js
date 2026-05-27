// frontend/app.js

const API_URL = 'http://127.0.0.1:8000';

// Estado global do aplicativo
let produtosCatalogo = [];
let carrinho = [];

// Formataadora de moeda (BRL)
const formatarMoeda = (valor) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
};

// Navegação entre abas
function mudarAba(abaId) {
    // Atualiza visual dos botões do menu
    const botoes = document.querySelectorAll('aside nav button');
    botoes.forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white');
        btn.classList.add('text-slate-300', 'hover:bg-slate-800');
    });
    event.currentTarget.classList.remove('text-slate-300', 'hover:bg-slate-800');
    event.currentTarget.classList.add('bg-blue-600', 'text-white');

    // Oculta todas as telas e mostra a selecionada
    document.getElementById('tela-pdv').classList.add('hidden');
    document.getElementById('tela-financeiro').classList.add('hidden');
    document.getElementById('tela-produtos').classList.add('hidden');
    
    document.getElementById(`tela-${abaId}`).classList.remove('hidden');

    // Atualiza o título
    const titulos = {
        'pdv': 'Ponto de Venda',
        'financeiro': 'Controle Financeiro',
        'produtos': 'Gestão de Serviços'
    };
    document.getElementById('titulo-aba').innerText = titulos[abaId];
}

// Busca os produtos na API
async function carregarProdutos() {
    try {
        const response = await fetch(`${API_URL}/produtos/?apenas_ativos=true`);
        if (!response.ok) throw new Error('Falha ao carregar produtos');
        
        produtosCatalogo = await response.json();
        renderizarGridProdutos();
    } catch (error) {
        console.error(error);
        document.getElementById('grid-produtos').innerHTML = `
            <div class="col-span-full text-red-500 text-center py-4">
                Erro ao conectar com a API. O servidor Python (uvicorn) está rodando?
            </div>
        `;
    }
}

// Desenha os botões de serviço na tela
function renderizarGridProdutos() {
    const grid = document.getElementById('grid-produtos');
    grid.innerHTML = '';

    produtosCatalogo.forEach(produto => {
        // Define uma cor sutil baseada na categoria para facilitar identificação visual
        const corBorda = produto.categoria === 'Afiação' ? 'border-blue-200' : 'border-emerald-200';
        
        const btn = document.createElement('button');
        btn.className = `flex flex-col items-center justify-center p-3 bg-white border ${corBorda} rounded-lg hover:shadow-md hover:border-blue-400 transition-all text-left active:scale-95`;
        btn.onclick = () => adicionarAoCarrinho(produto);
        
        btn.innerHTML = `
            <span class="text-sm font-medium text-gray-800 w-full truncate text-center" title="${produto.nome}">${produto.nome}</span>
            <span class="text-xs text-gray-400 mt-1">${produto.categoria}</span>
            <span class="text-green-600 font-bold mt-2">${formatarMoeda(produto.valor_padrao)}</span>
        `;
        grid.appendChild(btn);
    });
}

// ... (mantenha a parte de cima do app.js igualzinho, até o renderizarGridProdutos) ...

// ==========================================
// LÓGICA DO CARRINHO E PDV
// ==========================================

function adicionarAoCarrinho(produto) {
    // 1. Verifica se o produto já está no carrinho
    const itemExistente = carrinho.find(item => item.produto.id === produto.id);

    if (itemExistente) {
        // Se já tem, só aumenta a quantidade
        itemExistente.quantidade += 1;
    } else {
        // Se não tem, adiciona um novo registro
        carrinho.push({
            produto: produto,
            quantidade: 1,
            valor_unitario: produto.valor_padrao
        });
    }
    
    // Atualiza a tela
    renderizarCarrinho();
}

function removerDoCarrinho(index) {
    // Diminui a quantidade. Se chegar a zero, remove do vetor
    carrinho[index].quantidade -= 1;
    if (carrinho[index].quantidade <= 0) {
        carrinho.splice(index, 1);
    }
    renderizarCarrinho();
}

function renderizarCarrinho() {
    const lista = document.getElementById('lista-carrinho');
    const elementoTotal = document.getElementById('valor-total-carrinho');
    
    lista.innerHTML = '';
    let total = 0;

    // Se estiver vazio, mostra mensagem padrão
    if (carrinho.length === 0) {
        lista.innerHTML = `
            <div class="text-center text-gray-400 text-sm mt-10">
                Nenhum item adicionado.<br>Clique nos serviços ao lado.
            </div>`;
        elementoTotal.innerText = formatarMoeda(0);
        return;
    }

    // Desenha cada item na tela
    carrinho.forEach((item, index) => {
        const subtotal = item.quantidade * item.valor_unitario;
        total += subtotal;

        const div = document.createElement('div');
        div.className = 'flex justify-between items-center border-b border-gray-100 pb-2 mb-2';
        div.innerHTML = `
            <div class="flex-1">
                <p class="text-sm font-medium text-gray-800">${item.produto.nome}</p>
                <p class="text-xs text-gray-500">${item.quantidade}x ${formatarMoeda(item.valor_unitario)}</p>
            </div>
            <div class="flex items-center gap-3">
                <span class="font-semibold text-gray-700">${formatarMoeda(subtotal)}</span>
                <button onclick="removerDoCarrinho(${index})" class="text-red-400 hover:text-red-600 p-1 transition-colors" title="Remover item">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        `;
        lista.appendChild(div);
    });

    // Atualiza o valor totalzão da compra
    elementoTotal.innerText = formatarMoeda(total);
}

// ==========================================
// FINALIZAÇÃO DE VENDA (POST PARA API)
// ==========================================

async function finalizarVenda() {
    if (carrinho.length === 0) {
        alert('Adicione pelo menos um item ao carrinho antes de finalizar a venda.');
        return;
    }

    const formaPagamento = document.getElementById('forma-pagamento').value;
    const botaoFinalizar = document.querySelector('button[onclick="finalizarVenda()"]');
    
    // Altera o visual do botão para indicar carregamento (evita cliques duplos)
    botaoFinalizar.disabled = true;
    botaoFinalizar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registrando...';
    botaoFinalizar.classList.replace('bg-green-600', 'bg-gray-400');

    // Monta o objeto (payload) exatamente como o Pydantic (schemas.VendaCreate) exige
    const payload = {
        forma_pagamento: formaPagamento,
        observacoes: "Venda rápida (PDV Web)",
        itens: carrinho.map(item => ({
            produto_servico_id: item.produto.id,
            quantidade: item.quantidade,
            valor_unitario: item.valor_unitario
        }))
    };

    try {
        // Dispara para o Backend
        const response = await fetch(`${API_URL}/vendas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.detail || 'Erro ao gravar no banco de dados');
        }

        // Se deu tudo certo
        alert('✅ Venda registrada com sucesso no caixa!');
        
        // Zera o carrinho para o próximo cliente
        carrinho = [];
        renderizarCarrinho();
        
    } catch (error) {
        console.error("Erro na venda:", error);
        alert(`❌ Ocorreu um erro: ${error.message}`);
    } finally {
        // Devolve o botão ao estado original
        botaoFinalizar.disabled = false;
        botaoFinalizar.innerHTML = '<i class="fas fa-check-circle"></i> Finalizar Venda';
        botaoFinalizar.classList.replace('bg-gray-400', 'bg-green-600');
    }
}

// Inicializa a aplicação
document.addEventListener('DOMContentLoaded', () => {
    carregarProdutos();
});