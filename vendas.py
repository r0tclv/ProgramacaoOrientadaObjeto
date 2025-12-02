from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from datetime import datetime

# -------------------------
# CONFIGURAÇÃO DO BANCO (Singleton-like config)
# -------------------------
class DBConfig:
    _dsn = {
        "host": "localhost",
        "database": "aprendizado_postgres",
        "user": "postgres",
        "password": "3UQ14URU$$",
        "port": 5432
    }

    @classmethod
    def get_conn(cls):
        return psycopg2.connect(
            host=cls._dsn["host"],
            database=cls._dsn["database"],
            user=cls._dsn["user"],
            password=cls._dsn["password"],
            port=cls._dsn["port"]
        )


class Cliente:
    def __init__(self, id_cliente, cliente_tipo, nome, telefone, cidade, uf):
        self.id_cliente = id_cliente
        self.cliente_tipo = cliente_tipo
        self.nome = nome
        self.telefone = telefone
        self.cidade = cidade
        self.uf = uf

class Produto:
    def __init__(self, id_produto, descricao, quantidade, preco):
        self.id_produto = id_produto
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = Decimal(preco)

class ItemVenda:
    def __init__(self, id_item, id_venda, id_produto, descricao_produto, quantidade, valor_unitario, valor_total_item):
        self.id_item = id_item
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.descricao_produto = descricao_produto
        self.quantidade = quantidade
        self.valor_unitario = Decimal(valor_unitario)
        self.valor_total_item = Decimal(valor_total_item)

class Venda:
    def __init__(self, id_venda, id_cliente, nome_cliente, valor_total, data_venda):
        self.id_venda = id_venda
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.valor_total = Decimal(valor_total)
        self.data_venda = data_venda


# -------------------------
# REPOSITORIES
# -------------------------
class ClienteRepo:
    @staticmethod
    def listar():
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_cliente, cliente_tipo, nome, telefone, cidade, uf
                    FROM clientes ORDER BY id_cliente;
                """)
                rows = cur.fetchall()
                return [Cliente(*r) for r in rows]

    @staticmethod
    def buscar_por_id(id_cliente):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_cliente, cliente_tipo, nome, telefone, cidade, uf
                    FROM clientes WHERE id_cliente = %s;
                """, (id_cliente,))
                r = cur.fetchone()
                return Cliente(*r) if r else None

    @staticmethod
    def adicionar(cliente: Cliente):
        conn = DBConfig.get_conn()
        cur = conn.cursor()

        try:
            cur.execute("SELECT COALESCE(MAX(id_cliente), 0) + 1 FROM clientes")
            novo_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO clientes (id_cliente, cliente_tipo, nome, telefone, cidade, uf)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (novo_id, cliente.cliente_tipo, cliente.nome, cliente.telefone, cliente.cidade, cliente.uf))

            conn.commit()
            return novo_id

        finally:
            cur.close()
            conn.close()


class ProdutoRepo:
    @staticmethod
    def listar():
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_produto, descricao, quantidade, preco
                    FROM produtos ORDER BY id_produto;
                """)
                rows = cur.fetchall()
                return [Produto(*r) for r in rows]

    @staticmethod
    def buscar_por_id(id_produto):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_produto, descricao, quantidade, preco
                    FROM produtos WHERE id_produto = %s;
                """, (id_produto,))
                r = cur.fetchone()
                return Produto(*r) if r else None

    @staticmethod
    def atualizar_estoque(id_produto, delta_qtd):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE produtos SET quantidade = quantidade - %s WHERE id_produto = %s;
                """, (delta_qtd, id_produto))
            conn.commit()

    @staticmethod
    def ajustar_estoque(id_produto, nova_qtd):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE produtos SET quantidade = %s WHERE id_produto = %s;
                """, (nova_qtd, id_produto))
            conn.commit()

    @staticmethod
    def adicionar(produto: Produto):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO produtos (descricao, quantidade, preco)
                    VALUES (%s,%s,%s) RETURNING id_produto;
                """, (produto.descricao, produto.quantidade, str(produto.preco)))
                new_id = cur.fetchone()[0]
            conn.commit()
        return new_id


class VendaRepo:
    @staticmethod
    def listar():
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_venda, id_cliente, nome_cliente, valor_total, data_venda
                    FROM vendas ORDER BY id_venda DESC;
                """)
                rows = cur.fetchall()
                return [Venda(*r) for r in rows]

    @staticmethod
    def criar_venda(id_cliente, nome_cliente, valor_total):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO vendas (id_cliente, nome_cliente, valor_total)
                    VALUES (%s,%s,%s) RETURNING id_venda;
                """, (id_cliente, nome_cliente, str(valor_total)))
                new_id = cur.fetchone()[0]
            conn.commit()
        return new_id


class ItemVendaRepo:
    @staticmethod
    def listar():
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_item, id_venda, id_produto, descricao_produto, quantidade, valor_unitario, valor_total_item
                    FROM itens_venda ORDER BY id_item;
                """)
                rows = cur.fetchall()
                return [ItemVenda(*r) for r in rows]

    @staticmethod
    def adicionar(item: ItemVenda):
        with DBConfig.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO itens_venda (id_venda, id_produto, descricao_produto, quantidade, valor_unitario, valor_total_item)
                    VALUES (%s,%s,%s,%s,%s,%s) RETURNING id_item;
                """, (item.id_venda, item.id_produto, item.descricao_produto, item.quantidade,
                      str(item.valor_unitario), str(item.valor_total_item)))
                new_id = cur.fetchone()[0]
            conn.commit()
        return new_id


# -------------------------
# FACTORY
# -------------------------
class Factory:
    @staticmethod
    def produto_from_row(row):
        return Produto(*row)

    @staticmethod
    def cliente_from_row(row):
        return Cliente(*row)

    @staticmethod
    def venda_from_row(row):
        return Venda(*row)


# -------------------------
# STRATEGY — DESCONTO
# -------------------------
class DescontoStrategy:
    def aplicar(self, total: Decimal) -> Decimal:
        return Decimal('10.00')

class DescontoPessoaJuridica(DescontoStrategy):
    def aplicar(self, total: Decimal) -> Decimal:
        return (total * Decimal('0.05')).quantize(Decimal('0.01'))

class SemDesconto(DescontoStrategy):
    def aplicar(self, total: Decimal) -> Decimal:
        return Decimal('0.00')


# -------------------------
# POLIMORFISMO 
# -------------------------
class EstoqueOperation:
    def executar(self, produto: Produto, valor: int):
        raise NotImplementedError

class AddEstoque(EstoqueOperation):
    def executar(self, produto, valor):
        # aumenta: delta negativo do update (quantidade - delta)
        ProdutoRepo.atualizar_estoque(produto.id_produto, -valor)

class AjustarEstoque(EstoqueOperation):
    def executar(self, produto, novo_valor):
        ProdutoRepo.ajustar_estoque(produto.id_produto, novo_valor)

class ProdAddOrAdjust:
    def __init__(self, tipo):
        self.tipo = tipo

    def executar(self, produto: Produto, valor: int):
        if self.tipo == "add":
            return AddEstoque().executar(produto, valor)
        elif self.tipo == "adjust":
            return AjustarEstoque().executar(produto, valor)
        else:
            raise ValueError("Tipo inválido")


# -------------------------
# SERVICE LAYER
# -------------------------
class VendaService:
    def __init__(self):
        self.cliente_repo = ClienteRepo()
        self.produto_repo = ProdutoRepo()
        self.venda_repo = VendaRepo()
        self.item_repo = ItemVendaRepo()

    def selecionar_estrategia(self, cliente: Cliente):
        if cliente and cliente.cliente_tipo == 'J':
            return DescontoPessoaJuridica()
        return SemDesconto()

    def criar_venda_com_itens(self, id_cliente, produtos_ids: list, quantidades: list):
        cliente = self.cliente_repo.buscar_por_id(id_cliente)
        if not cliente:
            raise ValueError("Cliente inválido")

        itens_obj = []
        total = Decimal('0.00')

        for pid, qtd in zip(produtos_ids, quantidades):
            produto = self.produto_repo.buscar_por_id(pid)
            if not produto:
                raise ValueError(f"Produto {pid} não encontrado")
            if produto.quantidade < qtd:
                raise ValueError(f"Estoque insuficiente para {produto.descricao}")

            subtotal = produto.preco * Decimal(qtd)
            total += subtotal
            item = ItemVenda(None, None, produto.id_produto, produto.descricao,
                             qtd, produto.preco, subtotal)
            itens_obj.append((item, produto))

        estrategia = self.selecionar_estrategia(cliente)
        desconto = estrategia.aplicar(total)
        total_com_desconto = (total - desconto).quantize(Decimal('0.0'))

        id_venda = self.venda_repo.criar_venda(id_cliente, cliente.nome, total_com_desconto)

        for item_obj, produto in itens_obj:
            item_obj.id_venda = id_venda
            ItemVendaRepo.adicionar(item_obj)
            ProdutoRepo.atualizar_estoque(produto.id_produto, item_obj.quantidade)

        return {
            "id_venda": id_venda,
            "valor_total": str(total_com_desconto),
            "desconto": str(desconto)
        }


# -------------------------
# FLASK APP
# -------------------------
app = Flask(__name__)
app.secret_key = "SenhaTop10Segurancas"


# CLIENTES
@app.route('/')
@app.route('/clientes')
def listar_clientes():
    clientes = ClienteRepo.listar()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/add', methods=['POST'])
def adicionar_cliente():
    try:
        tipo = request.form['cliente_tipo'].upper()
        nome = request.form['nome']
        telefone = request.form.get('telefone', '')
        cidade = request.form.get('cidade', '')
        uf = request.form.get('uf', '').upper()
        c = Cliente(None, tipo, nome, telefone, cidade, uf)
        ClienteRepo.adicionar(c)
        flash("Cliente adicionado", "success")
    except Exception as e:
        flash(f"Erro: {e}", "danger")
    return redirect(url_for('listar_clientes'))

# PRODUTOS (listar, adicionar)
@app.route('/produtos')
def listar_produtos():
    produtos = ProdutoRepo.listar()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produtos/add', methods=['POST'])
def adicionar_produto():
    try:
        descricao = request.form['descricao']
        quantidade = int(request.form['quantidade'])
        preco = Decimal(request.form['preco'])
        p = Produto(None, descricao, quantidade, preco)
        ProdutoRepo.adicionar(p)
        flash("Produto adicionado", "success")
    except Exception as e:
        flash(f"Erro: {e}", "danger")
    return redirect(url_for('listar_produtos'))

#  NOVA ROTA — AJUSTAR ESTOQUE (polimorfismo)
@app.route('/produtos/ajustar', methods=['POST'])
def ajustar_estoque():
    try:
        id_produto = int(request.form['id_produto'])
        nova_qtd = int(request.form['nova_qtd'])

        produto = ProdutoRepo.buscar_por_id(id_produto)
        if not produto:
            flash("Produto não encontrado", "danger")
            return redirect(url_for('listar_produtos'))

        ProdAddOrAdjust("adjust").executar(produto, nova_qtd)

        flash(f"Estoque do produto {produto.descricao} ajustado para {nova_qtd}", "success")

    except Exception as e:
        flash(f"Erro ao ajustar estoque: {e}", "danger")

    return redirect(url_for('listar_produtos'))

# VENDAS
@app.route('/vendas')
def listar_vendas():
    vendas = VendaRepo.listar()
    return render_template('vendas.html', vendas=vendas)

@app.route('/vendas/nova', methods=['GET'])
def nova_venda_get():
    clientes = ClienteRepo.listar()
    produtos = ProdutoRepo.listar()
    return render_template('nova_venda.html', clientes=clientes, produtos=produtos)

@app.route('/vendas/nova', methods=['POST'])
def nova_venda_post():
    try:
        id_cliente = int(request.form['id_cliente'])
        produtos_ids = [int(x) for x in request.form.getlist('id_produto')]
        quantidades = [int(q) for q in request.form.getlist('quantidade')]

        service = VendaService()
        resultado = service.criar_venda_com_itens(id_cliente, produtos_ids, quantidades)

        flash(f"Venda criada (ID {resultado['id_venda']}) - Total: R$ {resultado['valor_total']} (Desconto R$ {resultado['desconto']})", "success")
    except Exception as e:
        flash(f"Erro ao criar venda: {e}", "danger")
    return redirect(url_for('listar_vendas'))

# ITENS DE VENDA
@app.route('/itens_venda')
def listar_itens():
    itens = ItemVendaRepo.listar()
    return render_template('itens_venda.html', itens=itens)

# SQL PLAYGROUND
@app.route('/sql', methods=['GET', 'POST'])
def executar_sql():
    resultado = None
    erro = None
    colunas = None
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        try:
            with DBConfig.get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    if cur.description:
                        colunas = [d[0] for d in cur.description]
                        resultado = cur.fetchall()
                    else:
                        conn.commit()
                        resultado = f"Comando executado com sucesso ({cur.rowcount} linhas afetadas)."
        except Exception as e:
            erro = str(e)
    return render_template('sql.html', query=query, resultado=resultado, erro=erro, colunas=colunas)

# RUN
if __name__ == '__main__':
    app.run(debug=True)
