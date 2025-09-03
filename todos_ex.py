import pymysql

# Conexão padrão
def conectar():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='sistema_escolar',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# ==========================
# Exercício 1 - Consulta Básica
# ==========================
def listar_disciplinas():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT d.disciplina_id,
                   d.nome_disciplina,
                   d.carga_horaria,
                   COUNT(m.aluno_id) AS num_alunos
            FROM disciplinas d
            LEFT JOIN turmas t ON d.disciplina_id = t.disciplina_id
            LEFT JOIN matriculas m ON t.turma_id = m.turma_id
            GROUP BY d.disciplina_id, d.nome_disciplina, d.carga_horaria
            ORDER BY d.nome_disciplina;
        """
        cursor.execute(sql)
        disciplinas = cursor.fetchall()
        print("\n--- Disciplinas ---")
        for d in disciplinas:
            print(f"ID: {d['disciplina_id']} | Nome: {d['nome_disciplina']} | "
                  f"Carga: {d['carga_horaria']}h | Alunos: {d['num_alunos']}")
    conexao.close()

# ==========================
# Exercício 2 - Relatório de Turmas
# ==========================
def relatorio_turmas():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT t.turma_id, d.nome_disciplina, p.nome AS professor,
                   CONCAT(t.semestre, '/', t.ano) AS periodo,
                   COUNT(m.aluno_id) AS num_alunos,
                   ROUND(AVG(n.nota), 2) AS media_turma
            FROM turmas t
            JOIN disciplinas d ON t.disciplina_id = d.disciplina_id
            JOIN professores p ON t.professor_id = p.professor_id
            LEFT JOIN matriculas m ON t.turma_id = m.turma_id
            LEFT JOIN notas n ON m.matricula_id = n.matricula_id
            GROUP BY t.turma_id, d.nome_disciplina, p.nome, periodo
            ORDER BY periodo DESC;
        """
        cursor.execute(sql)
        turmas = cursor.fetchall()
        print("\n--- Relatório de Turmas ---")
        for t in turmas:
            print(f"Turma: {t['turma_id']} | Disciplina: {t['nome_disciplina']} | Prof: {t['professor']} | "
                  f"Semestre: {t['periodo']} | Alunos: {t['num_alunos']} | Média: {t['media_turma']}")
    conexao.close()

# ==========================
# Exercício 3 - Sistema de Busca
# ==========================
def buscar_alunos(nome=None, email=None, status=None, curso=None):
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT a.aluno_id, a.nome, a.email, a.status_aluno, c.nome_curso
            FROM alunos a
            JOIN cursos c ON a.curso_id = c.curso_id
            WHERE 1=1
        """
        valores = []
        if nome:
            sql += " AND a.nome LIKE %s"
            valores.append(f"%{nome}%")
        if email:
            sql += " AND a.email = %s"
            valores.append(email)
        if status:
            sql += " AND a.status_aluno = %s"
            valores.append(status)
        if curso:
            sql += " AND c.nome_curso LIKE %s"
            valores.append(f"%{curso}%")

        cursor.execute(sql, valores)
        alunos = cursor.fetchall()
        print("\n--- Busca de Alunos ---")
        for a in alunos:
            print(f"ID: {a['aluno_id']} | Nome: {a['nome']} | Email: {a['email']} | "
                  f"Status: {a['status_aluno']} | Curso: {a['nome_curso']}")
    conexao.close()

# ==========================
# Exercício 4 - Análise de Performance
# ==========================
def alunos_com_media_alta():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT a.aluno_id, a.nome, ROUND(AVG(n.nota), 2) AS media
            FROM alunos a
            JOIN matriculas m ON a.aluno_id = m.aluno_id
            JOIN notas n ON m.matricula_id = n.matricula_id
            GROUP BY a.aluno_id, a.nome
            HAVING AVG(n.nota) > 8.0
            ORDER BY media DESC;
        """
        cursor.execute(sql)
        alunos = cursor.fetchall()
        print("\n--- Alunos com média > 8.0 ---")
        for a in alunos:
            print(f"ID: {a['aluno_id']} | Nome: {a['nome']} | Média: {a['media']}")
    conexao.close()

def disciplinas_com_reprovacao():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT d.nome_disciplina,
                   COUNT(CASE WHEN m.status_matricula = 'Reprovado' THEN 1 END) AS reprovados,
                   COUNT(*) AS total,
                   ROUND((COUNT(CASE WHEN m.status_matricula = 'Reprovado' THEN 1 END) / COUNT(*)) * 100, 2) AS perc_reprovacao
            FROM disciplinas d
            JOIN turmas t ON d.disciplina_id = t.disciplina_id
            JOIN matriculas m ON t.turma_id = m.turma_id
            GROUP BY d.disciplina_id, d.nome_disciplina
            ORDER BY perc_reprovacao DESC;
        """
        cursor.execute(sql)
        disc = cursor.fetchall()
        print("\n--- Disciplinas com maior reprovação ---")
        for d in disc:
            print(f"Disciplina: {d['nome_disciplina']} | Reprovados: {d['reprovados']} | "
                  f"Total: {d['total']} | % Reprovação: {d['perc_reprovacao']}%")
    conexao.close()

def cursos_com_formandos():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT c.nome_curso, COUNT(a.aluno_id) AS formandos
            FROM cursos c
            JOIN alunos a ON c.curso_id = a.curso_id
            WHERE a.status_aluno = 'Formado'
            GROUP BY c.curso_id, c.nome_curso
            ORDER BY formandos DESC;
        """
        cursor.execute(sql)
        cursos = cursor.fetchall()
        print("\n--- Cursos com mais formandos ---")
        for c in cursos:
            print(f"Curso: {c['nome_curso']} | Formandos: {c['formandos']}")
    conexao.close()

# ==========================
# Testando as funções
# ==========================
if __name__ == "__main__":
    listar_disciplinas()
    relatorio_turmas()
    buscar_alunos(nome="Maria")   # exemplo de busca parcial
    alunos_com_media_alta()
    disciplinas_com_reprovacao()
    cursos_com_formandos()
