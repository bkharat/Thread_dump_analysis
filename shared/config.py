"""
Configuration management for Thread Dump Analysis system
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for all agents"""
    
    # webMethods Integration Server
    WEBMETHODS_URL = os.getenv("WEBMETHODS_URL", "http://localhost:5555")
    WEBMETHODS_USER = os.getenv("WEBMETHODS_USER", "Administrator")
    WEBMETHODS_PASSWORD = os.getenv("WEBMETHODS_PASSWORD", "manage")
    
    # Slack Configuration
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#alerts")
    
    # AI Model Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
    
    # Thresholds
    HUNG_THREAD_THRESHOLD = int(os.getenv("HUNG_THREAD_THRESHOLD", "300"))  # 5 minutes
    CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", "80"))  # 80%
    MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD", "85"))  # 85%
    
    # Monitoring Configuration
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))  # 30 seconds
    
    # MCP Server Configuration
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8080"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.WEBMETHODS_URL:
            errors.append("WEBMETHODS_URL is required")
        
        if not cls.SLACK_WEBHOOK_URL:
            errors.append("SLACK_WEBHOOK_URL is required for notifications")
        
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            errors.append("Either OPENAI_API_KEY or ANTHROPIC_API_KEY is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True


# Create a singleton instance
config = Config()

# Made with Bob
