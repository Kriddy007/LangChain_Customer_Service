
!pip install langchain langchain-groq langchain-core -q

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool

llm = ChatGroq(
    api_key="api_key",
    model="llama3-groq-8b-8192-tool-use-preview"
)

@tool
def check_refund_status(transaction_id: str) -> str:
    """Check the refund status using a transaction ID starting with TXN."""
    refunds = {
        "TXN001": "Refund processed. Amount will reflect in 3-5 business days.",
        "TXN002": "Refund pending. Under review by the payments team.",
        "TXN003": "Refund rejected. Insufficient evidence provided."
    }
    return refunds.get(transaction_id, "Transaction ID not found.")

@tool
def get_account_status(account_id: str) -> str:
    """Get the account status using an account ID starting with ACC."""
    accounts = {
        "ACC001": "Account active. No issues detected.",
        "ACC002": "Account suspended due to suspicious activity.",
        "ACC003": "Account under verification. Limited access enabled."
    }
    return accounts.get(account_id, "Account ID not found.")

llm_with_tools = llm.bind_tools([check_refund_status, get_account_status])

def run_agent(user_message, history=[]):
    history.append(HumanMessage(content=user_message))

    response = llm_with_tools.invoke([
        SystemMessage(content="You are a helpful customer service agent. Use check_refund_status for transaction IDs starting with TXN. Use get_account_status for account IDs starting with ACC."),
        *history
    ])

    while response.tool_calls:
        history.append(response)

        for tool_call in response.tool_calls:
            if tool_call['name'] == 'check_refund_status':
                tool_result = check_refund_status.invoke(tool_call['args'])
            elif tool_call['name'] == 'get_account_status':
                tool_result = get_account_status.invoke(tool_call['args'])

            history.append(ToolMessage(
                content=tool_result,
                tool_call_id=tool_call['id']
            ))

        response = llm_with_tools.invoke([
            SystemMessage(content="You are a helpful customer service agent. Always give complete, clear answers."),
            *history
        ])

    history.append(AIMessage(content=response.content))
    return response.content, history

history = []

response, history = run_agent("Check refund for TXN001", history)
print(f"Agent: {response}\n")

response, history = run_agent("Check account ACC002", history)
print(f"Agent: {response}\n")



