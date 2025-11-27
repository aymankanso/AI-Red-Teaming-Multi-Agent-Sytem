import streamlit as st
import asyncio
import os
import sys
import time
import warnings
import atexit


warnings.filterwarnings('ignore', category=RuntimeWarning, message='coroutine.*was never awaited')
warnings.filterwarnings('ignore', category=RuntimeWarning, message='.*Enable tracemalloc.*')

def _cleanup_async_tasks():
    """Cancel all pending asyncio tasks to prevent warnings on Streamlit refresh"""
    try:
        loop = asyncio.get_event_loop()
        if not loop.is_closed():
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
    except:
        pass  

atexit.register(_cleanup_async_tasks)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from frontend.web.utils.float import float_init

from frontend.web.components.chat_messages import ChatMessagesComponent
from frontend.web.components.terminal_ui import TerminalUIComponent
from frontend.web.components.sidebar_component import SidebarComponent
from frontend.web.components.theme_ui import ThemeUIComponent

from frontend.web.core.app_state import get_app_state_manager
from frontend.web.core.executor_manager import get_executor_manager
from frontend.web.core.workflow_handler import get_workflow_handler
from frontend.web.core.terminal_processor import get_terminal_processor

from frontend.web.utils.validation import check_model_required
from frontend.web.utils.constants import ICON, ICON_TEXT, COMPANY_LINK

from frontend.web.core.chat_replay import ReplayManager

app_state = get_app_state_manager()
executor_manager = get_executor_manager()  
workflow_handler = get_workflow_handler()
terminal_processor = get_terminal_processor()


theme_ui = ThemeUIComponent()
chat_messages = ChatMessagesComponent()
terminal_ui = TerminalUIComponent()
sidebar = SidebarComponent()


def main():
   
    try:
        app_state._initialize_session_state()
        app_state._initialize_user_session()
        app_state._initialize_logging()
    except Exception as e:
        st.error(f"App state initialization error: {str(e)}")
        return
    
    
    if not check_model_required():
        _show_model_required_message()
        return

    current_theme = "dark" if st.session_state.get('dark_mode', True) else "light"
    theme_ui.apply_theme_css(current_theme)
    float_init()
    terminal_ui.apply_terminal_css()

    st.title(":red[AI Red Teaming Multi-Agent]")

    _setup_sidebar()

    replay_manager = ReplayManager()
    if replay_manager.is_replay_mode():
        _handle_replay_mode(replay_manager)
        return

    _display_main_interface()


def _show_model_required_message():
    """Display model required message"""
    st.warning("⚠️ Please select a model first")
    if st.button("Go to Model Selection", type="primary"):
        st.switch_page("streamlit_app.py")


def _setup_sidebar():
    """Sidebar setup - using new components"""

    callbacks = {
        "on_change_model": lambda: st.switch_page("streamlit_app.py"),
        "on_chat_history": lambda: st.switch_page("pages/02_Chat_History.py"),
        "on_new_chat": _create_new_chat,
        "on_debug_mode_change": app_state.set_debug_mode,
        "on_stop_workflow": _force_stop_workflow
    }

    try:
        current_model = st.session_state.get('current_model')
        active_agent = st.session_state.get('active_agent')
        completed_agents = st.session_state.get('completed_agents', [])
        session_stats = app_state.get_session_stats()
        debug_info = app_state.get_debug_info()
    except Exception as e:
        st.error(f"Sidebar data load error: {str(e)}")

        current_model = None
        active_agent = None
        completed_agents = []
        session_stats = {"messages_count": 0, "events_count": 0, "steps_count": 0, "elapsed_time": 0, "active_agent": None, "completed_agents_count": 0}
        debug_info = {"user_id": "Error", "thread_id": "Error", "executor_ready": False, "workflow_running": False}
    

    sidebar.render_complete_sidebar(
        model_info=current_model,
        active_agent=active_agent,
        completed_agents=completed_agents,
        session_stats=session_stats,
        debug_info=debug_info,
        callbacks=callbacks,
        executor_manager=executor_manager
    )


def _display_main_interface():
    """Main interface - Full screen Chat + Floating Terminal"""
    

    if "terminal_visible" not in st.session_state:
        st.session_state.terminal_visible = True
    
    terminal_processor.initialize_terminal_state()
    

    if '_messages_backup' in st.session_state:
        st.session_state.structured_messages = st.session_state._messages_backup
        del st.session_state._messages_backup
    
   
    chat_height = app_state.get_env_config().get("chat_height", 700)
    chat_container = st.container(height=chat_height, border=False)
    
    with chat_container:
        messages_area = st.container()

        structured_messages = st.session_state.get('structured_messages', [])
        chat_messages.display_messages(structured_messages, messages_area)
    

    _handle_terminal_toggle()
    

    _render_floating_terminal()
    

    _handle_user_input(messages_area)


def _handle_terminal_toggle():
    """Handle terminal toggle button - independent of workflow"""

    is_disabled = st.session_state.get('workflow_running', False)
    
    toggle_clicked = terminal_ui.create_floating_toggle_button(
        st.session_state.terminal_visible,
        disabled=is_disabled
    )
    
    if toggle_clicked:

        st.session_state.terminal_visible = not st.session_state.terminal_visible
        

        if 'structured_messages' in st.session_state:
            st.session_state._messages_backup = st.session_state.structured_messages.copy()
        
        st.rerun()


def _render_floating_terminal():
    """Render floating terminal - conditionally display based on state"""
    if st.session_state.terminal_visible:
        terminal_history = terminal_processor.get_terminal_history()
        terminal_ui.create_floating_terminal(terminal_history)


def _handle_user_input(messages_area):
    """Handle user input - using new workflow handler"""
    
    if st.session_state.get('workflow_running', False):
        st.warning("⏳ Workflow is currently running. Please wait for it to complete, or click '🛑 Stop Workflow' in the sidebar.")
    
    user_input = st.chat_input("Type your red team request here...", disabled=st.session_state.get('workflow_running', False))
    
    if user_input and not st.session_state.get('workflow_running', False):
        
        validation_result = workflow_handler.validate_execution_state()
        if not validation_result["can_execute"]:
            st.error(validation_result["errors"][0] if validation_result["errors"] else "Cannot execute workflow")
            return
        
        user_message = workflow_handler.prepare_user_input(user_input)
        
        with messages_area:
            chat_messages.display_user_message(user_message)
        
        ui_callbacks = {
            "on_message_ready": lambda msg: _display_message_callback(msg, messages_area),
            "on_terminal_message": _terminal_message_callback,
            "on_workflow_complete": lambda: None,
            "on_error": lambda error: st.error(f"Workflow error: {error}")
        }
        

        try:

            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            

            result = loop.run_until_complete(
                workflow_handler.execute_workflow_logic(
                    user_input, ui_callbacks, terminal_ui
                )
            )
            

            if result is not None:
                if not result["success"] and result.get("error_message"):
                    st.error(result["error_message"])
            

            st.session_state.workflow_running = False
            

            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            

            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        
        except Exception as e:
            st.error(f"Workflow execution error: {str(e)}")
            st.session_state.workflow_running = False
        
        finally:

            st.rerun()


def _display_message_callback(message, messages_area):
    """Message display callback"""
    with messages_area:
        message_type = message.get("type", "")
        if message_type == "ai":
            chat_messages.display_agent_message(message, streaming=True)
        elif message_type == "tool":
            chat_messages.display_tool_message(message)


def _terminal_message_callback(tool_name, content):
    """Terminal message callback (simplified version)"""

    pass


def _create_new_chat():
    """Create new chat - changed from wrapper function to direct implementation"""
    try:
        conversation_id = app_state.create_new_conversation()
        executor_manager.reset()
        
        from src.utils.memory import clear_thread_checkpoint
        thread_id = st.session_state.thread_config.get("configurable", {}).get("thread_id")
        if thread_id:
            clear_thread_checkpoint(thread_id)
        
 
        if 'structured_messages' in st.session_state:
            st.session_state.structured_messages = []
        if 'event_history' in st.session_state:
            st.session_state.event_history = []
        if 'workflow_running' in st.session_state:
            st.session_state.workflow_running = False
        if 'active_agent' in st.session_state:
            del st.session_state.active_agent
        if 'completed_agents' in st.session_state:
            st.session_state.completed_agents = []
        

        current_model = st.session_state.get('current_model')
        if current_model:
            async def reinitialize():
                await executor_manager.initialize_with_model(current_model)
            
            
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            loop.run_until_complete(reinitialize())
        
        terminal_processor.clear_terminal_state()
        
        st.success("✨ New chat session started!")
        time.sleep(0.5)
        st.rerun()
        
    except Exception as e:
        st.error(f"Failed to create new chat: {str(e)}")


def _force_stop_workflow():
    """Force stop the current workflow execution"""
    try:
      
        st.session_state.workflow_running = False
    
        if 'event_history' in st.session_state:
            st.session_state.event_history = []
        

        st.warning("🛑 Workflow stopped. Background tasks may take a moment to cleanup. You can now send new commands.")
        time.sleep(0.3)
        st.rerun()
    except Exception as e:
        st.error(f"Failed to stop workflow: {str(e)}")


def _handle_replay_mode(replay_manager):
    """Handle replay mode - using ReplayManager"""

    float_init()
    terminal_ui.apply_terminal_css()
    
 
    if "terminal_visible" not in st.session_state:
        st.session_state.terminal_visible = True
    
    terminal_processor.initialize_terminal_state()
    

    chat_height = app_state.get_env_config().get("chat_height", 700)
    chat_container = st.container(height=chat_height, border=False)
    
    with chat_container:
        messages_area = st.container()
        
  
        replay_handled = replay_manager.handle_replay_in_main_app(
            messages_area, st.sidebar.container(), chat_messages, terminal_ui
        )
        
        if not replay_handled:

            st.error("Replay failed. Session data not found.")
    

    _handle_terminal_toggle()
    

    _render_floating_terminal()
    

    if st.session_state.get("replay_completed", False):
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Start New Chat", use_container_width=True, type="primary"):
              
                for key in ["replay_mode", "replay_session_id", "replay_completed"]:
                    st.session_state.pop(key, None)
            
                _create_new_chat()
           


if __name__ == "__main__":
    main()
