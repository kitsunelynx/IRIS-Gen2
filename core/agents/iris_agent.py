import os
from core.llms.gemini import Gemini
from google.genai import types
from dotenv import load_dotenv
from core.utils.logger import get_logger

load_dotenv()

class IRISAgent:
    def __init__(self, system_prompt: str, memory, config: dict, tools: list = None):
        """
        Initialize IRISAgent with system prompt, memory instance, configuration, and integrated tools.
        
        Parameters:
            system_prompt (str): The system prompt guiding the agent.
            memory: A persistent Memory instance for logging conversation.
            config (dict): Configuration dictionary with model settings.
            tools (list): List of callable tools/tools.
        """
        self.logger = get_logger()
        self.memory = memory if memory is not None else []  # Ensure memory is a list, not None.
        
        # Track tool names for status updates
        self.tools = tools or []
        
        generate_conf = config.get("generate_config", {})
        gemini_config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=self.tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=generate_conf.get("automatic_function_calling_disable", False)
            ),
            top_p=generate_conf.get("top_p", 0.6),
            seed=generate_conf.get("seed", 42),
            top_k=generate_conf.get("top_k", 64),
            temperature=generate_conf.get("temperature", 64)
        )
        model_name = config.get("model", "gemini-2.0-flash")
        self.gemini_agent = Gemini(model_name, gemini_config)
        
        # Status tracking
        self.status_callback = None
        self.gemini_agent.set_status_callback(self._handle_status_update)
    
    def _get_friendly_tool_name(self, function_name):
        """Convert function names to friendly tool names for status updates"""
        name_map = {
            "search": "Web Search",
            "research": "Research",
            "query_wolfram_alpha": "Wolfram Alpha",
            "grok_response": "Grok AI",
            "add_reminder": "Reminder System",
            "remove_reminder": "Reminder System",
            "get_current_datetime": "Date & Time",
            "store_memory": "Memory Storage",
            "write_persistent_memory": "Persistent Memory",
            "read_persistent_memory": "Persistent Memory",
        }
        return name_map.get(function_name, function_name.replace("_", " ").title())
    
    def set_status_callback(self, callback):
        """Set a callback function to be called when status changes"""
        self.status_callback = callback
    
    def _handle_status_update(self, status):
        """Handle status updates from the LLM and pass them to the callback"""
        if self.status_callback:
            self.status_callback(status)
    
    def send_message(self, message: str) -> str:
        """
        Send a user's message to Gemini, log the conversation in memory, and return the response.
        
        Parameters:
            message (str): The user's query.
        
        Returns:
            str: The agent's response.
        """
        try:
            # Log the user's message
            self.memory.append(f"User: {message}")
            
            # Update status to indicate we're processing
            self._handle_status_update("Processing your message...")
            
            # Send to Gemini (which will update status for tool usage)
            response = self.gemini_agent.send_message(message)
            
            if isinstance(response, str) and response.startswith("Error"):
                raise Exception(response)
            
            # Log agent's response
            self.memory.append(f"IRIS: {response}")
            
            # Clear status when done
            self._handle_status_update(None)
            
            return response
        except Exception as e:
            self.logger.error("[IRISAgent] Gemini error during send_message, falling back to alternative model.")
            try:
                self._handle_status_update("Falling back to alternative model...")
                fallback_agent = Gemini("gemini-1.5-flash", self.gemini_agent.config)
                fallback_agent.set_status_callback(self._handle_status_update)
                response = fallback_agent.send_message(message)
                self.memory.append(f"IRIS (fallback): {response}")
                self._handle_status_update(None)
                return response
            except Exception as e2:
                self.logger.error("[IRISAgent] Gemini fallback error")
                error_response = f"Error processing message: {e2}"
                self.memory.append(error_response)
                self._handle_status_update(f"Error: {str(e2)}")
                return error_response
    
    def execute_task(self, task: dict):
        """
        Execute a given task as defined in the task dictionary.
        
        Parameters:
            task (dict): Contains 'action' and its parameters.
        """
        action = task.get("action")
        parameters = task.get("parameters", {})
        self.logger.success(f"[IRISAgent] Executing task: {action} with parameters: {parameters}")
        if action == "run_command":
            command = parameters.get("command")
            if command:
                try:
                    from tools.cli_command import execute_command_tool
                    result = execute_command_tool(command)
                    self.logger.success(f"[IRISAgent] Command output: {result}")
                except Exception as e:
                    self.logger.error(f"[IRISAgent] Error executing command: {command}")
            else:
                self.logger.error("[IRISAgent] No command provided in task parameters.")

    def reset_chat(self):
        """
        Reset the Gemini chat session.
        
        This function will reset the Gemini agent's internal chat history.
        
        Returns:
            None
        """
        try:
            self.gemini_agent.reset_chat()
            self.logger.success("[IRISAgent] Chat reset successfully.")
        except Exception as e:
            self.logger.error(f"[IRISAgent] Error resetting Gemini chat: {e}") 