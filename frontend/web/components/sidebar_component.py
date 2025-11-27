"""
Sidebar UI Component (refactored - pure UI logic)
Agent status, navigation, settings and other sidebar UI rendering
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Callable
from frontend.web.utils.constants import (
    AGENTS_INFO,
    CSS_CLASS_AGENT_STATUS,
    CSS_CLASS_STATUS_ACTIVE,
    CSS_CLASS_STATUS_COMPLETED,
    COMPANY_LINK
)
from src.utils.agents import AgentManager


class SidebarComponent:
    """Sidebar UI Component"""
    
    def __init__(self):
        """Initialize component"""
        pass
    
    def render_agent_status(
        self, 
        container, 
        active_agent: Optional[str] = None,
        completed_agents: Optional[List[str]] = None
    ):
        """Display agent status
        
        Args:
            container: Container to display in
            active_agent: Currently active agent
            completed_agents: List of completed agents
        """
        if completed_agents is None:
            completed_agents = []
        
        # Manage placeholders
        if "agent_status_placeholders" not in st.session_state:
            st.session_state.agent_status_placeholders = {}
        
        # Check initial UI state maintenance
        is_initial_ui = st.session_state.get("keep_initial_ui", True)
        
        # Display each agent's status
        for agent in AGENTS_INFO:
            agent_id = agent["id"]
            agent_name = agent["name"]
            agent_icon = agent["icon"]
            
            # Create placeholder
            if agent_id not in st.session_state.agent_status_placeholders:
                st.session_state.agent_status_placeholders[agent_id] = container.empty()
            
            # Determine status class
            status_class = ""
            
            if not is_initial_ui:
                # Active agent (currently running)
                if agent_id == active_agent:
                    status_class = CSS_CLASS_STATUS_ACTIVE
                # Completed agent
                elif agent_id in completed_agents:
                    status_class = CSS_CLASS_STATUS_COMPLETED
            
            # Update status
            st.session_state.agent_status_placeholders[agent_id].html(
                f"<div class='{CSS_CLASS_AGENT_STATUS} {status_class}'>" +
                f"<div>{agent_icon} {agent_name}</div>" +
                f"</div>"
            )
    
    def render_model_info(self, model_info: Optional[Dict[str, Any]] = None):
        """Display current model information
        
        Args:
            model_info: Model information dictionary
        """
        if model_info:
            model_name = model_info.get('display_name', 'Unknown Model')
            provider = model_info.get('provider', 'Unknown')
            
            # Set colors based on theme
            is_dark = st.session_state.get('dark_mode', True)
            
            if is_dark:
                bg_color = "#1a1a1a"
                border_color = "#333333"
                text_color = "#ffffff"
                subtitle_color = "#888888"
                icon_color = "#4a9eff"
            else:
                bg_color = "#f8f9fa"
                border_color = "#e9ecef"
                text_color = "#212529"
                subtitle_color = "#6c757d"
                icon_color = "#0d6efd"
            
            st.markdown(f"""
            <div style="
                background: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 12px 16px;
                margin: 8px 0;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: all 0.2s ease;
            ">
                <div style="
                    color: {icon_color};
                    font-size: 18px;
                    line-height: 1;
                ">🤖</div>
                <div style="flex: 1; min-width: 0;">
                    <div style="
                        color: {text_color};
                        font-weight: 600;
                        font-size: 14px;
                        margin: 0;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    ">{model_name}</div>
                    <div style="
                        color: {subtitle_color};
                        font-size: 12px;
                        margin: 2px 0 0 0;
                        opacity: 0.8;
                    ">{provider}</div>
                </div>
                <div style="
                    width: 8px;
                    height: 8px;
                    background: #10b981;
                    border-radius: 50%;
                    flex-shrink: 0;
                "></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # If no model is selected
            is_dark = st.session_state.get('dark_mode', True)
            
            if is_dark:
                bg_color = "#1a1a1a"
                border_color = "#444444"
                text_color = "#888888"
                icon_color = "#666666"
            else:
                bg_color = "#f8f9fa"
                border_color = "#dee2e6"
                text_color = "#6c757d"
                icon_color = "#adb5bd"
            
            st.markdown(f"""
            <div style="
                background: {bg_color};
                border: 1px dashed {border_color};
                border-radius: 8px;
                padding: 12px 16px;
                margin: 8px 0;
                display: flex;
                align-items: center;
                gap: 12px;
                opacity: 0.7;
            ">
                <div style="
                    color: {icon_color};
                    font-size: 18px;
                    line-height: 1;
                ">🤖</div>
                <div style="flex: 1;">
                    <div style="
                        color: {text_color};
                        font-weight: 500;
                        font-size: 14px;
                        margin: 0;
                    ">No Model Selected</div>
                    <div style="
                        color: {text_color};
                        font-size: 12px;
                        margin: 2px 0 0 0;
                        opacity: 0.6;
                    ">Choose a model to start</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_navigation_buttons(self, callbacks: Dict[str, Callable] = None):
        """Render navigation buttons
        
        Args:
            callbacks: Button click callback functions
        """
        if callbacks is None:
            callbacks = {}
        
        # Change model button
        if st.button("🔁 Change Model", use_container_width=True):
            if "on_change_model" in callbacks:
                callbacks["on_change_model"]()
            else:
                st.switch_page("streamlit_app.py")
        
        # Chat history button
        if st.button("📋 Chat History", use_container_width=True):
            if "on_chat_history" in callbacks:
                callbacks["on_chat_history"]()
            else:
                st.switch_page("pages/02_Chat_History.py")
        
        # New chat button
        if st.button("✨ New Chat", use_container_width=True):
            if "on_new_chat" in callbacks:
                callbacks["on_new_chat"]()
        
        # Stop workflow button (only show when workflow is running)
        if st.session_state.get('workflow_running', False):
            if st.button("🛑 Stop Workflow", use_container_width=True, type="secondary"):
                if "on_stop_workflow" in callbacks:
                    callbacks["on_stop_workflow"]()
    
    def render_settings_section(self, callbacks: Dict[str, Callable] = None):
        """Render settings section
        
        Args:
            callbacks: Settings change callback functions
        """
        if callbacks is None:
            callbacks = {}
        
        st.markdown("### ⚙️ Settings")
        
        # Theme toggle
        if "on_theme_toggle" in callbacks:
            theme_manager = st.session_state.get('theme_manager')
            if theme_manager:
                theme_manager.create_theme_toggle(st)
        
        # Debug mode
        current_debug = st.session_state.get('debug_mode', False)
        debug_mode = st.checkbox("🐞 Debug Mode", value=current_debug)
        
        if debug_mode != current_debug:
            if "on_debug_mode_change" in callbacks:
                callbacks["on_debug_mode_change"](debug_mode)
    
    def render_session_stats(self, stats: Dict[str, Any]):
        """Display session statistics
        
        Args:
            stats: Session statistics data
        """
        with st.expander("📊 Session Stats", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages", stats.get("messages_count", 0))
                st.metric("Events", stats.get("events_count", 0))
            with col2:
                st.metric("Steps", stats.get("steps_count", 0))
                st.metric("Time", f"{stats.get('elapsed_time', 0)}s")
    
    def render_cost_tracking(self, executor_manager=None):
        """Display cost tracking information
        
        Args:
            executor_manager: ExecutorManager instance (optional, will check session_state if not provided)
        """
        from frontend.web.components.cost_display_component import display_session_cost, show_cost_warning
        
        with st.expander("💰 Cost Tracking", expanded=True):
            try:
                # Get executor_manager from parameter or session_state
                if executor_manager is None:
                    executor_manager = st.session_state.get('executor_manager')
                
                if not executor_manager:
                    st.info("⏳ Executor manager not initialized")
                    return
                
                # Check if executor exists
                if not hasattr(executor_manager, 'executor'):
                    st.info("⏳ Executor not found")
                    return
                    
                executor = executor_manager.executor
                if not executor:
                    st.info("⏳ Executor not initialized")
                    return
                
                # Try to get session metrics
                session_metrics = executor.get_session_metrics()
                
                if not session_metrics:
                    # Check why no metrics
                    if not hasattr(executor, '_thread_id') or not executor._thread_id:
                        st.info("💬 Start a conversation to begin cost tracking")
                    else:
                        st.info("💬 No cost data yet. Costs will appear after agent responses.")
                    return
                
                if session_metrics.get("total_calls", 0) == 0:
                    st.info("💬 No cost data yet. Costs will appear after agent responses.")
                    return
                
                # Display costs
                display_session_cost(session_metrics)
                show_cost_warning(session_metrics.get("total_cost", 0), threshold=0.10)
                
            except Exception as e:
                st.error(f"Cost tracking error: {str(e)}")
                if st.session_state.get('debug_mode'):
                    import traceback
                    st.code(traceback.format_exc())
    
    def render_debug_info(self, debug_info: Dict[str, Any]):
        """Display debug information
        
        Args:
            debug_info: Debug information data
        """
        if not st.session_state.get('debug_mode'):
            return
        
        with st.expander("🔍 Debug Info", expanded=False):
            st.markdown("**Session Info:**")
            session_info = {
                "user_id": debug_info.get("user_id", "Not set"),
                "thread_id": debug_info.get("thread_id", "Not set")[:8] + "..." if len(debug_info.get("thread_id", "")) > 8 else debug_info.get("thread_id", "Not set"),
            }
            st.json(session_info)
            
            if "logging" in debug_info:
                st.markdown("**Logging Info:**")
                st.json(debug_info["logging"])
    
    def render_complete_sidebar(
        self,
        model_info: Optional[Dict[str, Any]] = None,
        active_agent: Optional[str] = None,
        completed_agents: Optional[List[str]] = None,
        session_stats: Optional[Dict[str, Any]] = None,
        debug_info: Optional[Dict[str, Any]] = None,
        callbacks: Optional[Dict[str, Callable]] = None,
        executor_manager = None
    ):
        """Render complete sidebar
        
        Args:
            model_info: Model information
            active_agent: Active agent
            completed_agents: List of completed agents
            session_stats: Session statistics
            debug_info: Debug information
            callbacks: Callback functions
            executor_manager: ExecutorManager instance for cost tracking
        """
        with st.sidebar:
            # Agent status
            agents_container = st.container()
            self.render_agent_status(agents_container, active_agent, completed_agents)
            
            st.divider()
            
            # Current model info
            self.render_model_info(model_info)
            st.divider()
            
            # Navigation buttons
            self.render_navigation_buttons(callbacks)
            
            st.divider()
            
            # Settings section
            self.render_settings_section(callbacks)
            
            # Session statistics (if available)
            if session_stats:
                self.render_session_stats(session_stats)
            
            # Cost tracking
            self.render_cost_tracking(executor_manager)
            
            # Debug info (if available)
            if debug_info:
                self.render_debug_info(debug_info)
    
    def hide_sidebar(self):
        """Hide sidebar (using CSS)"""
        st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
            
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            
            /* Expand main content to full screen */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                max-width: none;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def show_back_button(self, callback: Callable = None, text: str = "← Back"):
        """Display back button
        
        Args:
            callback: Click callback function
            text: Button text
            
        Returns:
            bool: Whether the button was clicked
        """
        if st.button(text, use_container_width=True):
            if callback:
                callback()
                return True
            return True
        return False
