import json
from datetime import datetime, timedelta
from openai import OpenAI
import os


class Agent:
    def __init__(self, name, instructions, tools=[], mcp_servers=[], handoffs=[]):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.mcp_servers = mcp_servers
        self.handoffs = handoffs
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.total_turns = 0
        

    def run(self, user_input):
        observation = self.observe(user_input)
        orientation = self.orient(user_input, observation)
        decision = self.decide(user_input, observation, orientation)
        action = self.act(user_input, observation, orientation, decision)
        if self.total_turns < 3:
            self.total_turns += 1
            return self.run(user_input + " " + ",".join(action))
        else:
            return action

        
    def observe(self, user_input):
        ## get info about the world-
        ## weather
        weather = "sunny"
        ## the date
        date = datetime.now().strftime("%Y-%m-%d")
        print(f"Observation: {weather}, {date}")
        return weather, date
    
    def orient(self, user_input, observation):
        ## determine which tasks are due to be done soon
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
        ## determine which tasks are due to be done soon
        due_tasks = []
        for task_name, task in tasks.items():
            task["name"] = task_name
            if task.get("frequency") is None:
                task["frequency"] = "daily"
            if task.get("last_done") is None:
                task["last_done"] = datetime.now() - timedelta(days=365)
           
            if task["frequency"] == "daily":
                if task["last_done"] < datetime.now() - timedelta(days=1):
                    due_tasks.append(task)
            elif task["frequency"] == "weekly":
                if task["last_done"] < datetime.now() - timedelta(weeks=1):
                    due_tasks.append(task)
            elif task["frequency"] == "monthly":
                if task["last_done"] < datetime.now() - timedelta(days=30):
                    due_tasks.append(task)
            elif task["frequency"] == "yearly":
                if task["last_done"] < datetime.now() - timedelta(days=365):
                    due_tasks.append(task)
        print(f"Due tasks: {due_tasks}")
        return due_tasks
    
    def decide(self, user_input, observation, orientation):
        ## determine which tasks are appropriate to continue to remind the user to do
        ## use the llm to decide which ones, based on the currently due tasks
        prompt = f"""
        You are a reminder agent. There are a number of tasks that need to be done, that are important but not always urgent. Your role is to remind the user of these tasks.
        Here is the list of tasks, along with when they were last done, and how often they are due to be done.
        Trim down the list of tasks so that it's achievable in the next 3 hours, which is about how long each user can reasonably be expected to be able to work on tasks.
        Respond with a list of tasks, formatted as a JSON object.
        {observation}
        Tasks:
        {orientation}
        """
        response = self.llm.responses.create(
            model="gpt-4o",
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Which tasks are appropriate to continue to remind the user to do?"}
            ],
            text={"format": {"type": "json_object"}}
        )
        print(f"Decision: {response.output[0].content[0].text}")
        return response.output[0].content[0].text
    
    
    def act(self, user_input, observation, orientation, decision):
        ## actually remind the user to do the tasks
        ## generate tool calls to remind the user to do the tasks, using the llm to decide which tools to use
        prompt = f"""
        You are a reminder agent. 
        These are the most important tasks that need to be done, your role is to remind the user of these tasks.
        Send a reminder to the user to do each of these tasks.
        {observation}
        Tasks:
        {decision}
        """
        response = self.llm.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": prompt}
            ],
            tools=self.tools
        )
        tool_results = []
        ## if we got a tool call, call the tool
        if response.output[0]:
            for tool_call in response.output:
                tool_type = tool_call.type
                if tool_type == "function":
                    
                    tool_result = None
                    tool_name = tool_call["name"]
                    tool_args = tool_call["arguments"]
                    if tool_name == "remind_user":
                        tool_result = remind_user(tool_args["reminders"])
                        tool_results.append(tool_result)
                    elif tool_name == "add_task":
                        tool_result = add_task(tool_args["task"], tool_args["frequency"])   
                        tool_results.append(tool_result)
                    elif tool_name == "fetch_task_status":
                        tool_result = fetch_task_status(tool_args["task"])
                        tool_results.append(tool_result)
                
                    print(tool_result)
        print(response)
        return tool_results                
                    
                
    
    def handoff(self, user_input, observation):
        pass
    
    
def remind_user(task):
    print(f"Reminding user to do: {task}")
    ## send the user an email
    return "Email sent to user"

def add_task(task, frequency):
    ## add the task to tasks.json
    with open("tasks.json", "w") as f:
        tasks = json.load(f)
        tasks[task] = {"last_done": datetime.now().strftime("%Y-%m-%d"), "frequency": frequency}
        json.dump(tasks, f)
    return "Task added to database"

def fetch_task_status(task):
    ## fetch the status of the task from tasks.json
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
        return tasks[task]
    
reminder_agent = Agent(
    name="Reminder Agent",
    instructions="You are a reminder agent. There are a number of tasks that need to be done, that are important but not always urgent. Your role is to remind the user of these tasks.",
    tools=[{
        "type": "function",
        "name": "remind_user",
        "description": "Send a list of reminders to the user about their tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "reminders": {
                    "type": "string",
                    "description": "The task to be done"
                }
            },
            "required": [
                "reminders"
            ],
            "additionalProperties": False
        }
    }]
)


print(reminder_agent.run("What's on the docket for today?"))

## open the log file and log that we ran 
with open("log.txt", "a") as f:
    f.write(f"Reminder agent ran at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
