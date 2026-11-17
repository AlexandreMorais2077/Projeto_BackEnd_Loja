from flask import Blueprint, flash, render_template, request, redirect, url_for
from services.livro_service import (create_livro, get_livros, get_livro_by_id, update_livro, delete_livro)
from .auth_decorator import login_required

livro_bp = Blueprint('livro', __name__, url_prefix='/livros', template_folder='templates')


@livro_bp.route('/')
@login_required
def listar_livros():
    livros = get_livros()
    return render_template('livros.html', livros=livros)


@livro_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_livro():
    if request.method == 'POST':
        try:
            create_livro(
                request.form['titulo'],
                request.form['autor'],
                request.form['isbn'],
                request.form['editora'],
                request.form['ano_publicacao'],
                request.form['quantidade'],
            )
            flash("Livro cadastrado com sucesso!", "success")
            return redirect(url_for('livro.listar_livros'))
        except ValueError as e:
            flash(str(e), "danger")
            # mantém o que o usuário digitou
            return render_template('cd_livros.html', livro=request.form)

    return render_template('cd_livros.html', livro={})


@livro_bp.route('/edit/<int:livro_id>', methods=['GET', 'POST'])
@login_required
def editar_livro(livro_id):
    livro = get_livro_by_id(livro_id)
    if not livro:
        flash("Livro não encontrado.", "danger")
        return redirect(url_for('livro.listar_livros'))

    if request.method == 'POST':
        try:
            update_livro(
                livro_id,
                request.form['titulo'],
                request.form['autor'],
                request.form['isbn'],
                request.form['editora'],
                request.form['ano_publicacao'],
                request.form['quantidade'],
            )
            flash("Livro atualizado com sucesso!", "success")
            return redirect(url_for('livro.listar_livros'))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template('edit_livro.html', livro=livro)


@livro_bp.route('/delete/<int:livro_id>', methods=['POST'])
@login_required
def deletar_livro(livro_id):
    try:
        delete_livro(livro_id)
        flash("Livro excluído com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('livro.listar_livros'))
