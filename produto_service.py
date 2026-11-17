from flask import flash
from models.models import Produtos, db

def create_produto(nome: str, descricao: str, preco: float, quantia: int) -> Produtos:
    if not nome or not descricao or not preco or not quantia:
        raise ValueError("Por favor, preencha todos os campos.")
    
    
    produto = Produtos(nome=nome, descricao=descricao, preco=preco, quantia=quantia)
    db.session.add(produto)
    db.session.commit()
    return produto

def get_produto() -> list[Produtos]:
    return db.session.query(Produtos).limit(25).all()

def get_produto_by_id(produto_id: int) -> Produtos:
    return db.session.query(Produtos).filter_by(id=produto_id).first()

def get_produto_by_nome(nome: str) -> Produtos:
    return db.session.query(Produtos).filter_by(nomme=nome).first()

def update_produto(produto_id: int, nome: str, descricao: str, preco: float, quantia: int) -> Produtos:
    produto = get_produto_by_id(produto_id)
    if not produto:
        raise ValueError("Produto não encontrado.")
    
    if not nome or not preco or not quantia:
        raise ValueError("Por favor, preencha todos os campos.")
    
    
    produto.nome = nome
    produto.descricao = descricao
    produto.preco = preco
    produto.quantia = quantia
    db.session.commit()
    return produto, flash("Dados atualizados com sucesso!", "success")

def delete_produto(produto_id: int) -> None:
    produto = get_produto_by_id(produto_id)
    if not produto:
        raise ValueError("Produto não encontrado.")
    
    db.session.delete(produto)
    db.session.commit()

