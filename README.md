# Control

O **Control** é um sistema web de gestão empresarial que centraliza o cadastro de produtos, clientes, fornecedores e funcionários, o controle de estoque e o registro de compras e vendas. Por meio de dashboards, gráficos e relatórios, permite que empresas acompanhem suas operações e consultem informações para apoiar a administração do negócio.

## Tecnologias previstas e utilizadas

| Área | Tecnologias |
| --- | --- |
| Backend | Python e Django 5.2.6 |
| Interface | HTML, CSS, JavaScript, Bootstrap 5 e templates do Django |
| Gráficos e tabelas | Chart.js e Simple-DataTables |
| Formulários | django-crispy-forms e crispy-bootstrap5 |
| Banco de dados | SQLite na configuração local; PostgreSQL 15 na configuração de deploy |
| Imagens e relatórios | Pillow, ReportLab e openpyxl |
| Infraestrutura de deploy | Docker, Docker Compose, Gunicorn e Nginx |

As dependências Python estão em [requirements.txt](requirements.txt), e a imagem Docker utiliza Python 3.11.

## Integrantes da equipe

| Nome | GitHub |
| --- | --- |
| Lucas Thierry | [lucasthierry9](https://github.com/lucasthierry9) |
| Fernando Cesar | [cesarfcg](https://github.com/cesarfcg) |
| Pedro Henrique | [Pedro44-henrique44](https://github.com/Pedro44-henrique44) |

## Como executar localmente

Pré-requisitos: Python 3.11 com pip e uma cópia do repositório. Execute os comandos na pasta que contém `manage.py`.

1. Crie e ative um ambiente virtual:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   No Linux/macOS, utilize `python3 -m venv venv` e `source venv/bin/activate`.

2. Instale as dependências:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Mantenha o bloco `DATABASES` do SQLite ativo em [config/settings.py](config/settings.py) e aplique as migrações:

   ```sh
   python manage.py migrate
   ```

4. Inicie o servidor de desenvolvimento:

   ```sh
   python manage.py runserver
   ```

5. Acesse <http://127.0.0.1:8000/> e utilize a opção de cadastro para criar sua conta. Para acessar o painel `/admin/`, crie também um administrador com `python manage.py createsuperuser`.

O `runserver` é destinado ao desenvolvimento. A configuração atual permite execução local com SQLite sem arquivo `.env`.

## Como executar com Docker e Nginx

Pré-requisitos: Docker com Docker Compose e porta 80 disponível. Os arquivos [docker-compose.yml](docker-compose.yml), [Dockerfile](Dockerfile), [entrypoint.sh](entrypoint.sh) e [nginx/nginx.conf](nginx/nginx.conf) definem essa estrutura.

1. Em [config/settings.py](config/settings.py), descomente o bloco `DATABASES` do PostgreSQL e comente o bloco do SQLite. O Compose já fornece as variáveis de conexão. Ajuste também `DEBUG` para converter o texto recebido do ambiente em booleano:

   ```python
   DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
   ```

   A leitura atual retorna uma string quando a variável existe; por isso, apenas definir `DEBUG=False` no `.env` não desativa o modo de depuração sem esse ajuste. Em `ALLOWED_HOSTS`, substitua `'*'` pelos domínios ou IPs usados para acessar o servidor, mantendo `localhost` e `127.0.0.1` se necessário.

2. Crie um arquivo `.env` na raiz do projeto com os valores abaixo, substituindo a chave e a senha por valores próprios. Esse arquivo já está no `.gitignore`:

   ```dotenv
   DEBUG=False
   SECRET_KEY=substitua_por_uma_chave_longa_e_aleatoria
   POSTGRES_DB=control
   POSTGRES_USER=control
   POSTGRES_PASSWORD=substitua_por_uma_senha_forte
   ```

   O Docker Compose lê esse arquivo e repassa as variáveis à aplicação.

3. Para acesso por domínio ou IP, ajuste `server_name` em [nginx/nginx.conf](nginx/nginx.conf). A configuração fornecida atende por HTTP na porta 80; para disponibilizar o sistema publicamente com HTTPS, configure também certificado e TLS no servidor.

4. Construa e inicie os serviços:

   ```sh
   docker compose up -d --build
   ```

   O script de inicialização aguarda o banco, aplica as migrações, coleta os arquivos estáticos e inicia o Gunicorn. O Nginx recebe as requisições e serve os arquivos estáticos e de mídia.

5. Acesse <http://localhost/> ou o endereço configurado. Para criar um administrador e consultar os logs:

   ```sh
   docker compose exec web python manage.py createsuperuser
   docker compose logs -f web nginx
   ```

Para encerrar os serviços, execute `docker compose down`. Os dados do PostgreSQL e os arquivos de mídia ficam em volumes persistentes. Ao voltar à execução local com `runserver`, reative o bloco do SQLite em `settings.py`.
