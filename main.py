from agents import Agent, Runner, WebSearchTool, CodeInterpreterTool, function_tool, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
import asyncio
import os
import subprocess
import datetime
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

with open("python_coder_system_prompt.md", "r") as file:
    system_prompt = file.read()
    print(system_prompt)
    
with open("code_reviewer_system_prompt.md", "r") as file:
    reviewer_system_prompt = file.read()
    print(reviewer_system_prompt)

        
@function_tool()
def run_command(command: str):
    ## first, always run the command in the agent_output directory
    os.chdir("/Users/annhoward/prompt_engineering_agents_and_tools/agent_output")
    ## check the command doesn't ask to leave this directory
    if "cd" in command:
        return "Error: The command cannot ask to leave the agent_output directory."
    if ".." in command:
        return "Error: The command cannot ask to leave the agent_output directory."
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

current_directory = os.getcwd()
system_prompt = RECOMMENDED_PROMPT_PREFIX + "\n\n" + system_prompt
reviewer_system_prompt = RECOMMENDED_PROMPT_PREFIX + "\n\n" + reviewer_system_prompt

system_prompt += f"You are currently in the directory {current_directory}/agent_output. You can't leave this directory."
system_prompt += f"The current date and time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
system_prompt += f"You are on a Macbook Pro M3 Max with 64GB of RAM, so write for this system."


async def main():
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", current_directory + "/agent_output"],
        }
    ) as server:
        async with MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@upstash/context7-mcp@latest"],
            }
        ) as ctx7server:
            
            
            code_reviewer_agent = Agent(
                name="Code Reviewer",
                instructions=reviewer_system_prompt,
                tools=[
                    WebSearchTool(),
                    run_command
                ],
                mcp_servers=[server, ctx7server],
            )
            
            code_writer_agent = Agent(
                name="Code Writer",
                instructions=system_prompt,
                tools=[
                    WebSearchTool(),
                    run_command
                ],
                mcp_servers=[server, ctx7server],
                handoffs=[code_reviewer_agent]
            )
            code_reviewer_agent.handoffs = [code_writer_agent]
            
            trace_id = gen_trace_id()
            with trace(workflow_name="Code Writer and Reviewer", trace_id=trace_id):
                
                result = await Runner.run(code_writer_agent, "Write me a Python script that will tell me what kind of video RAM is available on the system that I am on.",
                                          max_turns=50)
                print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())