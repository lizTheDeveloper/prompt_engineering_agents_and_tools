from agents import Agent, Runner, WebSearchTool, CodeInterpreterTool, function_tool
import asyncio


with open("python_coder_system_prompt.md", "r") as file:
    system_prompt = file.read()
    print(system_prompt)

## function that writes files to the local file system, given a file name and content
@function_tool()
def write_file(file_name: str, content: str):
    with open("./agent_output/" + file_name, "w") as file:
        file.write(content)


agent = Agent(
    name="Code Writer",
    instructions=system_prompt,
    tools=[
        WebSearchTool(),
        CodeInterpreterTool(
            tool_config={"type": "code_interpreter", "container": {"type": "auto"}},
        ),
        write_file
    ]
)

async def main():
    result = await Runner.run(agent, "Write an nltk program that can analyze the average sentence-by-sentence sentiment of a corpus of text and plot it as a graph with x as the ordinal value of the sentence within the text, and y as the sentiment score of the sentence.")
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())