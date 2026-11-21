from .models import HistoricoAcao

def empresa_do_usuario(usuario):
    if usuario.tipo == 'funcionario':
        funcionario = getattr(usuario, 'perfil_funcionario', None)
        if funcionario:
            return funcionario.empresa
    return usuario

def filtrar_empresa(queryset, usuario):
    if hasattr(queryset.model, 'empresa'):
        return queryset.filter(empresa=empresa_do_usuario(usuario))
    return queryset

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