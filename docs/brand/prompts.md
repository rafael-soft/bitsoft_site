# Prompts para gerar os logos individualmente (ChatGPT / geradores de imagem)

Os arquivos oficiais são os SVGs em `assets/brand/` (vetoriais, gerados por `docs/brand/gen.py`).
Use estes prompts apenas se quiser versões raster alternativas. Anexe sempre a prancha
`docs/brand/prancha-chatgpt.png` como referência e peça **uma imagem por vez**.

**Base comum (cole no início de cada prompt):**

> Usando a prancha anexada como referência exata, recrie somente a variação descrita abaixo da marca Bitsoft:
> símbolo "B" geométrico com o código `</>` no centro, gradiente de azul #0EA5E9 (canto superior direito)
> para violeta #7C3AED (canto inferior esquerdo), wordmark "Bitsoft" em sans-serif extrabold (estilo Inter Black)
> com o pingo do "i" em quadrado violeta #7C3AED, slogan "SOLUÇÕES EM APLICAÇÕES WEB" em caixa alta com espaçamento largo.
> Design vetorial plano, bordas nítidas, centralizado, margem generosa, alta resolução, sem mockup, sem sombras externas,
> sem texto adicional, sem rótulos.

1. **Logo horizontal (principal):** símbolo à esquerda, wordmark branco #F8FAFC e slogan cinza-claro à direita, fundo sólido navy #0B1026, proporção 3:1.
2. **Logo horizontal (fundo claro):** mesma composição, wordmark navy #0B1026, slogan cinza #334155, fundo transparente (ou branco), proporção 3:1.
3. **Logo vertical (principal):** símbolo centralizado acima do wordmark branco e do slogan, fundo navy #0B1026, proporção 1:1.
4. **Logo vertical (fundo claro):** igual ao anterior, wordmark navy, fundo transparente, proporção 1:1.
5. **Ícone colorido:** apenas o símbolo com gradiente e `</>` branco, dentro de um quadrado navy #0B1026 de cantos arredondados (estilo ícone de app), 1024×1024.
6. **Ícone branco:** símbolo sólido navy #0B1026 sobre quadrado branco #F8FAFC de cantos arredondados, 1024×1024.
7. **Ícone escuro:** símbolo sólido branco #F8FAFC sobre quadrado navy #0B1026 de cantos arredondados, 1024×1024.
8. **Monocromático:** apenas o símbolo em uma única cor sólida (branco, violeta #7C3AED, azul #0EA5E9 ou cinza #94A3B8), isolado, fundo transparente, 1024×1024.

Dica: peça "PNG com fundo transparente" explicitamente; se o gerador não suportar, use fundo sólido e remova depois.
