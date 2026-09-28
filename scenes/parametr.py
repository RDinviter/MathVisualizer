
from manim import GrowFromCenter as Grow

ELASTIC = dict(run_time=3, rate_func=rate_functions.ease_out_elastic)

PROBLEM = (
    r"\linespread{1.3}\selectfont "
    r"Найдите все значения параметра $a$, при каждом их которых уравнение \\"
    r"$ax^4 + x^3 + (a^3 - 2a)x^2 + $"
    r"$(a^2 -2)x = ax^3 + x^2 + $"
    r"$(a^3 - 2a)x + a^2 - 2$ \\"
    r"имеет ровно 2 решения."
)


TRANSFORMATIONS = (
    r"ax^4 + x^3 + (a^3 - 2a)x^2 + (a^2 - 2)x - ax^3 - x^2 - (a^3 - 2a)x - a^2 + 2 = 0",
    r"ax^4 - ax^3 + x^3 - x^2 + ax^2(a^2 - 2) - ax(a^2 - 2) + x(a^2 - 2) - (a^2 - 2) = 0",
    r"(x - 1)(ax^3 + x^2) + (a^2 - 2)(ax^2 - ax + x - 1) = 0",
    r"x^2(x - 1)(ax + 1) + (a^2 - 2)(ax + 1)(x - 1) = 0",
    r"(x - 1)(ax + 1)(a^2 + x^2 - 2) = 0"
)

RESULT_1 = (
    r"\left[ \begin{gathered} "
    r"x - 1 = 0, \\ "
    r"ax + 1 = 0, \\ "
    r"x^2 + a^2 - 2 = 0 "
    r"\end{gathered} \right."  
)

RESULT_2 = (
    r"\left[ \begin{gathered} "
    r"x = 1, \\ "
    r"a = -\frac{1}{x}, \\ "
    r"x^2 + a^2 = 2 "
    r"\end{gathered} \right."
)
class Parametr(Scene):
    def construct(self):
        #Цвет фона
        self.camera.background_color = "#121440"

        #Условие задачи
        problem = Tex(
            PROBLEM,
            font_size=24, 
            tex_environment='flushleft', 
            tex_to_color_map = {
                "$ax^4 + x^3 + (a^3 - 2a)x^2 + $": YELLOW,
                "$(a^2 -2)x = ax^3 + x^2 + $": YELLOW,
                "$(a^3 - 2a)x + a^2 - 2$": YELLOW
            }
        )

        problem_rect = SurroundingRectangle(
            problem,
            color=YELLOW,
            buff=0.15,
            stroke_width=2
        )

        self.play(Grow(problem, **ELASTIC))        
        self.play(Create(problem_rect), run_time=1)

        problem_group = VGroup(
            problem, problem_rect
        )
        self.play(problem_group.animate.scale(0.8))
        self.play(problem_group.animate.to_corner(UL, buff=0.2))


        #Шаг первый
        step1 = Tex(
            r"\textbf{Решение.} Перенесём все слагаемые в левую часть \\",
            r"и разложим на множители:",
            font_size=20, color=WHITE, tex_environment="flushleft"
        )
        #Преобразования
        tranformations = MathTex(
            *TRANSFORMATIONS, 
            font_size=16
        )

        result_1 = MathTex(RESULT_1, font_size=24, color=WHITE)
        result_2 = MathTex(RESULT_2, font_size=24, color=YELLOW)
        res_group = VGroup(
            result_1,
            result_2
        ).arrange(RIGHT, aligned_edge=LEFT, buff=1.5)

        tranformations.arrange(DOWN, aligned_edge=LEFT, buff=0.20)

        #Группировка частей решения
        step_1_group = VGroup(
            step1, tranformations, res_group
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        step_1_group.next_to(
            problem_group,
            DOWN, 
            aligned_edge=LEFT,
            buff=0.3
        )

        step_1_group.shift(RIGHT * 0.3)

        #Анимации группы первого шага
        self.play(FadeIn(step1, shift=UP), run_time=1.5)
        self.wait(0.5)

        for line in tranformations:
            self.play(Write(line))
            self.wait(0.5)

        self.play(Grow(result_1, **ELASTIC))
        self.play(Write(result_2))

        self.wait()

        title = Tex(
            "Решим в осях XoA:",
            font_size=30
        )

        title.next_to(problem_group, RIGHT, buff=2)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2.4, 2.4, 1],
            y_range=[-2.4, 2.4, 1],
            x_length=7.5,
            y_length=7.5,
            axis_config={
                "include_numbers": True,
                "font_size": 22,
                "stroke_width": 2.5,
            },
            tips=False
        )
