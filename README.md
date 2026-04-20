# AGE - Administração de Ginásios de Embu

**Versão Atual:** `0.3.0 (Beta)`  
**Desenvolvedor:** Leonardo Braga Silva

O **AGE** é uma solução robusta de gerenciamento administrativo desenvolvida em **Python**, projetada para centralizar o controle de alunos, cursos e turmas. O sistema utiliza uma arquitetura modular que separa a interface gráfica (GUI) da lógica de persistência de dados, garantindo escalabilidade e facilidade de manutenção.

# Stack Tecnológica

O projeto foi construído utilizando as ferramentas mais estáveis do ecossistema Python:

* **Interface Gráfica:** Tkinter (Customizada com o tema *Clam* para uma estética profissional).
* **Banco de Dados:** SQLite3 com suporte total a Relacionamentos e Chaves Estrangeiras.
* **Processamento de Imagem:** Pillow (PIL) para o tratamento dinâmico de fotos de perfil.
* **Análise de Dados:** Pandas para a engine de exportação em Excel.
* **Geração de Documentos:** FPDF para emissão de relatórios em PDF.
* **Utilidades:** `tkcalendar` (seleção de datas) e `shutil` (gestão de arquivos do sistema).

# Funcionalidades Principais

### 1. Central de Alunos (Módulo CRM)
* **Cadastro Biométrico Visual:** Vinculação de fotos aos alunos, com sistema de cópia automática para o diretório local do software.
* **Arquitetura de Busca:** Motor de busca por nome com filtragem dinâmica em tempo real na Treeview.
* **Segurança de Dados:** Validação de campos obrigatórios e tratamento de exceções em tempo de execução.

### 2. Gestão Acadêmica (Cursos & Turmas)
* **Integridade Referencial:** Implementação de `ON UPDATE CASCADE` e `ON DELETE CASCADE`. Se o nome de um curso for alterado, o sistema propaga a mudança para todas as turmas vinculadas automaticamente.
* **Automação de Seleção:** Componentes Combobox alimentados dinamicamente via banco de dados para evitar erros de digitação.

### 3. Business Intelligence (BI) & Relatórios
* **Exportação Multiformato:** Conversão de qualquer tabela do sistema para arquivos `.xlsx` (Excel) ou `.pdf`.
* **Relatórios Administrativos:** Documentos gerados com formatação limpa e profissional para apresentações e arquivos físicos.

# Arquitetura do Projeto

A organização do código segue o princípio de separação de responsabilidades:

* **`main.py`**: Orquestrador da interface e controle de fluxo entre frames.
* **`view.py`**: Camada de acesso a dados (Data Access Layer), contendo as queries SQL e lógica CRUD.
* **`cadastro_alunos.db`**: Banco de dados relacional local.
* **`/fotos_alunos`**: Diretório dinâmico que armazena os assets visuais do sistema (fotos nomeadas por CPF).

# Instalação e Execução

Para implantar o sistema em ambiente local, siga os passos abaixo:

# Clone o repositório
git clone https://github.com/lsbraga/AGE.git

# Instale as dependências necessárias
pip install pandas pillow tkcalendar fpdf openpyxl

# Inicie o software
python main.py

Licença e Créditos

Este projeto foi desenvolvido por Leonardo Braga Silva.

É um software destinado à modernização de processos administrativos em ginásios.
