
import time
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

from core.job import Job, extrair_data_publicacao
from core.logger import get_logger
from scrapers.base import BaseScraper

logger = get_logger()


class WorkanaScraper(BaseScraper):
    """Scraper para Workana (workana.com) — plataforma de projetos,
    freelance, prestação de serviços e trabalho remoto.
    """

    def __init__(self, termos_busca: list[str]):
        self.termos_busca = termos_busca

    def buscar_vagas(self) -> list[Job]:
        vagas: list[Job] = []
        for termo in self.termos_busca:
            vagas.extend(self._buscar_termo(termo))

        logger.info(f"[Workana] {len(vagas)} vaga(s) encontrada(s) no total")
        return vagas

    def _buscar_termo(self, termo: str) -> list[Job]:
        logger.info(f"[Workana] Buscando projetos: {termo}")
        vagas: list[Job] = []
        termo_url = quote_plus(termo)
        url = f"https://www.workana.com/jobs?query={termo_url}"

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled"],
                )
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                    ),
                    viewport={"width": 1280, "height": 800},
                    locale="pt-BR",
                )
                page = context.new_page()
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2)

                items = page.locator(".project-item").all()
                for item in items:
                    try:
                        link_el = item.locator('a[href*="/job/"]').first
                        if not link_el.count():
                            continue

                        titulo = link_el.inner_text().strip()
                        href = link_el.get_attribute("href") or ""
                        if not href:
                            continue

                        if href.startswith("/"):
                            link = f"https://www.workana.com{href}"
                        else:
                            link = href

                        # Se o título estiver truncado com reticências, recupera do slug da URL
                        if (titulo.endswith("...") or titulo.endswith("…")) and "/job/" in href:
                            slug = href.split("/job/")[-1].split("?")[0].replace("-", " ").strip()
                            if slug:
                                titulo = slug.capitalize()

                        budget_el = item.locator(".budget, .values").first
                        salario = budget_el.inner_text().strip() if budget_el.count() else ""

                        date_el = item.locator(".date, time").first
                        data_publicacao = date_el.inner_text().strip() if date_el.count() else ""
                        if not data_publicacao:
                            data_publicacao = extrair_data_publicacao(item.inner_text())

                        country_el = item.locator('a[href*="country="]').first
                        pais_cliente = country_el.inner_text().strip() if country_el.count() else ""
                        local = f"Remoto ({pais_cliente})" if pais_cliente else "Remoto (Mundial)"

                        vagas.append(Job(
                            titulo=titulo,
                            empresa="Cliente Workana",
                            local=local,
                            link=link,
                            site="Workana",
                            publicado_em=data_publicacao,
                            modalidade="Remoto",
                            salario=salario,
                            tipo_contrato="Prestação de Serviços / Freelance",
                            escopo_indefinido=True,
                        ))
                    except Exception as e:
                        logger.warning(f"[Workana] Erro ao processar projeto: {e}")
                        continue

                browser.close()
        except Exception as e:
            logger.error(f"[Workana] Erro ao buscar '{termo}': {e}")

        return vagas
