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
    goal="Evaluar hechos aleatorios y determinar si son útiles o inútiles",
    backstory="Eres un experto en clasificar información y determinar su valor práctico. "
              "Tu trabajo es analizar hechos curiosos y decidir si tienen alguna utilidad real.",
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
