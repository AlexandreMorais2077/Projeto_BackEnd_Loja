from datetime import date
from models.models import Livros, db


def _validar_dados(titulo, autor, isbn, editora, ano_publicacao, quantidade):
    """Valida e converte os dados vindos do formulário (tudo chega como texto)."""
    titulo = (titulo or "").strip()
    autor = (autor or "").strip()
    isbn = (isbn or "").strip() or None
    editora = (editora or "").strip() or None

    if not titulo or not autor:
        raise ValueError("Por favor, preencha o título e o autor.")

    ano = None
    if str(ano_publicacao or "").strip():
        try:
            ano = int(ano_publicacao)
        except ValueError:
            raise ValueError("Ano de publicação inválido.")
        if ano < 0 or ano > date.today().year:
            raise ValueError("Ano de publicação inválido.")

    try:
        qtd = int(quantidade)
    except (TypeError, ValueError):
        raise ValueError("Quantidade inválida.")
    if qtd < 0:
        raise ValueError("A quantidade não pode ser negativa.")

    return titulo, autor, isbn, editora, ano, qtd


def create_livro(titulo: str, autor: str, isbn: str, editora: str,
                 ano_publicacao, quantidade) -> Livros:
    titulo, autor, isbn, editora, ano, qtd = _validar_dados(
        titulo, autor, isbn, editora, ano_publicacao, quantidade
    )

    if isbn and get_livro_by_isbn(isbn):
        raise ValueError("ISBN já cadastrado.")

    livro = Livros(titulo=titulo, autor=autor, isbn=isbn, editora=editora,
                   ano_publicacao=ano, quantidade=qtd)
    db.session.add(livro)
    db.session.commit()
    return livro


def get_livros() -> list[Livros]:
    return db.session.query(Livros).order_by(Livros.titulo).limit(25).all()


def get_livro_by_id(livro_id: int) -> Livros:
    return db.session.query(Livros).filter_by(id=livro_id).first()


def get_livro_by_isbn(isbn: str) -> Livros:
    return db.session.query(Livros).filter_by(isbn=isbn).first()


def update_livro(livro_id: int, titulo: str, autor: str, isbn: str,
                 editora: str, ano_publicacao, quantidade) -> Livros:
    livro = get_livro_by_id(livro_id)
    if not livro:
        raise ValueError("Livro não encontrado.")

    titulo, autor, isbn, editora, ano, qtd = _validar_dados(
        titulo, autor, isbn, editora, ano_publicacao, quantidade
    )

    existing = get_livro_by_isbn(isbn) if isbn else None
    if existing and existing.id != livro_id:
        raise ValueError("ISBN já cadastrado em outro livro.")

    livro.titulo = titulo
    livro.autor = autor
    livro.isbn = isbn
    livro.editora = editora
    livro.ano_publicacao = ano
    livro.quantidade = qtd
    db.session.commit()
    return livro


def delete_livro(livro_id: int) -> None:
    livro = get_livro_by_id(livro_id)
    if not livro:
        raise ValueError("Livro não encontrado.")

    db.session.delete(livro)
    db.session.commit()
