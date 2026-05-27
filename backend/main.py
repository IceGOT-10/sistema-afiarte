# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
import datetime

# Importações dos seus arquivos locais
import models
import schemas
from database import engine, get_db

# Cria as tabelas automaticamente no SQLite se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Afiarte API",
    description="API de Gestão para Oficina de Afiação",
    version="1.0.0"
)

# Configuração de CORS para permitir que o Frontend comunique com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, colocaríamos a URL exata. Em dev local, "*" permite todas.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)
# ===========================

# ==========================================
# ENDPOINTS: PRODUTOS E SERVIÇOS
# ==========================================

@app.post("/produtos/", response_model=schemas.ProdutoServicoResponse, status_code=status.HTTP_201_CREATED, tags=["Produtos e Serviços"])
def criar_produto(produto: schemas.ProdutoServicoCreate, db: Session = Depends(get_db)):
    db_produto = models.ProdutoServico(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.get("/produtos/", response_model=List[schemas.ProdutoServicoResponse], tags=["Produtos e Serviços"])
def listar_produtos(skip: int = 0, limit: int = 100, apenas_ativos: bool = False, db: Session = Depends(get_db)):
    query = db.query(models.ProdutoServico)
    if apenas_ativos:
        query = query.filter(models.ProdutoServico.ativo == True)
    return query.offset(skip).limit(limit).all()

@app.get("/produtos/{produto_id}", response_model=schemas.ProdutoServicoResponse, tags=["Produtos e Serviços"])
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.ProdutoServico).filter(models.ProdutoServico.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto ou serviço não encontrado")
    return produto

@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoServicoResponse, tags=["Produtos e Serviços"])
def atualizar_produto(produto_id: int, produto_atualizado: schemas.ProdutoServicoUpdate, db: Session = Depends(get_db)):
    db_produto = db.query(models.ProdutoServico).filter(models.ProdutoServico.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto ou serviço não encontrado")
    
    update_data = produto_atualizado.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_produto, key, value)
        
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Produtos e Serviços"])
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(models.ProdutoServico).filter(models.ProdutoServico.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto ou serviço não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return None

# ==========================================
# ENDPOINTS: VENDAS E FINANCEIRO
# ==========================================

@app.post("/vendas/", response_model=schemas.VendaResponse, status_code=status.HTTP_201_CREATED, tags=["Vendas"])
def registrar_venda(venda_in: schemas.VendaCreate, db: Session = Depends(get_db)):
    # 1. Cria a venda zerada
    nova_venda = models.Venda(
        forma_pagamento=venda_in.forma_pagamento,
        observacoes=venda_in.observacoes,
        valor_total=0.0
    )
    db.add(nova_venda)
    db.flush() # Flush garante o ID da venda antes do commit

    valor_total_calculado = 0.0

    # 2. Processa cada item da venda
    for item in venda_in.itens:
        produto = db.query(models.ProdutoServico).filter(models.ProdutoServico.id == item.produto_servico_id).first()
        if not produto:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Produto/Serviço ID {item.produto_servico_id} não encontrado.")

        subtotal = item.quantidade * item.valor_unitario
        valor_total_calculado += subtotal

        novo_item = models.ItemVenda(
            venda_id=nova_venda.id,
            produto_servico_id=item.produto_servico_id,
            quantidade=item.quantidade,
            valor_unitario=item.valor_unitario,
            subtotal=subtotal
        )
        db.add(novo_item)

    # 3. Atualiza o valor total real da venda
    nova_venda.valor_total = valor_total_calculado
    db.commit()
    db.refresh(nova_venda)
    
    return nova_venda

@app.get("/vendas/", response_model=List[schemas.VendaResponse], tags=["Vendas"])
def listar_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Venda).order_by(models.Venda.data_hora.desc()).offset(skip).limit(limit).all()

@app.get("/vendas/{venda_id}", response_model=schemas.VendaResponse, tags=["Vendas"])
def buscar_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(models.Venda).filter(models.Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

# ==========================================
# ENDPOINTS: DESPESAS (SAÍDAS)
# ==========================================

@app.post("/despesas/", response_model=schemas.DespesaResponse, status_code=status.HTTP_201_CREATED, tags=["Financeiro"])
def registrar_despesa(despesa: schemas.DespesaCreate, db: Session = Depends(get_db)):
    nova_despesa = models.Despesa(**despesa.model_dump())
    db.add(nova_despesa)
    db.commit()
    db.refresh(nova_despesa)
    return nova_despesa

@app.get("/despesas/", response_model=List[schemas.DespesaResponse], tags=["Financeiro"])
def listar_despesas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Despesa).order_by(models.Despesa.data_hora.desc()).offset(skip).limit(limit).all()

@app.delete("/despesas/{despesa_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Financeiro"])
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    db.delete(despesa)
    db.commit()
    return None

# ==========================================
# ENDPOINTS: RELATÓRIOS E FLUXO DE CAIXA
# ==========================================

@app.get("/financeiro/fluxo-caixa", response_model=schemas.RelatorioFinanceiro, tags=["Relatórios"])
def relatorio_fluxo_caixa(
    data_inicio: datetime.date, 
    data_fim: datetime.date, 
    db: Session = Depends(get_db)
):
    # Converte as datas para cobrir do primeiro minuto do dia inicial até o último minuto do dia final
    inicio_dt = datetime.datetime.combine(data_inicio, datetime.time.min)
    fim_dt = datetime.datetime.combine(data_fim, datetime.time.max)

    # Soma de todas as vendas (Entradas) no período
    total_entradas = db.query(func.sum(models.Venda.valor_total)).filter(
        models.Venda.data_hora >= inicio_dt,
        models.Venda.data_hora <= fim_dt
    ).scalar() or 0.0

    # Soma de todas as despesas (Saídas) no período
    total_saidas = db.query(func.sum(models.Despesa.valor)).filter(
        models.Despesa.data_hora >= inicio_dt,
        models.Despesa.data_hora <= fim_dt
    ).scalar() or 0.0

    saldo_liquido = total_entradas - total_saidas

    return {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo_liquido": round(saldo_liquido, 2)
    }