import pymysql

def conectar():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='sistema_escolar',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 1) Alunos com média acima de 8.0
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
        resultados = cursor.fetchall()
        print("\n--- Alunos com média acima de 8.0 ---")
        for r in resultados:
            print(f"ID: {r['aluno_id']} | Nome: {r['nome']} | Média: {r['media']}")
    conexao.close()

# 2) Disciplinas com maior índice de reprovação
def disciplinas_com_reprovacao():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT d.disciplina_id, d.nome_disciplina,
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
        resultados = cursor.fetchall()
        print("\n--- Disciplinas com maior índice de reprovação ---")
        for r in resultados:
            print(f"ID: {r['disciplina_id']} | Disciplina: {r['nome_disciplina']} | "
                  f"Reprovados: {r['reprovados']} | Total: {r['total']} | % Reprovação: {r['perc_reprovacao']}%")
    conexao.close()

# 3) Cursos com maior número de formandos
def cursos_com_formandos():
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = """
            SELECT c.curso_id, c.nome_curso, COUNT(a.aluno_id) AS formandos
            FROM cursos c
            JOIN alunos a ON c.curso_id = a.curso_id
            WHERE a.status_aluno = 'Formado'
            GROUP BY c.curso_id, c.nome_curso
            ORDER BY formandos DESC;
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        print("\n--- Cursos com maior número de formandos ---")
        for r in resultados:
            print(f"ID: {r['curso_id']} | Curso: {r['nome_curso']} | Formandos: {r['formandos']}")
    conexao.close()


# Testando as funções
alunos_com_media_alta()
disciplinas_com_reprovacao()
cursos_com_formandos()
