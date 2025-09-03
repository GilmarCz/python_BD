import pymysql

def relatorio_turmas():
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
    
    except Exception as erro:
        print("Erro ao gerar relatório:", erro)
    finally:
        if conexao and conexao.open:
            conexao.close()

# Teste
relatorio_turmas()
