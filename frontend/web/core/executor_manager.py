"""
Executor Management Module (refactored)
- Executor initialization and configuration
- Swarm initialization based on model info
- Executor state management
"""

import streamlit as st
import asyncio
from typing import Optional, Dict, Any
import os
import sys

# Add project root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from frontend.web.core.executor import Executor

# Import logger (with graceful fallback)
try:
    from src.utils.logging.logger import get_logger
except ImportError:
    import logging
    def get_logger(name=__name__):
        return logging.getLogger(name)


class ExecutorManager:
    """Executor management class"""
    
    def __init__(self):
        """Initialize executor manager"""
        self.executor = None
        self._ensure_executor()
    
    def _ensure_executor(self):
        """Ensure executor instance"""
        if "direct_executor" not in st.session_state or st.session_state.direct_executor is None:
            st.session_state.direct_executor = Executor()
        
        self.executor = st.session_state.direct_executor
    
    def is_ready(self) -> bool:
        """Check if executor is ready"""
        self._ensure_executor()
        return self.executor.is_ready() if self.executor else False
    
    async def initialize_with_model(self, model_info: Dict[str, Any]) -> bool:
        """Initialize executor with model info
        
        Args:
            model_info: Model info dictionary
            
        Returns:
            bool: Initialization success
        """
        try:
            # Check logger initialization
            if "logger" not in st.session_state or st.session_state.logger is None:
                st.session_state.logger = get_logger()
            
            # Start logging session
            model_display_name = model_info.get('display_name', 'Unknown Model')
            session_id = st.session_state.logger.start_session(model_display_name)
            st.session_state.logging_session_id = session_id
            
            # Initialize executor
            self._ensure_executor()
            await self.executor.initialize_swarm(model_info)
            
            # Update state
            st.session_state.current_model = model_info
            st.session_state.executor_ready = True
            st.session_state.initialization_in_progress = False
            st.session_state.initialization_error = None
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to initialize AI agents: {str(e)}"
            
            st.session_state.executor_ready = False
            st.session_state.initialization_in_progress = False
            st.session_state.initialization_error = error_msg
            
            return False
    
    async def initialize_default(self) -> bool:
        """Initialize executor with default settings
        
        Returns:
            bool: Initialization success
        """
        try:
            # Check logger initialization
            if "logger" not in st.session_state or st.session_state.logger is None:
                st.session_state.logger = get_logger()
            
            # Initialize executor
            self._ensure_executor()
            await self.executor.initialize_swarm()
            
            # Update state
            st.session_state.executor_ready = True
            st.session_state.initialization_in_progress = False
            st.session_state.initialization_error = None
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to initialize AI agents: {str(e)}"
            
            st.session_state.executor_ready = False
            st.session_state.initialization_in_progress = False
            st.session_state.initialization_error = error_msg
            
            return False
    
    def reset(self):
        """Reset executor"""
        st.session_state.direct_executor = Executor()
        self.executor = st.session_state.direct_executor
        st.session_state.executor_ready = False
    
    def get_executor(self) -> Optional[Executor]:
        """Return current executor instance"""
        self._ensure_executor()
        return self.executor
    
    async def execute_workflow(self, user_input: str, config: Dict[str, Any]):
        """Execute workflow
        
        Args:
            user_input: User input
            config: Thread configuration
            
        Yields:
            Event stream
        """
        if not self.is_ready():
            raise RuntimeError("Executor not ready")
        
        # Log user input to logger
        if "logger" in st.session_state and st.session_state.logger:
            st.session_state.logger.log_user_input(user_input)
        
        # Execute workflow - pass config directly as dict
        async for event in self.executor.execute_workflow(user_input, config=config):
            yield event


# Global executor manager instance
_executor_manager = None

def get_executor_manager() -> ExecutorManager:
    """Return executor manager singleton instance"""
    global _executor_manager
    if _executor_manager is None:
        _executor_manager = ExecutorManager()
    return _executor_manager