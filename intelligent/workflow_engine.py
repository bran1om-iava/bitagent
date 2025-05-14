from typing import Any, Dict, List, Optional, Callable


class WorkflowNode:
    """
    Represents a node (task/action) in a workflow DAG.
    """

    def __init__(self, node_id: str, action: Dict[str, Any], dependencies: Optional[List[str]] = None):
        self.node_id = node_id
        self.action = action
        self.dependencies = dependencies or []
        self.status = 'pending'  # could be 'pending', 'running', 'completed', 'failed'
        self.result: Any = None


class WorkflowEngine:
    """
    Manages and executes workflows (sequential or DAG-based) for agents.
    Handles task scheduling, dependency resolution, and execution.
    """

    def __init__(self):
        # workflow_id -> list of nodes
        self.workflows: Dict[str, List[WorkflowNode]] = {}
        self.results: Dict[str, Any] = {}  # workflow_id -> results

    def create_workflow(self, workflow_id: str, nodes: List[WorkflowNode]):
        """
        Registers a new workflow with the engine.
        """
        self.workflows[workflow_id] = nodes

    def get_ready_nodes(self, workflow_id: str) -> List[WorkflowNode]:
        """
        Returns nodes that are ready to run (all dependencies completed).
        """
        nodes = self.workflows.get(workflow_id, [])
        ready = []
        completed = {n.node_id for n in nodes if n.status == 'completed'}
        for node in nodes:
            if node.status == 'pending' and all(dep in completed for dep in node.dependencies):
                ready.append(node)
        return ready

    async def execute_workflow(self, workflow_id: str, agent_executor: Callable[[Dict[str, Any]], Any]):
        """
        Executes the workflow by running ready nodes, respecting dependencies.
        agent_executor: a coroutine that takes an action dict and returns a result.
        """
        nodes = self.workflows.get(workflow_id, [])
        while any(n.status == 'pending' for n in nodes):
            ready_nodes = self.get_ready_nodes(workflow_id)
            if not ready_nodes:
                break  # Deadlock or all running
            for node in ready_nodes:
                node.status = 'running'
                try:
                    node.result = await agent_executor(node.action)
                    node.status = 'completed'
                except Exception as e:
                    node.result = e
                    node.status = 'failed'
        self.results[workflow_id] = [n.result for n in nodes]
        return self.results[workflow_id]

    def get_workflow_status(self, workflow_id: str) -> Dict[str, str]:
        """
        Returns the status of all nodes in the workflow.
        """
        nodes = self.workflows.get(workflow_id, [])
        return {n.node_id: n.status for n in nodes}

    def get_workflow_results(self, workflow_id: str) -> List[Any]:
        """
        Returns the results of all nodes in the workflow.
        """
        return self.results.get(workflow_id, [])
