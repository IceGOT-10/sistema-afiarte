# backend/seed.py
import random
from datetime import datetime, timedelta
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

def limpar_banco(db):
    """Limpa os dados existentes para evitar duplicações ao correr o script várias vezes."""
    print("A limpar a base de dados...")
    db.query(models.ItemVenda).delete()
    db.query(models.Venda).delete()
    db.query(models.Despesa).delete()
    db.query(models.ProdutoServico).delete()
    db.commit()
    
def popular_banco():
    db = SessionLocal()
    try:
        limpar_banco(db)
        
        print("A criar Produtos e Serviços...")
        servicos_iniciais = [
            models.ProdutoServico(nome="Afiação de alicate de cutícula", categoria="Afiação", valor_padrao=15.0),
            models.ProdutoServico(nome="Venda de alicate novo", categoria="Produto", valor_padrao=45.0),
            models.ProdutoServico(nome="Afiação de tesoura", categoria="Afiação", valor_padrao=20.0),
            models.ProdutoServico(nome="Afiação de disco de corte", categoria="Afiação", valor_padrao=35.0),
            models.ProdutoServico(nome="Afiação de faca", categoria="Afiação", valor_padrao=10.0),
        ]
        db.add_all(servicos_iniciais)
        db.commit()
        
        # Obter os IDs gerados
        servicos = db.query(models.ProdutoServico).all()
        
        print("A gerar Vendas (Entradas) para os últimos 90 dias...")
        formas_pagamento = ["Pix", "Dinheiro", "Cartão", "Pix"] # Pix com mais peso
        
        hoje = datetime.utcnow()
        inicio_periodo = hoje - timedelta(days=90)
        
        # Gerar cerca de 150 vendas aleatórias
        for _ in range(150):
            dias_aleatorios = random.randint(0, 90)
            data_venda = inicio_periodo + timedelta(days=dias_aleatorios, hours=random.randint(8, 18), minutes=random.randint(0, 59))
            
            nova_venda = models.Venda(
                data_hora=data_venda,
                forma_pagamento=random.choice(formas_pagamento),
                valor_total=0.0
            )
            db.add(nova_venda)
            db.flush()
            
            valor_total_venda = 0.0
            
            # Adicionar 1 a 3 itens por venda
            num_itens = random.randint(1, 3)
            servicos_escolhidos = random.sample(servicos, num_itens)
            
            for servico in servicos_escolhidos:
                quantidade = random.randint(1, 4) if servico.categoria == "Afiação" else 1
                subtotal = quantidade * servico.valor_padrao
                valor_total_venda += subtotal
                
                item = models.ItemVenda(
                    venda_id=nova_venda.id,
                    produto_servico_id=servico.id,
                    quantidade=quantidade,
                    valor_unitario=servico.valor_padrao,
                    subtotal=subtotal
                )
                db.add(item)
                
            nova_venda.valor_total = valor_total_venda
            
        print("A gerar Despesas (Saídas) para os últimos 90 dias...")
        despesas_tipicas = [
            {"descricao": "Conta de Energia", "categoria": "Custo Fixo", "valor_base": 120.0},
            {"descricao": "Compra de rebolos e lixas", "categoria": "Insumos", "valor_base": 250.0},
            {"descricao": "Manutenção da máquina", "categoria": "Manutenção", "valor_base": 180.0},
            {"descricao": "Material de limpeza", "categoria": "Insumos", "valor_base": 45.0},
        ]
        
        # Gerar cerca de 15 despesas aleatórias
        for _ in range(15):
            dias_aleatorios = random.randint(0, 90)
            data_despesa = inicio_periodo + timedelta(days=dias_aleatorios)
            despesa_escolhida = random.choice(despesas_tipicas)
            
            # Variar o valor em +/- 20%
            variacao = despesa_escolhida["valor_base"] * random.uniform(0.8, 1.2)
            
            nova_despesa = models.Despesa(
                data_hora=data_despesa,
                descricao=despesa_escolhida["descricao"],
                categoria=despesa_escolhida["categoria"],
                valor=round(variacao, 2)
            )
            db.add(nova_despesa)
            
        db.commit()
        print("Sucesso! Base de dados populada com dados de teste.")

    except Exception as e:
        db.rollback()
        print(f"Erro ao popular base de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()