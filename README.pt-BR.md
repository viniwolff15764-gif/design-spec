<p align="center"><img src="docs/assets/banner.svg" alt="Design Spec" width="100%"></p>

# Design Spec

**Descubra o nome de cada detalhe de um site, com prints mostrando qual é qual.**

Uma skill que orienta agentes de IA a inspecionar sites, identificar elementos visuais e animações e entregar um inventário técnico com evidências. A resposta vem no idioma do usuário, preservando os nomes técnicos em inglês.

[English documentation](README.md) · [Exemplo de relatório](examples/sample-report/report.md) · [Licença MIT](LICENSE)

## Instalação rápida

```sh
npx skills add viniwolff15764-gif/design-spec --skill design-spec
```

Selecione o agente. Acrescente `-g` para instalar globalmente.

Sem Node.js, com Python 3.10+:

```sh
git clone https://github.com/viniwolff15764-gif/design-spec.git
cd design-spec
python3 install.py
```

O instalador copia a skill para Claude Code e Codex. Não modifica configurações nem sobrescreve uma instalação diferente. No Windows, use `python` ou `py -3`.

## Como chamar

**Claude Code**
```text
/design-spec https://example.com
```

**Codex**
```text
$design-spec https://example.com
```

A sintaxe depende do aplicativo. No Codex, também é possível selecionar a skill por `/skills`. Outros agentes compatíveis com Agent Skills podem carregar a mesma pasta. Um agente sem suporte nativo pode ler o SKILL.md como instruções, desde que tenha as ferramentas necessárias.

## O que recebe

- Lista numerada dos elementos, estilos, tratamentos e animações observáveis.
- Prints com círculos, caixas e IDs correspondentes aos itens da lista.
- Evidências antes/depois para os movimentos.
- Especificações medidas: cores, tipografia, espaçamento, bordas e sombras.
- Diferenças entre desktop e celular.
- Relatório Markdown, inventário JSON e imagens, quando houver acesso a arquivos.
- Cobertura explícita: o que foi inspecionado e o que ficou inacessível.

![Exemplo original de relatório visual](docs/assets/example-annotated.png)

## Nomes reais, evidências reais

A skill separa:
- **Elemento:** notification banner, calendar heatmap, device mockup.
- **Tratamento:** outer glow, rounded corners, monochromatic palette.
- **Movimento:** fade, scale transition, scroll-linked translation.
- **Implementação:** apenas quando inspecionada, como `position: sticky`.

Ela distingue termos estabelecidos de descrições e classificações incertas. Não inventa uma categoria porque algo parece "premium", não chama todo celular inclinado de isométrico e não presume animação a partir de um print.

## Limites honestos

A skill usa o navegador e a visão do próprio agente. Não instala nem inclui um navegador. DOM/CSS melhora as medições; Python e Pillow permitem gerar as marcações. Sem esses recursos, informa a limitação.

Por padrão, cobre a URL fornecida e seus estados observáveis. Peça "o site inteiro" para incluir diferentes páginas e modelos públicos. Nenhuma inspeção pode garantir todos os estados privados, testes A/B, rotas ocultas ou combinações possíveis.

Veja opções de instalação, testes e estrutura no [README completo](README.md).
