"""Regras de negócio do perfil de Igor Braga Palhano (Sistemas Embarcados & Telecom).

Regras resumidas:
  BRASIL   -> remoto de qualquer lugar do país;
              híbrido/presencial SÓ nas cidades de CIDADES (Fortaleza/CE e região).
  EXTERIOR -> SÓ remoto (100% remoto em moeda forte: EUA, Europa, Canadá, Worldwide/Global).
              Nunca híbrido, nunca presencial no exterior.
"""

import pytest

from core.job import Job
from core.perfis import PERFIL_BR, PERFIL_INTL


def _vaga(titulo, local, modalidade):
    return Job(
        titulo=titulo, empresa="Empresa Teste", local=local,
        link=f"https://exemplo.com/{abs(hash((titulo, local, modalidade)))}",
        site="Teste", modalidade=modalidade,
    )


# Cidades aceitas para vagas presenciais/híbridas do perfil de Igor Palhano.
CIDADES_ACEITAS = [
    "Fortaleza", "Caucaia", "Eusébio", "Maracanaú", "Ceará",
]


# ---------------------------------------------------------------- BRASIL

@pytest.mark.parametrize("modalidade", ["Híbrido", "Presencial"])
@pytest.mark.parametrize("cidade", CIDADES_ACEITAS)
def test_br_hibrido_e_presencial_nas_cidades_aceitas(cidade, modalidade):
    assert _vaga("Engenheiro de Sistemas Embarcados", f"{cidade} - CE", modalidade).combina_com(PERFIL_BR.regras)


# Variacoes de escrita que as fontes realmente usam -- separador, acento e
# caixa nao podem mudar o resultado.
@pytest.mark.parametrize("local", [
    "Fortaleza", "Fortaleza - CE", "Fortaleza, CE",
    "Fortaleza/CE", "FORTALEZA - CE", "fortaleza, ce",
    "Caucaia - CE", "Caucaia, CE",
    "Eusébio - CE", "Maracanaú - CE",
])
def test_br_variacoes_de_escrita_da_cidade(local):
    assert _vaga("Desenvolvedor C++", local, "Híbrido").combina_com(PERFIL_BR.regras)


@pytest.mark.parametrize("modalidade", ["Híbrido", "Presencial"])
@pytest.mark.parametrize("local", [
    "São Paulo - SP", "Belo Horizonte, MG", "Salvador - BA",
    "Rio de Janeiro, RJ", "Curitiba - PR", "Brasília, DF",
    "Recife - PE", "Porto Alegre - RS", "Campina Grande - PB",
])
def test_br_hibrido_e_presencial_fora_das_cidades_e_rejeitado(local, modalidade):
    assert not _vaga("Engenheiro de Firmware", local, modalidade).combina_com(PERFIL_BR.regras)


@pytest.mark.parametrize("local", [
    "Remoto", "Remoto (São Paulo, SP)", "Remoto (Fortaleza, CE)",
    "Remoto - Brasil", "Remote, Brazil", "Remoto (Belo Horizonte, MG)",
])
def test_br_remoto_no_brasil_e_aceito_de_qualquer_cidade(local):
    """Remoto nao tem restricao de cidade -- a regra de CIDADES vale so
    pra hibrido/presencial."""
    assert _vaga("Engenheiro de Sistemas Embarcados", local, "Remoto").combina_com(PERFIL_BR.regras)


@pytest.mark.parametrize("local", [
    "Remote - US only", "Remote, United States", "Remote (Austin, TX)",
    "Remote - India",
])
def test_br_remoto_de_mercado_nao_aceito_e_rejeitado(local):
    assert not _vaga("Desenvolvedor C++", local, "Remoto").combina_com(PERFIL_BR.regras)


# --------------------------------------------------------- INTERNACIONAL

@pytest.mark.parametrize("local", [
    "Remote - Spain", "Madrid, Spain", "España (En remoto)",
    "Remote - Mexico", "Ciudad de México, México", "Remote - Portugal",
    "Remote - Latin America", "Remote - Colombia", "Buenos Aires, Argentina",
    "Remote - France", "Remote - Germany", "Remote - United States",
    "Remote - Worldwide", "Remote - United Kingdom",
])
def test_intl_remoto_em_mercado_aceito_e_aceito(local):
    assert _vaga("Embedded Systems Engineer", local, "Remoto").combina_com(PERFIL_INTL.regras)


@pytest.mark.parametrize("modalidade", ["Híbrido", "Presencial"])
@pytest.mark.parametrize("local", [
    "Madrid, Spain", "Barcelona, España", "Lisboa, Portugal",
    "Paris, France", "Berlin, Germany", "London, UK",
    "Ciudad de México, México", "Buenos Aires, Argentina",
])
def test_intl_hibrido_e_presencial_sempre_rejeitado(local, modalidade):
    """Do exterior so interessa vaga 100% remota."""
    assert not _vaga("Embedded Software Engineer", local, modalidade).combina_com(PERFIL_INTL.regras)


@pytest.mark.parametrize("local", [
    "Remote - India", "Remote - Vietnam", "Remote - Nigeria",
])
def test_intl_remoto_de_mercado_nao_aceito_e_rejeitado(local):
    assert not _vaga("Embedded Systems Engineer", local, "Remoto").combina_com(PERFIL_INTL.regras)


def test_intl_titulo_hibrido_vence_a_classificacao_da_fonte():
    """O filtro nativo do LinkedIn as vezes marca como remota uma vaga que
    o proprio anuncio chama de hibrida -- o titulo vence."""
    vaga = _vaga("Embedded Systems Engineer - Hybrid", "Paris, France", "Remoto")
    assert vaga.modalidade == "Híbrido"
    assert not vaga.combina_com(PERFIL_INTL.regras)


# ------------------------------------------------------------------ CARGO

@pytest.mark.parametrize("titulo, esperado", [
    ("Engenheiro de Sistemas Embarcados", True),
    ("Engenheiro de Firmware", True),
    ("Desenvolvedor C++", True),
    ("Engenheiro de Telecomunicações", True),
    ("DSP Engineer", True),
    ("Embedded Software Engineer", True),
    ("Edge AI Engineer", True),
    ("Desenvolvedor", False),                          # ambíguo, sem qualificador
    ("Desenvolvedor C++ Jr", True),                    # ambíguo + qualificador
    ("Desenvolvedor Python (Firmware)", True),         # qualificador no título
    ("Vendedor Externo", False),
    ("Gerente de Projetos Sênior", False),
    ("Suporte N1", False),                             # excluído por "suporte" / "n1"
    ("Atendimento e Helpdesk", False),                 # excluído por "atendimento" / "helpdesk"
    ("Vendas de Eletrônicos", False),                  # excluído por "vendas"
    ("Marketing Digital", False),                      # excluído por "marketing"
])
def test_cargo_no_titulo(titulo, esperado):
    assert _vaga(titulo, "Fortaleza - CE", "Presencial").combina_com(PERFIL_BR.regras) is esperado

