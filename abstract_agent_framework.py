class Agent:
    def __init__(self, name, instructions, tools, mcp_servers, handoffs=None):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.mcp_servers = mcp_servers
        self.handoffs = handoffs
        

    def run(self, input):
        observation = self.observe(input)
        orientation = self.orient(input, observation)
        decision = self.decide(input, observation, orientation)
        action = self.act(input, observation, orientation, decision)
        return action
        
    def observe(self, input):
        pass
    
    def orient(self, input, observation):
        pass
    
    def decide(self, input, observation):
        pass
    
    def act(self, input, observation):
        pass
    
    def handoff(self, input, observation):
        pass