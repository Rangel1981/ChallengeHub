1. Banco de Dados & Modelagem (models.py)
    O foco aqui é garantir a integridade dos relacionamentos e os estados de cada desafio.
    •	[ ] Modelo de Perfil (Profile):
    o	[ ] Criar relacionamento $1:1$ com django.contrib.auth.models.User (OneToOneField).
    o	[ ] Adicionar campo plan (CharField com choices: 'free', 'pro').
    o	[ ] Adicionar post_save signal para criar/salvar o Profile automaticamente na criação de um User.

    •	[ ] Modelo de Desafio (Challenge):
    o	[ ] Adicionar relacionamento $N:1$ com o autor (ForeignKey para User, on_delete=CASCADE).
    o	[ ] Adicionar campos básicos: title (CharField), description (TextField), created_at (DateTimeField).
    o	[ ] Adicionar campo de visibilidade: is_public (BooleanField, default=True).
    o	[ ] Adicionar campo de limite numérico ou meta (ex: target_days ou target_count).

    •	[ ] Modelo de Engajamento/Participação (Participation):
    o	[ ] Criar relacionamento $N:1$ com User e $N:1$ com Challenge (Tabela pivô/intermediária para relacionamento $N:N$).
    o	[ ] Adicionar campo status (CharField com choices: 'in_progress', 'completed').
    o	[ ] Adicionar campo started_at (DateTimeField, auto_now_add=True).
    o	[ ] Definir restrição de unicidade em Meta: unique_together = ['user', 'challenge'] (impede o usuário de aceitar o mesmo desafio duas vezes).

2. Regras de Negócio & Segurança (views.py / services.py)
    •	[ ] Autenticação & Controle de Acesso:
        o	[ ] Proteger todas as views principais com @login_required.
        o	[ ] Garantir no formulário de cadastro que novas contas recebam o plano 'free' por padrão.
    •	[ ] Trava de Limites por Plano (Limitação SaaS):
        o	[ ] Antes de criar um desafio, contar quantos desafios criados o usuário possui (Challenge.objects.filter(user=request.user).count()).
        o	[ ] Comparar com o limite permitido (ex: Plano Gratuito = no máximo 3 desafios ativos).
        o	[ ] Retornar mensagem de erro/redirecionamento se o limite for atingido.

    •	[ ] Filtros e Permissões de Leitura:
        o	[ ] Feed Comunitário: Buscar apenas desafios onde is_public=True OU user=request.user (Q(is_public=True) | Q(user=request.user)).
        o	[ ] Painel Pessoal: Buscar apenas os desafios e participações vinculados a request.user.

    •	[ ] Permissões de Escrita e Deleção (Ownership):
        o	[ ] Nas views de edição e exclusão de desafios, validar se challenge.user == request.user.
        o	[ ] Retornar HttpResponseForbidden (403) ou erro se outro usuário tentar alterar via URL.
    •	[ ] Lógica de Participação:

        o	[ ] View para o usuário clicar em "Aceitar Desafio", criando o registro em Participation.
        o	[ ] View para alternar o status do desafio entre 'in_progress' e 'completed'.

3. Endpoints e Rotas (urls.py)
    •	[ ] Rota de Autenticação (/login/, /logout/, /cadastro/).
    •	[ ] Rota do Feed Comunitário (/desafios/).
    •	[ ] Rota de Meus Desafios (/meus-desafios/).
    •	[ ] Rota de Criação de Desafio (/desafios/novo/).
    •	[ ] Rota de Detalhes do Desafio (/desafios/<int:pk>/).
    •	[ ] Rota de Ações de Edição/Deleção (/desafios/<int:pk>/editar/, /desafios/<int:pk>/deletar/).
    •	[ ] Rota para Aceitar/Concluir Desafio (/desafios/<int:pk>/participar/).
    
4. Front-End & Interfaces (templates/)
    •	[ ] Layout Base (base.html):
        o	[ ] Configurar HTML5, CSS (Tailwind CSS, Bootstrap ou CSS puro) e bloco de mensagens do Django (django.contrib.messages).
        o	[ ] Navbar dinâmica: exibir "Login / Cadastrar" se deslogado, e "Feed / Meus Desafios / Sair" se logado.

    •	[ ] Páginas de Autenticação:
        o	[ ] Formulário de Login.
        o	[ ] Formulário de Cadastro (criando usuário e perfil).

    •	[ ] Feed Comunitário (feed.html):
        o	[ ] Cards de desafios listando: Título, Descrição curta, Nome do Criador ({{ challenge.user.username }}) e total de participantes.
    o	[ ] Botão de "Aceitar Desafio" ou "Ver Detalhes".
    •	[ ] Painel Pessoal (dashboard.html):

    o	[ ] Indicador de uso do plano (ex: "2 / 3 desafios criados").
    o	[ ] Abas ou seções para "Desafios Criados por Mim" e "Desafios em Andamento".
    o	[ ] Botões de "Editar" e "Deletar" renderizados apenas nos desafios que pertencem ao usuário logado ({% if challenge.user == user %}).

    •	[ ] Formulários (challenge_form.html):
    o	[ ] Campos estruturados para criação e edição.
    o	[ ] Checkbox para definir visibilidade (is_public)

