# Alexandrita(PT-BR)

O pequeno script abaixo tem como objetivo editar e mudar as cores de anotações manuscritas em png,jpg ou pdf. Ele foi feito para embelezar de forma simples e rápida as anotações do obsidian, mas talvez alguns queiram usar para objetivos diversos. O programa foi batizado de alexandrita porque é o nome de uma pedra preciosa que é capaz de mudar de cor.

# Sobre o papel e caneta
## Papel
O programa deve ser inteligente suficiente para olhar qual é a cor de papel que você estará usando. Embora eu tenha no presente momento testado apenas com papel A4 branco padrão, em teroria deve funcionar com papel de qualquer cor.

## Caneta
O presente script trabalha apenas com caneta preta. Caso você use outra cor, é possível trocar a cor da caneta na linha 126.Entretanto, a eficácia do programa pode ser questionável.Talvez modificar a tolerância da caneta na linha 26 ajude

# Bibliotecas externas requeridas
Para utilizar esse script, você precisa instalar essas 3 bibliotecas:numpy, pillow e pymupdf.Dependendo do seu sistema ou ambiente de desenvolvimento, os meios para instalar essas bibliotecas podem varias:

Vscodium ou Vscode
```
pip install pillow pymupdf numpy
```

Distros linux baseadas no Debain
```bash
sudo apt update
sudo apt install python3 python3-pip
sudo apt install build-essential
pip3 install pillow pymupdf numpy
```

Windows
```cmd
pip install pillow pymupdf numpy
```
# Como usar
1. Coloque o caminho da entrada, onde seus pdfs ou imagens que devem ser processadas devem entrar (linha 152)
2. Logicamente você também deve apontar a pasta de saída onde os arquivos processados devem sair (linha 153)
3. Você pode determinar a cor da caneta de saída com qualquer cor RGB que quiser, ou pode escolher as opções Catppuccinn Mocha que foram colocadas no script (linha 65)
4. Por fim, também existe a possilidade de trocar a cor de fundo (linha 47)
