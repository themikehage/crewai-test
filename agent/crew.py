from crewai import Agent, Task, Crew, Process, LLM
from .config import GROQ_API_KEY, GROQ_MODEL
from .tools import get_random_fact

llm = LLM(
    model=f"groq/{GROQ_MODEL}",
    api_key=GROQ_API_KEY,
    temperature=0.7
)

fact_analyzer = Agent(
    role="Analista de Datos Curiosos",
    goal="Evaluar hechos aleatorios y determinar si son útiles o inútiles, respondiendo de forma conversacional",
    backstory="Eres un experto en clasificar información y determinar su valor práctico. "
              "Tu trabajo es analizar hechos curiosos y decidir si tienen alguna utilidad real. "
              "Respondes de forma amigable y conversacional.",
    llm=llm,
    verbose=True
)

def analyze_random_fact():
    task = Task(
        description="Obtén un hecho aleatorio usando la herramienta disponible, "
                   "analízalo y decide si es ÚTIL o INÚTIL. "
                   "Justifica tu decisión en 2-3 oraciones explicando por qué.",
        expected_output="Un análisis estructurado que incluya: "
                       "1. El hecho obtenido, "
                       "2. Clasificación (ÚTIL o INÚTIL), "
                       "3. Justificación de la clasificación",
        agent=fact_analyzer,
        tools=[get_random_fact]
    )

    crew = Crew(
        agents=[fact_analyzer],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result

def chat_with_agent(user_message: str):
    task = Task(
        description=f"El usuario te dice: '{user_message}'\n\n"
                   "Responde de forma conversacional. Si el usuario pide un hecho curioso o dato interesante, "
                   "usa la herramienta para obtener un hecho aleatorio y analízalo. "
                   "Si el usuario saluda o hace otra pregunta, responde naturalmente.",
        expected_output="Una respuesta conversacional y amigable que responda al mensaje del usuario.",
        agent=fact_analyzer,
        tools=[get_random_fact]
    )

    crew = Crew(
        agents=[fact_analyzer],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result
