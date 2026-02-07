import random

EXERCISES = [
    "کشش گردن: سر را آرام به چپ و راست بچرخان. ۵ بار.",
    "چرخش شانه‌ها: شانه‌ها را دایره‌ای بچرخان. ۱۰ ثانیه.",
    "کشش ستون فقرات: دست‌ها را بالا ببر و بدن را بکش.",
]

MOTIVATIONAL_MESSAGES = [
    "ای انسان خسته از صندلی، برخیز.",
    "بدنت ابزار توست، از آن مراقبت کن.",
    "پنج دقیقه حرکت، یک ساعت عمر.",
]


def get_random_exercises(count: int = 2) -> list[str]:
    """Return random ergonomic exercises."""
    return random.sample(EXERCISES, k=min(count, len(EXERCISES)))


def get_random_message() -> str:
    """Return one short motivational message."""
    return random.choice(MOTIVATIONAL_MESSAGES)
