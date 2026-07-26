import json
import urllib.request

HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def from_guidi():
    d = fetch("https://api.guidi.dev.br/loteria/lotofacil/ultimo")
    return {
        "concurso": d["numero"],
        "data": d["dataApuracao"],
        "dezenas": d["listaDezenas"],
        "premiacoes": [
            {"descricao": p["descricaoFaixa"], "valorPremio": p["valorPremio"]}
            for p in d["listaRateioPremio"]
        ],
        "acumulou": d["acumulado"],
        "valorAcumuladoProximoConcurso": d.get("valorAcumuladoProximoConcurso", 0),
        "valorEstimadoProximoConcurso": d.get("valorEstimadoProximoConcurso", 0),
    }


def from_loteriascaixa_api():
    d = fetch("https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest")
    return {
        "concurso": d["concurso"],
        "data": d["data"],
        "dezenas": d["dezenas"],
        "premiacoes": d["premiacoes"],
        "acumulou": d.get("acumulou", False),
        "valorAcumuladoProximoConcurso": d.get("valorAcumuladoProximoConcurso", 0),
        "valorEstimadoProximoConcurso": d.get("valorEstimadoProximoConcurso", 0),
    }


def main():
    result = None
    errors = []
    for source in (from_guidi, from_loteriascaixa_api):
        try:
            result = source()
            print(f"{source.__name__}: OK (concurso {result['concurso']}, {result['data']})")
            break
        except Exception as e:
            print(f"{source.__name__}: FALHOU ({type(e).__name__}: {e})")
            errors.append(f"{source.__name__}: {e}")

    if result is None:
        raise SystemExit("Todas as fontes falharam:\n" + "\n".join(errors))

    with open("latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Salvo:", result["concurso"], result["data"])


if __name__ == "__main__":
    main()
