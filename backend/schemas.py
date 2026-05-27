# backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

# ==========================
# SCHEMAS DE PRODUTOS/SERVIÇOS
# ==========================
class ProdutoServicoBase(BaseModel):
    nome: str = Field(..., example="Afiação de Alicate de Cutícula")
    categoria: str = Field(..., example="Afiação")
    descricao: Optional[str] = Field(None, example="Afiação padrão com polimento")
    valor_padrao: float = Field(..., gt=0, example=15.00)
    ativo: Optional[bool] = True

class ProdutoServicoCreate(ProdutoServicoBase):
    pass

class ProdutoServicoUpdate(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    valor_padrao: Optional[float] = None
    ativo: Optional[bool] = None

class ProdutoServicoResponse(ProdutoServicoBase):
    id: int

    class Config:
        from_attributes = True

# ==========================
# SCHEMAS DE ITEM DE VENDA
# ==========================
class ItemVendaCreate(BaseModel):
    produto_servico_id: int
    quantidade: int = Field(default=1, gt=0)
    valor_unitario: float = Field(..., gt=0) 

class ItemVendaResponse(BaseModel):
    id: int
    produto_servico_id: int
    quantidade: int
    valor_unitario: float
    subtotal: float
    produto_servico: ProdutoServicoResponse 

    class Config:
        from_attributes = True

# ==========================
# SCHEMAS DE VENDA
# ==========================
class VendaCreate(BaseModel):
    forma_pagamento: str = Field(..., example="Pix")
    observacoes: Optional[str] = None
    itens: List[ItemVendaCreate] = Field(..., min_length=1)

class VendaResponse(BaseModel):
    id: int
    data_hora: datetime.datetime
    valor_total: float
    forma_pagamento: str
    observacoes: Optional[str]
    itens: List[ItemVendaResponse]

    class Config:
        from_attributes = True
# ==========================
# SCHEMAS DE DESPESAS (SAÍDAS)
# ==========================
class DespesaBase(BaseModel):
    descricao: str = Field(..., example="Conta de Energia")
    categoria: str = Field(..., example="Custo Fixo")
    valor: float = Field(..., gt=0, example=150.50)
    observacoes: Optional[str] = None

class DespesaCreate(DespesaBase):
    pass

class DespesaResponse(DespesaBase):
    id: int
    data_hora: datetime.datetime

    class Config:
        from_attributes = True

# ==========================
# SCHEMAS DE RELATÓRIOS
# ==========================
class RelatorioFinanceiro(BaseModel):
    data_inicio: datetime.date
    data_fim: datetime.date
    total_entradas: float
    total_saidas: float
    saldo_liquido: float