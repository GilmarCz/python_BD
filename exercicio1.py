import pymysql

def listar_disciplinas():
    try:
        conexao = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='sistema_escolar',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

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

            print("\n--- Disciplinas Disponíveis ---")
            for disc in disciplinas:
                print(f"ID: {disc['disciplina_id']} | "
                      f"Nome: {disc['nome_disciplina']} | "
                      f"Carga Horária: {disc['carga_horaria']}h | "
                      f"Alunos Matriculados: {disc['num_alunos']}")

    except Exception as erro:
        print("Erro ao consultar disciplinas:", erro)

    finally:
        if conexao and conexao.open:
            conexao.close()

# Teste
listar_disciplinas()
