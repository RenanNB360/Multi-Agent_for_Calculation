# Case

## Visão Geral

Este projeto foi desenvolvido como um **case técnico de arquitetura com agentes e LLM**, focado em separação clara de responsabilidades, uso de ferramentas determinísticas fora do modelo e orquestração via grafo.

A aplicação permite que um usuário faça perguntas em linguagem natural. Dependendo da intenção, o sistema:
- Responde diretamente usando um LLM
- Ou delega cálculos matemáticos a um microserviço externo, evitando que o modelo "invente" resultados

Toda a comunicação é feita via containers Docker, com observabilidade básica e arquitetura preparada para evolução.

---

## Como instalar e rodar o projeto

### Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

- **Docker** (versão recente)
- **Docker Compose**
- **Ollama** rodando localmente ou acessível pela rede

### Ollama e modelo

Este projeto depende explicitamente do Ollama para execução do LLM.

Você precisa ter o modelo abaixo disponível:

```
qwen3:14b
Tamanho aproximado: 9.3 GB
```

Para baixar o modelo:

```
ollama pull qwen3:14b
```

Certifique-se de que o Ollama esteja rodando e acessível na URL configurada (por padrão `http://localhost:11434`).

---

## Subindo a aplicação

Com Docker e Docker Compose instalados, basta executar:

```
docker-compose up --build
```

Isso irá subir automaticamente:

- API principal com FastAPI e LangGraph (agents)
- Microserviço de cálculo matemático
- Frontend em Streamlit

### Portas utilizadas

- **Frontend (Streamlit):** `http://localhost:8501`
- **API principal (Agents):** `http://localhost:8080`
- **API Calculadora:** `http://localhost:8500`

---

> **Observação importante:** a explicação detalhada do código e da lógica de desenvolvimento **não está concentrada apenas neste README**. Cada diretório do projeto possui seu próprio arquivo `README.md`, onde são descritas as decisões técnicas, responsabilidades e lógica específica daquela parte do sistema.

## Arquitetura resumida

- **Frontend:** Interface simples de chat (Streamlit)
- **API:** Orquestra agentes, LLM e ferramentas
- **Planner Agent:** Decide se a pergunta é cálculo ou resposta direta
- **Executor Agent:** Executa ferramentas externas e formata respostas
- **LangGraph:** Controla o fluxo entre os agentes
- **Tool Calculator:** Microserviço isolado para operações matemáticas

Essa separação garante previsibilidade, facilidade de teste e menor acoplamento com o modelo.

---

## O que aprendi e o que faria diferente com mais tempo

Este projeto foi pensado como um **alicerce arquitetural**, não como um produto final. Com mais tempo, algumas evoluções naturais seriam aplicadas.

### Uso de Redis

Adicionar Redis permitiria:
- Cache de respostas
- Armazenamento de estado de conversas
- Rate limiting

Isso reduziria latência e custo de chamadas ao LLM.

---

### Guardrails

Implementaria **guardrails** para:
- Validar entradas do usuário
- Bloquear prompts maliciosos
- Garantir formato correto das respostas dos agentes

Isso aumentaria a segurança e confiabilidade do sistema.

---

### Agent como julgador (Evaluator / Judge)

Criaria um **agente avaliador** responsável por:
- Julgar a qualidade da resposta final
- Detectar inconsistências
- Decidir se a resposta deve ser refeita

Esse padrão melhora robustez em pipelines multi-agent.

---

### Pipeline de avaliação

Estruturaria um pipeline contínuo de avaliação para:
- Testar prompts
- Medir qualidade das respostas
- Comparar versões de agentes

Esse pipeline seria fundamental para evolução controlada do sistema.

---

### Observabilidade avançada com Langfuse e DeepEval

A integração com ferramentas como:
- **Langfuse** (observabilidade, tracing e métricas)
- **DeepEval** (avaliação automática de respostas)

permitiria acompanhar custo, latência e qualidade real das respostas em produção.

---

### MCP Server com FastMCP

Criaria um **MCP Server usando FastMCP** para:
- Centralizar ferramentas externas
- Facilitar integração com novos serviços
- Padronizar chamadas de ferramentas pelos agentes

Isso tornaria o sistema muito mais extensível.

---

### Processo de CI/CD com agentes

Implementaria um pipeline de CI/CD usando uma ferramenta consolidada como:
- **GitHub Actions**

Esse pipeline poderia incluir agentes para:
- Rodar testes
- Avaliar prompts
- Validar respostas automaticamente antes do deploy

---

### Processo de RAG

Para aumentar a inteligência e precisão do modelo em domínios específicos, adicionaria um pipeline de **RAG (Retrieval-Augmented Generation)**, permitindo:
- Consultar bases de conhecimento externas
- Responder perguntas fora do conhecimento treinado do modelo
- Reduzir alucinações

Essa evolução tornaria o sistema aplicável a cenários reais de negócio.

---

## Considerações finais

Este projeto demonstra uma abordagem prática para construção de sistemas com LLM:
- Sem depender exclusivamente do modelo
- Com controle explícito do fluxo
- Preparado para escalar em complexidade

Ele foi pensado para ser simples de entender, mas sólido o suficiente para evoluir.

