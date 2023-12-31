

#  views.py


from django.contrib.auth import authenticate, login
from .forms import LoginForm, DemandaForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import logging
from django.contrib.auth import logout


logger = logging.getLogger(__name__)
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('criar_demanda')  # página após o login
            else:
                form.add_error(None, 'Nome de usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

logger = logging.getLogger(__name__)
def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Usuário salvo com sucesso!")
            return redirect('user_login')
        else:
            logger.error("Formulário inválido: %s", form.errors)
            error_messages = form.errors.values()
            return render(request, 'cadastro.html', {'form': form, 'error_messages': error_messages})
    else:
        form = CustomUserCreationForm()

    return render(request, 'cadastro.html', {'form': form})


def enviar_email_nova_demanda(demanda):
    # Configurações de e-mail
    subject = 'Nova Demanda Criada'
    message = f'Uma nova demanda foi criada por {demanda.usuario.username}. Detalhes:\n\nTelefone: {demanda.telefone}\nProblema: {demanda.descricao}'
    from_email = settings.DEFAULT_FROM_EMAIL

    # Lista de destinatários
    to_email = settings.EMAIL_RECEPIENT

    try:
        # Enviar e-mail
        email = EmailMessage(subject, message, from_email, to_email)
        email.send()
        logger.info(f'E-mail enviado com sucesso para {", ".join(to_email)}')
    except Exception as e:
        logger.error(f'Erro ao enviar e-mail: {str(e)}')


# Verifica se o usuário está autenticado, redirecionando-o para a página de login se não estiver.
@login_required(login_url='user_login')
def criar_demanda(request):
    # Verifica novamente a autenticação para garantir que o usuário está autenticado.
    if request.user.is_authenticated:
        # Cria uma instância do formulário de demanda, passando o usuário autenticado como parâmetro.
        form = DemandaForm(user=request.user)

        # Verifica se o método da requisição é POST (envio de formulário).
        if request.method == 'POST':
            # Cria uma instância do formulário com os dados do POST, incluindo o usuário autenticado.
            form = DemandaForm(request.POST, user=request.user)
            
            # Verifica se o formulário é válido.
            if form.is_valid():
                # Salva a demanda no banco de dados, associando-a ao usuário autenticado.
                demanda = form.save(commit=False)
                demanda.usuario = request.user
                demanda.save()

                # Exibe uma mensagem de sucesso para o usuário.
                messages.success(request, 'A demanda foi criada com sucesso!')

                # Envia um e-mail para destinatários informando sobre a nova demanda.
                enviar_email_nova_demanda(demanda)

                # Cria um contexto com a variável 'sucesso' para ser usada no template 'aviso.html'.
                context = {'sucesso': True}

                # Renderiza o template 'aviso.html' com o contexto, exibindo a mensagem de sucesso.
                return render(request, 'aviso.html', context)

        else:
            # Se o método da requisição não for POST, mantém o formulário de demanda para exibição.
            form = DemandaForm(user=request.user)

        # Renderiza o template 'criar_demanda.html' com o formulário de demanda.
        return render(request, 'criar_demanda.html', {'form': form})
    else:
        # Se o usuário não estiver autenticado, redireciona para a página de login.
        return redirect('user_login')

def custom_logout(request):
   

    # Chame a função de logout do Django
    logout(request)

    # Redirecione para onde desejar após o logout
    
    return redirect('user_login')