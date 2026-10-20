// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AIGuardian - On-Chain Audit & Emergency Kill-Switch for Autonomous AI Agents
 */
contract AIGuardian {
    address public owner;

    enum AgentStatus { Active, Suspended, Terminated }

    struct Agent {
        string agentId;
        AgentStatus status;
        uint256 lastHeartbeat;
        uint256 violationCount;
    }

    mapping(bytes32 => Agent) public agents;
    
    event AgentRegistered(bytes32 indexed agentHash, string agentId);
    event SafetyViolationLogged(bytes32 indexed agentHash, string reason, uint256 timestamp);
    event KillSwitchTriggered(bytes32 indexed agentHash, string reason);
    event ExecutionLogged(bytes32 indexed agentHash, bytes32 executionHash, bool passedGuardrails);

    modifier onlyOwner() {
        require(msg.sender == owner, "Unauthorized: Only Governance Owner");
        _;
    }

    modifier onlyActive(bytes32 agentHash) {
        require(agents[agentHash].status == AgentStatus.Active, "Agent is not active");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerAgent(string memory agentId) external onlyOwner returns (bytes32) {
        bytes32 agentHash = keccak256(abi.encodePacked(agentId, block.timestamp));
        agents[agentHash] = Agent({
            agentId: agentId,
            status: AgentStatus.Active,
            lastHeartbeat: block.timestamp,
            violationCount: 0
        });
        emit AgentRegistered(agentHash, agentId);
        return agentHash;
    }

    function logExecution(
        bytes32 agentHash,
        bytes32 executionHash,
        bool passedGuardrails,
        string memory violationReason
    ) external onlyActive(agentHash) {
        agents[agentHash].lastHeartbeat = block.timestamp;

        if (!passedGuardrails) {
            agents[agentHash].violationCount += 1;
            emit SafetyViolationLogged(agentHash, violationReason, block.timestamp);

            if (agents[agentHash].violationCount >= 3) {
                agents[agentHash].status = AgentStatus.Terminated;
                emit KillSwitchTriggered(agentHash, "Maximum violation threshold exceeded");
            }
        }

        emit ExecutionLogged(agentHash, executionHash, passedGuardrails);
    }

    function triggerEmergencyKillSwitch(bytes32 agentHash, string memory reason) external onlyOwner {
        agents[agentHash].status = AgentStatus.Terminated;
        emit KillSwitchTriggered(agentHash, reason);
    }
}
