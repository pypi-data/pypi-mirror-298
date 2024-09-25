from enum import Enum

SDK_VERSION = "1.4.0"

class Provider(Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure-openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    AI21 = "ai21"
    CUSTOM_MODEL = "custom-model"