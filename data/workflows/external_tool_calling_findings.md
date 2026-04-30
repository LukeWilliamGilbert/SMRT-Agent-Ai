# External Tool-Calling Documentation Findings

Author: **Manus AI**

This note captures key documentation facts used only to support the SMRT prompt-system forensic audit.

## n8n Tools Agent Documentation

Source: [n8n Tools AI Agent node documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/tools-agent/)

The n8n Tools Agent documentation states that the Tools Agent uses external tools and APIs to perform actions and retrieve information. It can understand the capabilities of different tools and determine which tool to use depending on the task. The page also states that the Tools Agent implements LangChain's tool-calling interface and that this interface describes available tools and their schemas. It identifies the System Message option as a place to guide the agent's decision-making and lists `Max Iterations` as defaulting to `10`.

## OpenAI Function / Tool Calling Documentation

Source: [OpenAI Function calling guide](https://developers.openai.com/api/docs/guides/function-calling)

The OpenAI function-calling guide states that tool calling starts by making a model request with tools it could call, then receiving a tool call, executing code, sending tool output back to the model, and receiving a final response. It describes function definitions as including a `description` field containing details on when and how to use the function. The guide recommends keeping the number of initially available functions small for higher accuracy, aiming for fewer than 20 functions available at the start of a turn as a soft suggestion. It also states that function definitions are injected into the system message in a syntax the model has been trained on, meaning callable function definitions count against the model context limit and are billed as input tokens.
