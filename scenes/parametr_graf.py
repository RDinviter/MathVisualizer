from manim import *
import numpy as np


ELASTIC = dict(run_time=3, rate_func=rate_functions.ease_out_elastic)

SQRT2 = np.sqrt(2)
BG_COLOR = "#121440"
CURVE_COLOR = GOLD_A
CURVE_WIDTH = 3
DOT_RADIUS = 0.10
DOT_STROKE = 1
PARAM_COLOR = RED
PARAM_WIDTH = 2
HIGHLIGHT_COLOR = BLUE
HIGHLIGHT_WIDTH = 2


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

ANALYSIS = (
    r"При $a < -\sqrt{2}$: 2 решения", 
    r"При $a = -\sqrt{2}$: 3 решения \\",
    r"При $a \in (-\sqrt{2}; -1 )$: 4 решения",
    r"При $a = -1$: 2 решения \\",
    r"При $a \in \left(-1; 0 \right)$: 4 решения",
    r"При $a = 0$: 3 решения \\",
    r"При $a \in \left(0; 1 \right)$: 4 решения",
    r"При $a = 1$: 2 решения \\",
    r"При $a \in \left(1; \sqrt{2} \right)$: 4 решения",
    r"При $a = \sqrt{2}$: 3 решения \\",
    r"При $a > \sqrt{2}$: 2 решения",
    r" "
)

PRE_FINAL = (
    r"При $a < -\sqrt{2}$: 2 решения",
    r"При $a = -1$: 2 решения \\",
    r"При $a = 1$: 2 решения \\",
    r"При $a > \sqrt{2}$: 2 решения",
)

FINAL = r"a \in \{-1;\, 1\} \cup (-\infty;\, -\sqrt{2}) \cup (\sqrt{2};\, +\infty)"


ANALYSIS_STEPS = [
    (-SQRT2, True),
    (-1, True),
    (0, True),
    (1, False),
    (SQRT2, True),
    (2.5, False)
]

class test(Scene):
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

        self.add(problem)        
        self.add(problem_rect)

        problem_group = VGroup(
            problem, problem_rect
        )
        self.add(problem_group.scale(0.8))
        self.add(problem_group.to_corner(UL, buff=0.2))


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
        self.add(step1)

        for line in tranformations:
            self.add(line)

        self.add(result_1)
        self.add(result_2)
        
        result_2.next_to(problem_group, DOWN, aligned_edge=LEFT)
        self.play(
            FadeOut(step_1_group, shift=UP),
            run_time=2)

        self.play(
            FadeIn(result_2, shift=UP),
            run_time=1)

        title = Tex(
            "Решим в осях xOa:",
            font_size=30
        )

        title.next_to(problem_group, RIGHT, buff=2)
        self.add(title)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=7,
            color=WHITE,
            axis_config={
                "include_numbers": True,
                "font_size": 22,
                "stroke_width": 2.5,
            },
            tips=True,
            x_axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
                },             
            y_axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,                
                "tick_size": 0.08,
                "font_size": 25, 
                }
        )

        axes.next_to(title, DOWN)

        self.play(Create(axes), run_time=6)

        circ = Circle(
            radius=axes.x_axis.get_unit_size() * SQRT2,
            stroke_width=5, 
            color=GOLD_A,
        ).move_to(axes.c2p(0, 0))
        self.play(Create(circ), run_time=3)
        self.wait(1.5)


        hyperbola_left = axes.plot(
            lambda x: -1 / x,
            x_range=[-3, -0.38],
            stroke_width=5,
            color=GOLD_A,
        )

        hyperbola_right = axes.plot(
            lambda x: -1 / x,
            x_range=[0.38, 3],
            stroke_width=5,
            color=GOLD_A,
        )
        self.play(Create(hyperbola_left), Create(hyperbola_right), run_time=3)
        self.wait(1.5)

        vertical_line = Line(
            axes.c2p(1, -3),
            axes.c2p(1, 3),
            stroke_width=5,
            color=GOLD_A,
        )

        self.play(Create(vertical_line), run_time=2)
        self.wait()

        #Создание прямой, зависящей от параметра
        a_value = ValueTracker(-2)


        def get_intersection_points():
            a = a_value.get_value()
            points = VGroup()

            dot1 = Dot(axes.c2p(1, a), color=BLUE, radius=0.08)
            points.add(dot1)
    
            if abs(a) > 0.01: 
                x_hyp = -1 / a
                if -3 <= x_hyp <= 3:
                    dot2 = Dot(axes.c2p(x_hyp, a), color=GREEN, radius=0.08)
                    points.add(dot2)
            
            
            if abs(a) <= SQRT2 + 0.1:
                discriminant = 2 - a**2
                if discriminant >= -0.01:         
                    x_circ = np.sqrt(max(0, discriminant))
                    dot3 = Dot(axes.c2p(x_circ, a), color=YELLOW, radius=0.08)
                    dot4 = Dot(axes.c2p(-x_circ, a), color=YELLOW, radius=0.08)
                    points.add(dot3, dot4)
            
            return points

        

        param_line = always_redraw(
           lambda: Line(
            axes.c2p(-3, a_value.get_value()),
            axes.c2p(3, a_value.get_value()),
            color=RED,
            stroke_width=5
            )
        )
        self.play(GrowFromCenter(param_line, **ELASTIC))

        intersection_dots = always_redraw(get_intersection_points)
        self.play(Create(intersection_dots))

        self.play(FadeOut(result_2), shift=UP)
        t = Tex("Анализ графика: ", font_size=24)
        t.next_to(problem_group, DOWN, aligned_edge=LEFT)
        self.play(Write(t))

        analysis = Tex(
            *ANALYSIS,
            font_size=20, 
            tex_to_color_map = {
                "2 решения": YELLOW
            }
        ).arrange(
            DOWN, aligned_edge=LEFT)

        analysis_group = VGroup(analysis)
        analysis_group.next_to(t, DOWN, aligned_edge=LEFT).shift(RIGHT)
        
        self.play(a_value.animate.set_value(ANALYSIS_STEPS[0][0]), run_time=2)
        self.play(Write(analysis[0]), Write(analysis[1]))
        self.play(Create(
            Line(
                axes.c2p(-3, -SQRT2), axes.c2p(3, -SQRT2), 
                stroke_width=HIGHLIGHT_WIDTH, color=HIGHLIGHT_COLOR
            )
        ))

        for i in range(1, len(ANALYSIS_STEPS)):
            a_target, show_line = ANALYSIS_STEPS[i]

            self.play(a_value.animate.set_value(a_target), run_time=2)
            self.play(Write(analysis[2 * i]), Write(analysis[2 * i + 1]))

            if show_line:
                self.play(Create(Line(
                    axes.c2p(-3, a_target), axes.c2p(3, a_target), 
                    stroke_width=HIGHLIGHT_WIDTH, color=HIGHLIGHT_COLOR
            )))

        self.play(
            FadeOut(param_line, shift=UP),
             FadeOut(intersection_dots, shift=UP)
        )

        pre_final = Tex(
            *PRE_FINAL, 
            color=YELLOW, 
            font_size=24, 
        )
        pre_final.arrange(
            DOWN,
            aligned_edge=LEFT
        )
        pre_final.next_to(
            problem_group, 
            DOWN,
            aligned_edge=LEFT
        )
        self.play(
            FadeOut(analysis, shift=UP),
            FadeOut(t, shift=UP),
            FadeIn(pre_final, shift=UP),
            run_time=5)

        final = MathTex(FINAL, font_size=30, color=YELLOW)
        final.next_to(pre_final, DOWN, aligned_edge=LEFT)

        self.play(Write(final), run_time=3)

        final_rect = SurroundingRectangle(
            final,
            color=YELLOW,
            buff=0.15,
            stroke_width=2
        )

        self.play(Create(final_rect), run_time=1.5)

        self.wait()
