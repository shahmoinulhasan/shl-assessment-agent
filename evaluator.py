import json
from agent import get_agent_response

# Mock structure representing SHL's provided public conversation traces
MOCK_TEST_TRACES = [
    {
        "trace_id": "trace_01_java_dev",
        "history": [
            {"role": "user", "content": "I am hiring a Java developer who works with stakeholders"},
            {"role": "assistant", "content": "Sure. What is seniority level?"},
            {"role": "user", "content": "Mid-level, around 4 years"}
        ],
        "expected_assessments": ["Automated Coding Simulator (Java, Python, C++)", "Situational Judgement Test (SJT)"]
    }
]

def calculate_recall_at_k(recommended, expected, k=10):
    """Calculates the fraction of relevant assessments in top K choices."""
    top_k_rec = [rec["name"] for rec in recommended[:k]]
    if not expected:
        return 0.0
    
    matched = sum(1 for item in expected if item in top_k_rec)
    return matched / len(expected)

def run_offline_evaluation():
    print("=== Starting Offline Agent Evaluation ===")
    total_recall = 0.0
    
    # In a full run, you would loop through all 10 of SHL's public traces
    for trace in MOCK_TEST_TRACES:
        print(f"\nRunning Trace: {trace['trace_id']}")
        
        # Convert trace history into the structural format expected by the agent
        class MockMessage:
            def __init__(self, role, content):
                self.role = role
                self.content = content
            def dict(self):
                return {"role": self.role, "content": self.content}
                
        history_objs = [MockMessage(m["role"], m["content"]) for m in trace["history"]]
        
        # Run agent logic
        response = get_agent_response(history_objs)
        
        # Calculate Retrieval Quality Metrics
        recall = calculate_recall_at_k(response["recommendations"], trace["expected_assessments"], k=10)
        total_recall += recall
        
        print(f"Agent Reply: '{response['reply'][:50]}...'")
        print(f"Recommendations Returned: {len(response['recommendations'])}")
        print(f"Calculated Recall@10 for this trace: {recall * 100}%")
        
    mean_recall = total_recall / len(MOCK_TEST_TRACES)
    print(f"\n=== Evaluation Summary ===")
    print(f"Mean Recall@10 Across Traces: {mean_recall * 100}%")

if __name__ == "__main__":
    run_offline_evaluation()