# MSW-tradutor
Software tradutor de API dos receptores Sennheiser/Shure para stream e rest.

### Instalação
1. Faça um clone do repositório.
2. Crie um novo ambiente virtual. `python -m venv venv`
3. Atualize a versão do pip. `python -m pip install --upgrade pip`
4. Instale todas as dependências. `python -m pip install -r requirements.txt`

### Configuração
1. Acesse o arquivo `/configs/settings.py` para incluir informações do banco de dados.
2. Verificamos as atualizações pro nosso modelo do banco de dados. `python manage.py makemigrations`
3. Em seguida, aplicamos as atualizações verificadas. `python manage.py migrate`
4. E para finalizar, carregamos os dados iniciais. `python manage.py first-data`

### Usabilidade
1. Tudo certo! Podemos iniciar a aplicação do tradutor. `python manage.py msw`
2. Também é possível monitorar o servidor do tradutor. `python manage.py monitor`
3. Opcionalmente, pode-se utilizar o servidor django. `python manage.py runserver`
