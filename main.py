from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import ephem

app = FastAPI()

# ---------- MODELS ----------


class UserInput(BaseModel):
    name: str | None = None
    birth_date: str
    birth_time: str
    birth_place: str
    question: str


# ---------- MOON PHASE ----------


def get_moon_phase():
    moon = ephem.Moon()
    moon.compute(datetime.utcnow())
    phase = moon.phase  # 0 to 100

    if phase < 10:
        return "New Moon"
    elif phase < 45:
        return "Waxing Moon"
    elif phase < 55:
        return "Full Moon"
    else:
        return "Waning Moon"


# ---------- ALCHEMY ----------


def get_alchemical_stage(moon_phase: str):
    if moon_phase == "New Moon":
        return {
            "stage": "Nigredo",
            "focus": "Introspection and intention",
            "do": "Rest, observe, and set intentions.",
            "avoid": "Forcing decisions or rushing action.",
        }
    elif moon_phase == "Waxing Moon":
        return {
            "stage": "Albedo",
            "focus": "Clarity and construction",
            "do": "Organize plans and take consistent action.",
            "avoid": "Overthinking or waiting for perfection.",
        }
    elif moon_phase == "Full Moon":
        return {
            "stage": "Rubedo",
            "focus": "Awareness and culmination",
            "do": "Act consciously and express clearly.",
            "avoid": "Emotional reactions or impulsive choices.",
        }
    else:
        return {
            "stage": "Solve / Release",
            "focus": "Completion and letting go",
            "do": "Finish tasks and release what is no longer needed.",
            "avoid": "Starting new commitments.",
        }


# ---------- PLANET OF THE DAY ----------


def get_planet_of_the_day():
    weekday = datetime.utcnow().weekday()  # Monday = 0

    planets = {
        0: {
            "planet": "Moon",
            "theme": "Emotions, intuition, inner world",
            "do": "Care for emotional needs and observe feelings.",
            "avoid": "Overreacting or absorbing others' emotions.",
        },
        1: {
            "planet": "Mars",
            "theme": "Action, courage, initiative",
            "do": "Take decisive action and move forward.",
            "avoid": "Aggression or impulsive conflict.",
        },
        2: {
            "planet": "Mercury",
            "theme": "Communication, learning, thinking",
            "do": "Write, study, communicate, organize ideas.",
            "avoid": "Overthinking or miscommunication.",
        },
        3: {
            "planet": "Jupiter",
            "theme": "Expansion, meaning, growth",
            "do": "Seek understanding and broaden perspective.",
            "avoid": "Excess or unrealistic expectations.",
        },
        4: {
            "planet": "Venus",
            "theme": "Values, relationships, pleasure",
            "do": "Nurture relationships and self-worth.",
            "avoid": "People-pleasing or indulgence.",
        },
        5: {
            "planet": "Saturn",
            "theme": "Structure, responsibility, discipline",
            "do": "Organize responsibilities and set boundaries.",
            "avoid": "Procrastination or self-criticism.",
        },
        6: {
            "planet": "Sun",
            "theme": "Identity, vitality, purpose",
            "do": "Express yourself and take conscious leadership.",
            "avoid": "Ego-driven decisions.",
        },
    }

    return planets[weekday]


# ---------- API ENDPOINT ----------


@app.post("/guidance")
def get_guidance(data: UserInput):
    moon_phase = get_moon_phase()
    alchemy = get_alchemical_stage(moon_phase)
    planet = get_planet_of_the_day()

    return {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "moon_phase": moon_phase,
        "alchemical_stage": alchemy["stage"],
        "alchemical_focus": alchemy["focus"],
        "alchemical_do": alchemy["do"],
        "alchemical_avoid": alchemy["avoid"],
        "planet_of_the_day": planet["planet"],
        "planet_theme": planet["theme"],
        "planet_do": planet["do"],
        "planet_avoid": planet["avoid"],
    }
