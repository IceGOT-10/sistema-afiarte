from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class ProdutoServico(Base):
    __tablename__ = "produtos_servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    categoria = Column(String, index=True, nullable=False)
    descricao = Column(Text, nullable=True)
    valor_padrao = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    valor_total = Column(Float, default=0.0, nullable=False)
    forma_pagamento = Column(String, nullable=False) # Ex: Pix, Dinheiro, Cartão
    observacoes = Column(Text, nullable=True)

    # Relacionamento com os itens que compõem essa venda
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id", ondelete="CASCADE"), nullable=False)
    produto_servico_id = Column(Integer, ForeignKey("produtos_servicos.id"), nullable=False)
    quantidade = Column(Integer, default=1, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto_servico = relationship("ProdutoServico")

class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    descricao = Column(String, nullable=False) # Ex: Compra de rebolo
    categoria = Column(String, nullable=False) # Ex: Insumos, Energia, Ferramentas
    valor = Column(Float, nullable=False)
    observacoes = Column(Text, nullable=True)
    