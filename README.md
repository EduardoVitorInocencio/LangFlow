# LangFlow - Superchatbot com LangChain, FastAPI e React

**Status do Projeto**: *Em Desenvolvimento*

## Sobre o Projeto

O **LangFlow** é um superchatbot inteligente projetado para integrar diversas APIs externas e oferecer respostas dinâmicas e automatização de tarefas. Utilizando **LangChain** e **FastAPI** no backend, e um frontend moderno desenvolvido com **React**, o LangFlow funciona como um microserviço para facilitar interações conversacionais avançadas.

## Tecnologias Utilizadas

- **Backend**:
  - LangChain
  - FastAPI
  - Uvicorn
  - Requests (para interação com APIs externas)
  - Pydantic (para validação de dados)

- **Frontend**:
  - React.js
  - TailwindCSS (para estilização rápida e responsiva)
  - Axios (para requisições HTTP ao backend)
  - React Router (para navegação entre páginas)

## Funcionalidades Atuais

- **Busca no Wikipedia**: Retorna informações detalhadas extraídas diretamente da Wikipedia.
- **Previsão do Tempo**: Consulta previsão meteorológica para qualquer localidade.
- **Busca de CEP**: Obtém dados completos de endereço a partir de um CEP.
- **Cotação de Moedas**: Retorna valores de câmbio atualizados para diferentes moedas.

## Funcionalidades Futuras

- **Integração com mais APIs**: Ampliaremos a quantidade de serviços disponíveis.
- **Automatização de Processos**: O LangFlow será capaz de executar tarefas automatizadas.
- **Personalização de Agentes**: Permitiremos que usuários configurem respostas e comportamentos específicos.

## Como Usar

### Clonar o repositório
```bash
  git clone https://github.com/seu-usuario/langflow.git
  cd langflow
```

### Configurar o Backend
```bash
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload
```

### Configurar o Frontend
```bash
  cd frontend
  npm install
  npm start
```

Acesse a aplicação pelo navegador:
```
http://localhost:3000
```

## Estrutura do Projeto

```
langflow/
│
├── backend/                  # Backend com FastAPI
│   ├── main.py               # API principal
│   ├── auth.py               # Autenticação de usuários
│   ├── chatbot.py            # Funções de integração com LangChain
│   └── requirements.txt      # Dependências do backend
│
├── frontend/                 # Frontend com React.js
│   ├── src/
│   │   ├── components/       # Componentes reutilizáveis
│   │   ├── pages/            # Páginas principais (Login, Chat, etc.)
│   │   ├── App.js            # Componente raiz
│   │   ├── index.js          # Entrada do aplicativo React
│   │   ├── api.js            # Configuração de chamadas ao backend
│   ├── public/
│   ├── package.json          # Dependências do frontend
│   ├── tailwind.config.js    # Configuração do TailwindCSS
│
└── README.md                 # Documentação do projeto
```

## Contribuindo

Contribuições são bem-vindas! Para colaborar:

1. Faça um **fork** deste repositório.
2. Crie uma **branch** para sua modificação:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Realize as alterações e envie as modificações:
   ```bash
   git commit -m "Adicionando nova funcionalidade"
   git push origin feature/nova-funcionalidade
   ```
4. Abra um **pull request**.

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.