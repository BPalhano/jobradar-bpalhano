import pytest
from core.job import (
    Job,
    extrair_salario,
    extrair_tipo_contrato,
)
from core.perfis import PERFIL_BR, PERFIL_INTL
from notifier.telegram import _linha_relevancia


def test_extrair_salario():
    assert extrair_salario("USD 250 - 500") == "USD 250 - 500"
    assert extrair_salario("Menos de USD 50") == "Menos de USD 50"
    assert extrair_salario("Embedded Engineer ($120k - $150k/year)") == "$120k - $150k/year"
    assert extrair_salario("Remuneração: €70,000 to €90,000") == "€70,000 to €90,000"
    assert extrair_salario("R$ 10.000,00 a R$ 15.000,00 por mês") == "R$ 10.000,00 a R$ 15.000,00 por mês"
    assert extrair_salario("Vaga sem valor nenhum") == ""


def test_extrair_tipo_contrato():
    assert extrair_tipo_contrato("Firmware Developer (Contractor)") == "Contractor"
    assert extrair_tipo_contrato("Desenvolvedor C++ [PJ]") == "PJ / B2B"
    assert extrair_tipo_contrato("Engenheiro de Sistemas Embarcados - CLT") == "CLT"
    assert extrair_tipo_contrato("Projeto Freelance de IoT") == "Freelance"
    assert extrair_tipo_contrato("Prestação de Serviços em Telecom") == "Prestação de Serviços"


def test_job_e_prestacao_servico():
    vaga_workana = Job(
        titulo="Desenvolvimento ESP32",
        empresa="Cliente",
        local="Remoto",
        link="https://www.workana.com/job/1",
        site="Workana",
    )
    assert vaga_workana.e_prestacao_servico is True
    assert vaga_workana.tipo_contrato == "Prestação de Serviços / Freelance"

    vaga_contractor = Job(
        titulo="Embedded Linux Engineer (Contractor)",
        empresa="Acme",
        local="Remote",
        link="https://example.com/job/2",
        site="LinkedIn",
    )
    assert vaga_contractor.e_prestacao_servico is True

    vaga_clt = Job(
        titulo="Engenheiro de Firmware CLT",
        empresa="Acme BR",
        local="Remoto",
        link="https://example.com/job/3",
        site="Gupy",
        tipo_contrato="CLT",
    )
    assert vaga_clt.e_prestacao_servico is False


def test_pontuar_relevancia_novos_pontos():
    regras = PERFIL_BR.regras
    base_job = Job(
        titulo="Engenheiro de Firmware",
        empresa="Acme",
        local="Remoto",
        link="https://example.com/job/base",
        site="Gupy",
        modalidade="Remoto",
    )
    score_base = base_job.pontuar_relevancia(regras)

    job_prestacao = Job(
        titulo="Engenheiro de Firmware (Contractor)",
        empresa="Acme",
        local="Remoto",
        link="https://example.com/job/p1",
        site="Gupy",
        modalidade="Remoto",
    )
    assert job_prestacao.pontuar_relevancia(regras) == score_base + 1

    job_salario = Job(
        titulo="Engenheiro de Firmware",
        empresa="Acme",
        local="Remoto",
        link="https://example.com/job/p2",
        site="Gupy",
        modalidade="Remoto",
        salario="USD 3000 - 5000",
    )
    assert job_salario.pontuar_relevancia(regras) == score_base + 1

    job_ambos = Job(
        titulo="Engenheiro de Firmware (Contractor)",
        empresa="Acme",
        local="Remoto",
        link="https://example.com/job/p3",
        site="Gupy",
        modalidade="Remoto",
        salario="USD 3000 - 5000",
    )
    assert job_ambos.pontuar_relevancia(regras) == score_base + 2


def test_linha_relevancia():
    assert "12/12" in _linha_relevancia(12)
    assert "⭐⭐⭐⭐⭐" in _linha_relevancia(12)
    assert "6/12" in _linha_relevancia(6)
    assert "0/12" in _linha_relevancia(0)

from database.database import iniciar_db, salvar_vaga, ja_vista, _conectar


def test_db_salario_e_tipo_contrato(tmp_path, monkeypatch):
    test_db = str(tmp_path / "test_jobs.db")
    monkeypatch.setattr("database.database.DB_PATH", test_db)

    iniciar_db()

    job = Job(
        titulo="Engenheiro Firmware Contractor",
        empresa="Empresa Teste",
        local="Remoto",
        link="https://example.com/job/teste-db-1",
        site="Workana",
        salario="USD 100 - 200",
        tipo_contrato="Prestação de Serviços / Freelance",
        modalidade="Remoto",
    )

    assert not ja_vista(job)
    salvar_vaga(job, perfil_chave="brasil")
    assert ja_vista(job)

    # Verificar se as colunas foram persistidas
    with _conectar() as conn:
        row = conn.execute("SELECT salario, tipo_contrato FROM vagas_vistas WHERE id = ?", (job.id,)).fetchone()
        assert row is not None
        assert row[0] == "USD 100 - 200"
        assert row[1] == "Prestação de Serviços / Freelance"
