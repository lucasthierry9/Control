from .models import HistoricoAcao

def registrar_acao(usuario, modulo, descricao):
    HistoricoAcao.objects.create(
        usuario=usuario,
        modulo=modulo,
        descricao=descricao
    )

def ultimas_acoes_modulo(usuario, modulo, limite=3):
    return HistoricoAcao.objects.filter(
        usuario=usuario,
        modulo=modulo
    ).order_by('-criado_em')[:limite]