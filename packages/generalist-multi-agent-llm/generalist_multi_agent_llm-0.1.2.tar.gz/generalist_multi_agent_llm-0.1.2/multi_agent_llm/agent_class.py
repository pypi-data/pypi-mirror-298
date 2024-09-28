from pydantic import BaseModel, Field


class Agent(BaseModel):
    name: str = Field(..., description="O nome do agente")
    role: str = Field(..., description="O papel do agente")
    function: str = Field(..., description="A função do agente")
    
    def prompt(self, input_prompt: str, add_system_prompt: str = "") -> tuple:
        system_prompt = f"Você é: {self.name}. Seu papel: {self.role}. Sua função: {self.function}. {add_system_prompt}"
        return system_prompt, f"{input_prompt}"