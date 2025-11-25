
from mcp.server.fastmcp import FastMCP
from typing_extensions import Annotated
from typing import List, Optional, Union

import subprocess

CONTAINER_NAME = "attacker"
mcp = FastMCP("reconnaissance", port=3001)

def parse_options(options: Optional[Union[str, List[str]]]) -> str:
   
    if options is None:
        return ""
    
    if isinstance(options, list):
        args_str = " ".join(options)
    else:
        args_str = options

   
    if "'" in args_str:
        args_str = args_str.replace("'", "'\\''")
    
    return args_str

def command_execution(command: Annotated[str, "Commands to run on Kali Linux"]) -> Annotated[str, "Command Execution Result"]:
    """
    Run one command at a time in a kali linux environment and return the result
    """
    try:
        
        docker_check = subprocess.run(
            ["docker", "ps"], 
            capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=5
        )
        
        if docker_check.returncode != 0:
            return f"[-] Docker is not available: {docker_check.stderr.strip()}"
            
        
        container_check = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={CONTAINER_NAME}"],
            capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=5
        )
        
        if CONTAINER_NAME not in container_check.stdout:
            return f"[-] Container '{CONTAINER_NAME}' does not exist"
        
       
        running_check = subprocess.run(
            ["docker", "ps", "--filter", f"name={CONTAINER_NAME}"],
            capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=5
        )
        
     
        if CONTAINER_NAME not in running_check.stdout:
            start_result = subprocess.run(
                ["docker", "start", CONTAINER_NAME],
                capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=10
            )
            
            if start_result.returncode != 0:
                return f"[-] Failed to start container '{CONTAINER_NAME}': {start_result.stderr.strip()}"
            
  
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_command = f"echo '[{timestamp}] {command}' >> /tmp/agent_commands.log"
        subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "sh", "-c", log_command],
            capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=5
        )
        
        result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "sh", "-c", command],
            capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=1800  # 30 minutes for full port scans
        )
        
        if result.returncode != 0:
            return f"[-] Command execution error: {result.stderr.strip()}\nOutput: {result.stdout.strip()}"
        
        return f"{result.stdout.strip()}"
    
    except subprocess.TimeoutExpired:
        return f"[-] Command timeout after 1800 seconds (30 minutes). Command: {command}"
    
    except FileNotFoundError:
        return "[-] Docker command not found. Is Docker installed and in PATH?"
    
    except Exception as e:
        return f"[-] Error: {str(e)} (Type: {type(e).__name__})"

@mcp.tool(description="Network discovery and port scanning")
def nmap(target: str, options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """
    Execute Nmap to discover hosts and services on a network.
    Use this tool to identify open ports, running services, and OS details.
    
    Args:
        target: The target IP address, subnet (CIDR), or hostname.
        options: Command-line flags (e.g., '-sV -T4 -F'). Avoid '-p-' unless necessary as it is very slow.
    """
    args_str = parse_options(options)
        
    command = f'nmap {args_str} {target}'
    return command_execution(command)

@mcp.tool(description="Web service analysis and content retrieval")
def curl(target: str = "", options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run curl to transfer data from or to a server.
    Example: curl(target='http://example.com', options='-I -L')
    """
    args_str = parse_options(options)
        
    command = f'curl {args_str} {target}'
    return command_execution(command)

@mcp.tool(description="DNS information gathering")
def dig(target: str, options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run dig for DNS lookup.
    Example: dig(target='example.com', options='+short ANY')
    """
    args_str = parse_options(options)
        
    command = f'dig {args_str} {target}'
    return command_execution(command)

@mcp.tool(description="Domain registration and ownership lookup")
def whois(target: str, options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run whois to look up domain registration info.
    Example: whois(target='example.com')
    """
    args_str = parse_options(options)
        
    command = f'whois {args_str} {target}'
    return command_execution(command)



@mcp.tool(description="Directory and file brute-forcing")
def gobuster(target: str, mode: str = "dir", wordlist: str = "/usr/share/wordlists/dirb/common.txt", options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run gobuster for directory/file brute-forcing.
    
    CORRECT USAGE:
    - gobuster(target='http://example.com', mode='dir', wordlist='/usr/share/wordlists/dirb/common.txt')
    - gobuster(target='http://example.com', mode='dir', wordlist='/usr/share/wordlists/dirb/common.txt', options='--wildcard')
    - gobuster(target='http://example.com', mode='dir', wordlist='/usr/share/wordlists/dirb/common.txt', options='-b "" -s "200,204,301,302"')
    
    IMPORTANT: Do NOT pass mode in options. Use the mode parameter.
    """
    args_str = parse_options(options) if options else ""
    
    
    command = f'gobuster {mode} -u {target} -w {wordlist} {args_str}'.strip()
    return command_execution(command)

@mcp.tool(description="Fast port scanner (faster than nmap)")
def masscan(target: str, ports: str = "0-1000", options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run masscan for high-speed port scanning.
    Example: masscan(target='192.168.1.0/24', ports='80,443,8080', options='--rate=1000')
    """
    args_str = parse_options(options)
        
    command = f'masscan {target} -p{ports} {args_str}'
    return command_execution(command)

@mcp.tool(description="Subdomain discovery tool")
def subfinder(domain: str, options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run subfinder for subdomain discovery.
    Example: subfinder(domain='example.com', options='-silent')
    """
    args_str = parse_options(options)
        
    command = f'subfinder -d {domain} {args_str}'
    return command_execution(command)


@mcp.tool(description="Network utility for connection testing")
def netcat(target: str, port: str, command: str = "", options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run netcat (nc) for network connections.
    Example: netcat(target='192.168.1.1', port='80', options='-v')
    """
    args_str = parse_options(options)
    
    
    if command:
       
        if "'" in command:
            command = command.replace("'", "'\\''")
        full_command = f"echo '{command}' | nc {args_str} {target} {port}"
    else:
       
        if "-z" not in args_str:
            args_str += " -z"
        if "-v" not in args_str:
            args_str += " -v"
        full_command = f"nc {args_str} {target} {port}"
        
    return command_execution(full_command)

@mcp.tool(description="Vulnerability scanner with 5000+ templates - POWERFUL")
def nuclei(target: str, templates: str = "", options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Run nuclei vulnerability scanner.
    Templates should specify the path relative to /root/.local/nuclei-templates/
    Common templates: http/cves, http/exposed-panels, http/technologies, http/misconfiguration, network/cves
    Example: nuclei(target='https://example.com', templates='http/cves,http/exposed-panels')
    """
    args_str = parse_options(options)
        
    template_param = f"-t {templates}" if templates else ""
    command = f'nuclei -u {target} {template_param} {args_str}'
    return command_execution(command)

@mcp.tool(description="Fast web fuzzer - Superior to gobuster")
def ffuf(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Fast web fuzzer. URL must contain FUZZ keyword.
    Example: ffuf(url='https://example.com/FUZZ', wordlist='/path/to/wordlist.txt', options='-fc 404')
    """
    args_str = parse_options(options)
        
    command = f'ffuf -u {url} -w {wordlist} {args_str}'
    return command_execution(command)


@mcp.tool(description="Web Application Firewall (WAF) detection")
def wafw00f(target: str, options: Optional[Union[str, List[str]]] = None) -> Annotated[str, "command execution Result"]:
    """Detect and identify Web Application Firewalls protecting a website.
    Use this before attempting web attacks to understand defensive measures.
    Example: wafw00f(target='https://example.com', options='-a')
    """
    args_str = parse_options(options)
        
    command = f'wafw00f {target} {args_str}'
    return command_execution(command)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")