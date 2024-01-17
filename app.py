from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_DATABASE = 'test'

def create_table():
    try:
        print("Abrindo conexão para criar tabela...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        cursor = conn.cursor()

        # Verifica se a tabela existe
        cursor.execute("SHOW TABLES LIKE 'users'")
        table_exists = cursor.fetchone()

        if not table_exists:
            print("Tabela 'users' não encontrada. Criando tabela...")
            # Se a tabela não existir, cria a tabela
            cursor.execute('''
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    location VARCHAR(255),
                    machine_name VARCHAR(255),
                    ip VARCHAR(255),
                    serial_number VARCHAR(255),
                    asset_number VARCHAR(255),
                    monitor1_model VARCHAR(255),
                    monitor1_serial VARCHAR(255),
                    monitor1_asset VARCHAR(255),
                    monitor2_model VARCHAR(255),
                    monitor2_serial VARCHAR(255),
                    monitor2_asset VARCHAR(255)
                )
            ''')

            # Inserir dados de exemplo
            cursor.execute('''
                INSERT INTO users (
                    location, machine_name, ip, serial_number, asset_number,
                    monitor1_model, monitor1_serial, monitor1_asset,
                    monitor2_model, monitor2_serial, monitor2_asset
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', ('Sala 101', 'PC-001', '192.168.0.1', 'ABC123', '123456', 'Dell', 'SN123', 'A123', 'HP', 'SN456', 'B456'))

        conn.commit()
        conn.close()
        print("Conexão fechada após criar tabela.")
    except Exception as e:
        print("Erro ao criar tabela:", str(e))

create_table()

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para lidar com o formulário
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        location = request.form['location']
        machine_name = request.form['machine_name']
        ip = request.form['ip']
        serial_number = request.form['serial_number']
        asset_number = request.form['asset_number']
        monitor1_model = request.form['monitor1_model']
        monitor1_serial = request.form['monitor1_serial']
        monitor1_asset = request.form['monitor1_asset']
        monitor2_model = request.form['monitor2_model']
        monitor2_serial = request.form['monitor2_serial']
        monitor2_asset = request.form['monitor2_asset']

        try:
            print("Abrindo conexão para inserir dados no formulário...")
            # Conectar ao banco de dados e inserir os dados
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE
            )
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (
                    location, machine_name, ip, serial_number, asset_number,
                    monitor1_model, monitor1_serial, monitor1_asset,
                    monitor2_model, monitor2_serial, monitor2_asset
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (location, machine_name, ip, serial_number, asset_number,
                  monitor1_model, monitor1_serial, monitor1_asset,
                  monitor2_model, monitor2_serial, monitor2_asset))

            conn.commit()
            conn.close()
            print("Conexão fechada após inserir dados no formulário.")
            print("Dados do formulário inseridos com sucesso.")
        except Exception as e:
            print("Erro ao inserir dados no formulário:", str(e))

        return redirect(url_for('impressora.hmtl'))

if __name__ == '__main__':

    app.run(debug=False)
