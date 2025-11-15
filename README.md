# 🧠 HelPy — Agente de Sistema de Arquivos Local

Este projeto implementa um **agente de IA em Python** que utiliza a **API Google Gemini** e sua capacidade de *function calling* para interagir de forma controlada com um sistema de arquivos local.

O agente é capaz de **ler**, **escrever**, **listar** e **executar** arquivos dentro de um diretório de trabalho específico (*sandbox*), garantindo isolamento e segurança: ele **nunca acessa nem modifica** arquivos fora da área permitida.

---

## 🚀 Principais Recursos

- **Listar Arquivos:** O agente pode listar o conteúdo de diretórios.  
- **Ler Arquivos:** Lê o conteúdo de arquivos específicos (com limite de 10.000 caracteres).  
- **Escrever Arquivos:** Cria novos arquivos ou sobrescreve arquivos existentes com o conteúdo fornecido.  
- **Executar Scripts:** Executa scripts Python (`.py`) e captura sua saída (`STDOUT` e `STDERR`).  
- **Segurança (Sandbox):** Todas as operações são confinadas a um `working_directory`. O agente **não pode acessar** caminhos fora dessa área (ex.: `../` ou `/bin`).  

---

## ⚙️ Como Funciona

O fluxo de interação é orquestrado pelo arquivo `main.py`:

1. **Entrada do Usuário:** O usuário fornece um prompt pela linha de comando (ex: `"liste todos os arquivos"`).  
2. **Chamada à API:** O `main.py` envia o prompt à API Gemini, junto com a lista de ferramentas disponíveis (`get_files_info`, `get_file_content`, etc.).  
3. **Plano da IA:** A IA analisa o prompt e decide qual ferramenta deve usar, retornando uma *function call* (ex.: `function_call: get_files_info(directory=".")`).  
4. **Execução Local:** O `main.py` interpreta essa solicitação e chama a função Python local correspondente.  
5. **Verificação de Segurança:** A função valida o caminho usando `is_child` de `config.py` para garantir que ele está dentro do diretório permitido.  
6. **Retorno da Função:** O resultado (ex.: lista de arquivos) é retornado ao `main.py`.  
7. **Novo Ciclo:** O resultado é enviado de volta à IA Gemini, que pode realizar novas chamadas, se necessário.  
8. **Resposta Final:** A IA então responde em linguagem natural ao usuário (ex.: `"Aqui estão os arquivos no diretório..."`).  

Esse ciclo pode se repetir se a IA precisar combinar múltiplas ferramentas (ex.: ler, modificar e reescrever um arquivo).

---

## 🛠️ Instalação e Configuração

### 1. Requisitos
Certifique-se de ter **Python 3** instalado.

### 2. Instalar Dependências
Este projeto usa **`uv`** para gerenciamento de pacotes. As dependências estão listadas no arquivo `pyproject.toml`.
Se você ainda não tem o `uv`, pode instalá-lo rapidamente por esse [link](https://docs.astral.sh/uv/getting-started/installation/).

Crie o ambiente virtual e instale as dependências:
```bash
# 1. Crie um ambiente virtual (recomendado)
uv venv

# 2. Ative o ambiente
# No macOS/Linux:
source .venv/bin/activate
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 3. Instale as dependências do pyproject.toml
uv pip install .
```

### 3. Configurar a Chave de API
Crie um arquivo `.env` na raiz do projeto com sua chave da API Gemini:

```ini
GEMINI_API_KEY=SUA_CHAVE_DE_API_AQUI
```

### 4. Criar o Diretório de Trabalho (Sandbox)
O `main.py` está configurado para usar `./calculator` como diretório de trabalho:

```python
# main.py (dentro de call_function)
function_result = func(working_directory="./calculator", **function_args)
# defina para o diretório desejado
```
---

## 🧩 Como Usar

Execute o programa pela linha de comando:

```bash
python3 main.py "Seu pedido aqui"
```

### Exemplos de Prompts

- **Listar arquivos:**
```bash
python3 main.py "Quais arquivos estão no diretório atual?"
```

- **Ler um arquivo:**
```bash
python3 main.py "Leia o conteúdo do arquivo 'main.py' dentro da pasta calculator."
```

- **Escrever um arquivo:**
```bash
python3 main.py "Crie um arquivo chamado 'hello.py' e coloque nele o seguinte código: print('olá, mundo!')"
```

- **Executar um arquivo:**
```bash
python3 main.py "Agora, execute o arquivo 'hello.py' que acabamos de criar."
```

- **Tarefa complexa:**
```bash
python3 main.py "Leia o arquivo 'lorem.txt' e depois sobrescreva-o com o texto 'este arquivo foi modificado'."
```

---

## 📁 Estrutura do Projeto

```plaintext
.
├── functions/
│   ├── config.py           # Configurações globais e função de segurança
│   ├── get_file_content.py # Ler arquivos
│   ├── get_files_info.py   # Listar arquivos
│   ├── run_python_file.py  # Executar scripts .py
│   └── write_file.py       # Escrever arquivos
├── calculator/             # Diretório "sandbox" de exemplo
│   └── (seus arquivos de teste)
├── main.py                 # Ponto de entrada e orquestrador da IA
├── tests.py                # Testes unitários
└── requirements.txt        # Dependências do Python
```

---

## 🧪 Próximos Passos

- Adicionar suporte a logs e monitoramento das operações.  
- Integrar outras funções do sistema (ex.: manipulação de JSON, compressão, etc.).  
- Criar uma interface interativa (CLI ou web).  

---


