# Service

Este diretório concentra toda a **inteligência do sistema**. É aqui que acontece a tomada de decisão, a orquestração entre agentes, a chamada ao LLM e a comunicação com serviços externos.

A ideia principal não é responder tudo com o modelo, mas **usar o LLM como um decisor**, mantendo regras claras, rastreabilidade e separação de responsabilidades.

---

## Visão Geral do Fluxo

1. O usuário envia uma pergunta.
2. O **PlannerAgent** analisa a intenção da pergunta.
3. Se for um cálculo, o fluxo segue para o **ExecutorAgent**.
4. O Executor chama um serviço externo de cálculo.
5. O resultado bruto é devolvido ao LLM apenas para **formatação**, não para raciocínio.
6. O grafo finaliza e retorna a resposta.

Todo esse fluxo é coordenado por um grafo explícito, e não por lógica condicional espalhada no código.

---

## Agents

### PlannerAgent

O Planner é responsável por **entender o que o usuário quer**, não por resolver o problema.

A função dele é:
- Receber a entrada do usuário
- Passar essa entrada para o LLM com um prompt bem restritivo
- Garantir que a saída seja **sempre um JSON estruturado**

O Planner decide apenas entre duas ações possíveis:
- `calculate`: quando identifica uma operação matemática
- `answer`: quando a pergunta pode ser respondida diretamente

Esse agente nunca executa cálculos e nunca decide como responder no formato final. Ele só classifica e extrai dados.

Além disso, existe uma camada defensiva forte de parsing para evitar respostas fora do padrão esperado do modelo.

---

### ExecutorAgent

O Executor entra em ação **somente quando o Planner decide que existe um cálculo**.

Responsabilidades principais:
- Receber os números e o operador já extraídos
- Chamar uma API externa especializada em cálculo
- Receber o resultado numérico bruto
- Pedir ao LLM apenas para **transformar esse resultado em uma frase final**

Ou seja: o LLM não calcula, não decide e não inventa. Ele só formata.

Isso reduz risco de erro, alucinação e inconsistência de resposta.

---

## Graph (Orquestração)

O diretório `graph` define explicitamente o fluxo da aplicação.

O grafo tem três características importantes:
- Um ponto de entrada claro (`planner`)
- Uma decisão condicional baseada no resultado do Planner
- Um encerramento explícito do fluxo

Se o Planner retornar `calculate`, o Executor é chamado. Caso contrário, o fluxo termina.

Essa abordagem evita encadeamentos implícitos e deixa o comportamento do sistema fácil de entender, debugar e evoluir.

---

## Infra

### LLMModel

Essa camada funciona como um **adaptador** entre o sistema e qualquer provedor de LLM.

Ela padroniza:
- A chamada assíncrona
- O formato da resposta
- A limpeza de tokens indesejados (como tags internas do modelo)

O restante do sistema não precisa saber se o modelo vem do Ollama, OpenAI ou outro provedor.

---

### OllamaClient

Cliente HTTP simples responsável por:
- Enviar prompts para o Ollama
- Controlar timeout e modelo
- Retornar apenas o texto gerado

Toda a lógica de observabilidade e logging é mantida aqui para facilitar diagnóstico.

---

### Logger e Observability

A aplicação já nasce instrumentada:
- Logs padronizados
- Tracing com OpenTelemetry
- Spans separados por agente, nó do grafo e chamadas externas

Isso permite entender exatamente:
- Onde o tempo está sendo gasto
- Onde falhas ocorrem
- Qual parte do fluxo foi executada

---

## MCP Client (Integração Externa)

O `mcp_client` é responsável por se comunicar com serviços externos, neste caso, a API de cálculo.

A regra aqui é clara:
- O sistema **não calcula internamente**
- Qualquer cálculo é delegado
- Falhas externas não quebram o sistema, retornam erro controlado

---

## Prompts

Os prompts são tratados como **artefatos versionados**, não como strings soltas no código.

### Técnicas Utilizadas

- **Prompt versioning**: permite evoluir o comportamento sem alterar código
- **Instruções restritivas**: o modelo tem menos liberdade, logo menos erro
- **Output controlado**: JSON obrigatório no Planner e texto curto no Executor
- **Separation of concerns**: cada prompt resolve um único problema

No Planner, o foco é **extração de intenção e dados estruturados**.
No Executor, o foco é **formatação de resposta**, não raciocínio.

Essa separação reduz drasticamente alucinação e aumenta previsibilidade.

---

## Conclusão

Este diretório implementa uma arquitetura de agentes pragmática:
- LLM como decisor, não como solução mágica
- Fluxo explícito e observável
- Serviços externos fazendo o trabalho crítico

O resultado é um sistema mais confiável, auditável e pronto para produção.