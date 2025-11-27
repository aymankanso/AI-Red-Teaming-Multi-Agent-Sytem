
import asyncio
import uuid
import time
from datetime import datetime
from typing import Optional, Dict, Any, AsyncGenerator, Tuple

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from src.graphs.swarm import create_dynamic_swarm
from src.utils.llm.config_manager import (
    update_llm_config, 
    get_current_llm_config,
    get_current_llm
)
from src.utils.message import (
    extract_message_content,
    get_message_type,
    get_agent_name,
    parse_tool_name
)
from src.utils.metrics.cost_tracker import get_cost_tracker


class Executor:
    def __init__(self):
 
        self._initialized = False
        self._swarm = None
        self._config: Optional[RunnableConfig] = None
        self._thread_id = None
        self._current_model = None
        self._current_llm = None
        self._processed_message_ids = set()
        self._cost_tracker = get_cost_tracker()
    
    @property
    def swarm(self):
        return self._swarm
    
    @property
    def thread_id(self):
        return self._thread_id
    
    @property
    def current_model(self):
        return self._current_model
    
    async def initialize_swarm(self, model_info: Optional[Dict[str, Any]] = None, thread_config: Optional[Dict[str, Any]] = None):
        """Initialize swarm"""
        try:
           
            self._initialized = False
            self._swarm = None
            
            if thread_config:
               
                if isinstance(thread_config, dict) and "configurable" in thread_config:
                    self._config = RunnableConfig(
                        configurable=thread_config["configurable"],
                        recursion_limit=150
                    )
                    self._thread_id = thread_config["configurable"]["thread_id"]
                else:
                  
                    self._thread_id = str(uuid.uuid4())
                    self._config = RunnableConfig(
                        configurable={"thread_id": self._thread_id},
                        recursion_limit=150
                    )
            else:
               
                self._thread_id = str(uuid.uuid4())
                self._config = RunnableConfig(
                    configurable={"thread_id": self._thread_id},
                    recursion_limit=150
                )
            
           
            if model_info:
                self._current_model = model_info
                
                
                update_llm_config(
                    model_name=model_info['model_name'],
                    provider=model_info['provider'],
                    display_name=model_info['display_name'],
                    temperature=0.0
                )
            
           
            self._current_llm = get_current_llm()
            
           
            self._swarm = await create_dynamic_swarm()
            
          
            self._initialized = True
            
            return self._thread_id
            
        except Exception as e:
            self._initialized = False
            self._swarm = None
            raise Exception(f"Swarm initialization failed: {str(e)}")
    
    async def execute_workflow(self, user_input: str, config: Optional[Dict[str, Any]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute workflow
        """
        if not self.is_ready():
            raise Exception("Executor not ready - swarm not initialized")
        
     
        if self._swarm is None:
            raise Exception("Swarm is None - initialization failed")
        
      
        # Use provided config or fallback to instance config
        execution_config = config if config is not None else self._config
        
        # Initialize message ID tracking
        self._processed_message_ids = set()
        
        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        try:
            step_count = 0
            
            stream_result = self._swarm.astream(
                inputs,
                stream_mode="updates",
                config=execution_config,
                subgraphs=True
            )
            
            async for stream_item in stream_result:
                # Validate stream item is tuple
                if not isinstance(stream_item, tuple) or len(stream_item) != 2:
                    continue
                    
                namespace, output = stream_item
                step_count += 1
              
                if not isinstance(output, dict):
                    continue
                    
                for node, value in output.items():
                    # Determine agent name
                    agent_name = get_agent_name(namespace)
                    
                    # Process messages
                    if isinstance(value, dict) and "messages" in value and value["messages"]:
                        messages = value["messages"]
                        if messages and isinstance(messages, list):
                            latest_message = messages[-1]
                            should_display, message_type = self._should_display_message(
                                latest_message, agent_name, step_count
                            )
                            
                            if should_display:
                                # Track AI message costs
                                if message_type == "ai":
                                    self._track_message_cost(latest_message, agent_name)
                                
                                # Create event in format frontend can process
                                event_data = {
                                    "type": "message",
                                    "message_type": message_type,
                                    "agent_name": agent_name,
                                    "namespace": namespace,
                                    "content": extract_message_content(latest_message),
                                    "raw_message": latest_message,
                                    "step_count": step_count,
                                    "timestamp": datetime.now().isoformat()
                                }
                                
                                # Add tool info for tool messages
                                if message_type == "tool":
                                    tool_name = getattr(latest_message, 'name', 'Unknown Tool')
                                    event_data["tool_name"] = tool_name
                                    event_data["tool_display_name"] = parse_tool_name(tool_name)
                                
                                yield event_data
            
            # Completion signal
            yield {
                "type": "workflow_complete",
                "step_count": step_count,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _should_display_message(self, message, agent_name: str, step_count: int) -> Tuple[bool, Optional[str]]:
        """Determine whether to display message"""
        
        message_id = getattr(message, 'id', None)
        if not message_id:
            # If no ID, generate a unique ID to ensure we display the message
            # We trust that the stream and messages[-1] logic gives us the correct new message
            # Using content hash caused issues with duplicate messages (e.g. "hello" -> "hello")
            message_id = f"{agent_name}_{uuid.uuid4()}"
        
      
        if isinstance(message, HumanMessage):
            if message_id not in self._processed_message_ids:
                self._processed_message_ids.add(message_id)
                return True, "user"
            return False, None
        
        elif isinstance(message, AIMessage):
            if message_id not in self._processed_message_ids:
                self._processed_message_ids.add(message_id)
                return True, "ai"
            return False, None
        
        elif isinstance(message, ToolMessage):
            if message_id not in self._processed_message_ids:
                self._processed_message_ids.add(message_id)
                return True, "tool"
            return False, None
        
        return False, None
    
    def _track_message_cost(self, message: AIMessage, agent_name: str):
        """Track cost for an AI message"""
        try:
            # Extract token usage from message
            usage_metadata = getattr(message, 'usage_metadata', None)
            
            # Fallback to response_metadata if usage_metadata is missing
            if not usage_metadata and hasattr(message, 'response_metadata'):
                usage_metadata = message.response_metadata.get('token_usage') or message.response_metadata.get('usage')
            
            if not usage_metadata:
                return
            
            # Handle both object and dict access
            if isinstance(usage_metadata, dict):
                input_tokens = usage_metadata.get('input_tokens', 0)
                output_tokens = usage_metadata.get('output_tokens', 0)
            else:
                input_tokens = getattr(usage_metadata, 'input_tokens', 0)
                output_tokens = getattr(usage_metadata, 'output_tokens', 0)
            
            if input_tokens == 0 and output_tokens == 0:
                return
            
            # Get current model info
            model_info = self.get_current_model_info()
            
            # Track the call
            self._cost_tracker.track_call(
                session_id=self._thread_id or "unknown",
                agent_name=agent_name,
                model=model_info['model_name'],
                provider=model_info['provider'],
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=0.0  # TODO: Add latency tracking if needed
            )
        except Exception as e:
            # Log error but don't fail workflow
            print(f"Cost tracking error: {str(e)}")
            pass
    
    def get_current_model_info(self) -> Dict[str, str]:
        """Return current model info"""
        if self._current_model:
            return self._current_model
        
        try:
            config = get_current_llm_config()
            return {
                "display_name": config.display_name,
                "provider": config.provider,
                "model_name": config.model_name
            }
        except:
            return {
                "display_name": "Unknown Model",
                "provider": "Unknown",
                "model_name": "unknown"
            }
    
    async def change_model(self, model_info: Dict[str, Any]) -> bool:
        """Change model"""
        try:
            self._current_model = model_info
            
            update_llm_config(
                model_name=model_info['model_name'],
                provider=model_info['provider'],
                display_name=model_info['display_name'],
                temperature=0.0
            )
            
    
            self._current_llm = get_current_llm()
     
            self._swarm = await create_dynamic_swarm()
            
            return True
            
        except Exception as e:
            raise Exception(f"Model change failed: {str(e)}")
    
    def is_ready(self) -> bool:
        """Check execution ready state"""
        return (self._initialized and 
                self._swarm is not None and 
                hasattr(self._swarm, 'astream'))
    
    def reset_session(self) -> None:
        """Initialize session"""
        self._thread_id = None
        self._config = None
        self._processed_message_ids = set()
        self._initialized = False
    
    def get_state_dict(self) -> Dict[str, Any]:
        """Return state as dictionary (for session saving)"""
        session_cost = self._cost_tracker.get_session_cost(self._thread_id) if self._thread_id else None
        
        return {
            "initialized": self._initialized,
            "thread_id": self._thread_id,
            "current_model": self._current_model,
            "has_swarm": self._swarm is not None,
            "session_cost": session_cost
        }
    
    def get_session_metrics(self) -> Optional[Dict]:
        """Get cost metrics for current session"""
        if not self._thread_id:
            return None
        return self._cost_tracker.get_session_cost(self._thread_id)
    
    def get_cost_summary(self) -> Dict:
        """Get overall cost summary across all sessions"""
        return self._cost_tracker.generate_summary()