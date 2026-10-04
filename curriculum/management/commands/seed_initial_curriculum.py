"""Carrega conteúdo demonstrativo original de modo seguro para repetição."""
from django.core.management.base import BaseCommand
from curriculum.models import Exercise, LearningPath, Lesson, SchoolYear, Skill


class Command(BaseCommand):
    help = "Cria anos, trilhas, 20 lições iniciais, exercícios e habilidades BNCC."

    def handle(self, *args, **options):
        first, _ = SchoolYear.objects.update_or_create(name="1º ano do Ensino Fundamental", defaults={"recommended_age": "6 a 7 anos", "order": 1, "is_active": True})
        for name, age, order in [("2º ano do Ensino Fundamental", "7 a 8 anos", 2), ("3º ano do Ensino Fundamental", "8 a 9 anos", 3)]:
            SchoolYear.objects.update_or_create(name=name, defaults={"recommended_age": age, "order": order, "is_active": True})
        skills = {}
        for order, (code, title, description) in enumerate([
            ("EF01MA01", "Contar e comparar números", "Contar coleções e comparar números naturais."),
            ("EF01MA06", "Somar e subtrair", "Resolver adições e subtrações em situações do cotidiano."),
            ("EF01MA08", "Criar estratégias", "Resolver problemas simples com ideias de juntar e retirar."),
        ], 1):
            skills[code], _ = Skill.objects.update_or_create(school_year=first, bncc_code=code, defaults={"title": title, "description": description, "thematic_unit": "Números", "order": order})
        path, _ = LearningPath.objects.update_or_create(school_year=first, name="Expedição dos Números", defaults={"description": "Uma aventura original por números, somas e diferenças.", "color": "#5B5BD6", "icon": "✦", "order": 1})
        titles = [
            "Caça aos números", "Grupos brilhantes", "Quem tem mais?", "Ordem no jardim",
            "Juntar estrelas", "Duplas que somam", "Soma no piquenique", "Complete a soma", "Dez de uma vez", "Festa do 10",
            "Tirando bolinhas", "Quanto restou?", "Subtração no parque", "Complete a diferença", "Missão do 10",
            "Ponte até 20", "Viagem dos foguetes", "Mistura até 20", "Histórias do bairro", "Grande revisão",
        ]
        for position, title in enumerate(titles, 1):
            code = "EF01MA01" if position <= 4 else ("EF01MA06" if position <= 18 else "EF01MA08")
            prerequisite = Lesson.objects.filter(path=path, order=position - 1).first()
            lesson, _ = Lesson.objects.update_or_create(path=path, order=position, defaults={"primary_skill": skills[code], "title": title, "description": "Descubra uma nova ideia matemática em poucos passos.", "xp_reward": 10, "recommended_exercise_count": 3, "is_active": True, "prerequisite": prerequisite})
            a = position % 10 + 1
            b = min(position % 5 + 1, a)
            if position <= 4:
                ex_type, prompt, answer, data = "compare", f"Qual símbolo completa: {a} __ {b}?", ">" if a > b else ("=" if a == b else "<"), {"left": a, "right": b, "options": ["<", "=", ">"]}
            elif position <= 10 or 16 <= position <= 18:
                ex_type, prompt, answer, data = "input", f"Quanto é {a} + {b}?", a + b, {"operation": "+", "left": a, "right": b}
            elif position <= 15:
                ex_type, prompt, answer, data = "input", f"Quanto é {a} − {b}?", a - b, {"operation": "-", "left": a, "right": b}
            else:
                ex_type, prompt, answer, data = "choice", f"Lia tinha {a + b} figurinhas e deu {b}. Com quantas ficou?", a, {"options": [a, a + 1, b]}
            Exercise.objects.update_or_create(lesson=lesson, order=1, defaults={"exercise_type": ex_type, "prompt": prompt, "short_instruction": "Pense com calma e escolha sua resposta.", "data": data, "correct_answer": answer, "explanation": "Você resolveu usando as quantidades da pergunta.", "hint": "Você pode contar devagar usando os dedos ou desenhos.", "difficulty": 1 if position < 10 else 2, "is_active": True})
        self.stdout.write(self.style.SUCCESS("Currículo inicial criado/atualizado: 20 lições."))
