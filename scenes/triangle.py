from manim import *
import numpy as np
from manim import GrowFromCenter as Grow

ELASTIC = dict(run_time=3, rate_func=rate_functions.ease_out_elastic)


def setup_problem(
        scene,
        text,
        font_size=24,
        rect_color=YELLOW,
        rect_buff=0.15,
        rect_stroke_width=2,
        scale_factor=0.8,
        corner=UL,
        corner_buff=0.2,
        tex_to_color_map=None,
):
    """
    Показывает условие задачи, обрамляет его рамкой и уводит в угол.

    Возвращает:
        problem_group — VGroup с условием и рамкой (для дальнейшего использования)
    """
    # Создаём текст условия
    problem = Tex(
        text,
        font_size=font_size,
        tex_environment='flushleft',
        tex_to_color_map=tex_to_color_map or {}
    )

    # Рамка вокруг условия
    problem_rect = SurroundingRectangle(
        problem,
        color=rect_color,
        buff=rect_buff,
        stroke_width=rect_stroke_width
    )

    # Анимация появления
    scene.play(Grow(problem, **ELASTIC))
    scene.play(Create(problem_rect), run_time=1)

    # Группируем и уводим в угол
    problem_group = VGroup(problem, problem_rect)
    scene.play(problem_group.animate.scale(scale_factor))
    scene.play(problem_group.animate.to_corner(corner, buff=corner_buff))

    return problem_group


def project_point_onto_line(P, A, B):
    """проекция точки P на прямую, заданную точками A и B"""
    v = B - A
    w = P - A
    t = np.dot(w, v) / np.dot(v, v)
    return A + t * v


def get_unit_vector(v):
    """Возвращает единичный вектор того же направления"""
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-6 else v


def line_intersection(p1, v1, p2, v2):
    """Находит точку пересечения двух"""
    # p1 + t*v1 = p2 + s*v2  =>  t*v1 - s*v2 = p2 - p1
    A_mat = np.column_stack([v1[:2], -v2[:2]])
    b_vec = (p2 - p1)[:2]

    det = np.linalg.det(A_mat)
    if abs(det) < 1e-6:
        return None  # Прямые параллельны

    t, s = np.linalg.solve(A_mat, b_vec)
    # Возвращаем точку с z=0
    return np.array([p1[0] + t * v1[0], p1[1] + t * v1[1], 0])


PROBLEM = '''Окружность с центром O, вписанная в треугольник ABC, касается сторон AB и BC в точках P и Q соответственно. В четырёхугольник BPOQ можно вписать окружность. Найдите угол ABC, если известно, что радиус этой окружности вдвое меньше радиуса вписанной окружности треугольника ABC. Ответ дайте в градусах.'''

SOLVE_1 = (
    r"Построим $\triangle$ABC\\",
    r"Впишем окружность в $\triangle$ABC, центр - точка $O$\\",
    r"Построим касательные OP и OQ\\",
    r"Впишем окружность в четырехугольник BPOQ\\",
    r"(центр вписанной окружности - точка пересечения биссектрис)\\",
    r"Требуется найти $\angle$ABC\\",
    r"Известно, что $R=2\cdot r$\\",
)

SOLVE_2 = (
    r"Решение\\",
    r"Пусть $r$ - радиус окружности, вписанной в BPOQ\\",
    r"Тогда радиус окружности O равен $2\cdot r$\\",
    r"Если окружность с центром $O_1$, вписанная в четырёхугольник "
    r"BPOQ, касается его стороны OP в точке F, а стороны BP — в точке E, "
    r"то $O_1F \perp OP$, $O_1F = r$, $O_1E \perp BP$, $FP = O_1E = r$, "
    r"$OF = OP - FP = 2r - r = r$.\\",
    r"Из прямоугольного $\triangle OFO_1$ находим, что $\angle FO_1O = \angle FOO_1 = 45^\circ$. \\"
    r"Тогда $\angle OBQ = \angle OBP = 45^\circ$. Следовательно, $\angle ABC = 2\angle OBP = 90^\circ$."
)


class Triangle(Scene):
    def construct(self):
        problem_group = setup_problem(
           self,
           PROBLEM,
           font_size=24
        )

        A = Dot(3 * LEFT + 1.5 * DOWN)
        B = Dot(1.5 * DR + RIGHT)
        C = Dot(1.2 * UP + 1.2 * UR)

        A_text = Tex("$A$", color=YELLOW, font_size=34).next_to(A, DL, buff=0.1)
        B_text = Tex("$B$", color=YELLOW, font_size=34).next_to(B, DR, buff=0.1)
        C_text = Tex("$C$", color=YELLOW, font_size=34).next_to(C, UR, buff=0.1)

        A_coord = A.get_center()
        B_coord = B.get_center()
        C_coord = C.get_center()

        a = np.linalg.norm(B_coord - C_coord)
        b = np.linalg.norm(C_coord - A_coord)
        c = np.linalg.norm(A_coord - B_coord)

        I_coord = (a * A_coord + b * B_coord + c * C_coord) / (a + b + c)
        incenter = Dot(I_coord, color=RED, radius=0.05)

        O_text = Tex("$O$", color=YELLOW, font_size=34).next_to(incenter, UL, buff=0.1)

        p = (a + b + c) / 2
        area = np.sqrt(p * (p - a) * (p - b) * (p - c))
        r = area / p

        incircle = Circle(radius=r, color=BLUE, stroke_width=3).move_to(I_coord)

        AB = Line(A_coord, B_coord, color=WHITE)
        BC = Line(B_coord, C_coord, color=WHITE)
        CA = Line(C_coord, A_coord, color=WHITE)

        # === НОВОЕ: точки касания ===
        T_AB = project_point_onto_line(I_coord, A_coord, B_coord)
        T_BC = project_point_onto_line(I_coord, B_coord, C_coord)

        # Маленькие точки в местах касания
        P = Dot(T_AB, color=GREEN, radius=0.04)
        Q = Dot(T_BC, color=GREEN, radius=0.04)

        P_text = Tex("$P$", color=YELLOW, font_size=34).next_to(P, DOWN, buff=0.1)
        Q_text = Tex("$Q$", color=YELLOW, font_size=34).next_to(Q, UR, buff=0.1)

        # Радиусы от центра к точкам касания
        OP = Line(I_coord, T_AB, color=YELLOW)
        OQ = Line(I_coord, T_BC, color=YELLOW)

        APO_angle = RightAngle(
            Line(P.get_center(), A.get_center()),
            Line(P.get_center(), I_coord),
            color=YELLOW,
            length=0.2
        )

        OQC_angle = RightAngle(
            Line(Q.get_center(), I_coord),
            Line(Q.get_center(), C_coord),
            color=YELLOW,
            length=0.2

        )

        ABC_angle = Angle(
            Line(B_coord, C_coord),
            Line(B_coord, A_coord),
            color=WHITE
        )


        # Координаты вершин четырехугольника
        O_coord = I_coord
        P_coord = T_AB
        B_coord = B_coord
        Q_coord = T_BC

        # Найдем направление бисс. угла Р
        dir_PO = get_unit_vector(O_coord - P_coord)
        dir_PB = get_unit_vector(B_coord - P_coord)
        bis_P_dir = get_unit_vector(dir_PO + dir_PB)

        # Найдем направление бисс. угла Q
        dir_QO = get_unit_vector(O_coord - Q_coord)
        dir_QB = get_unit_vector(B_coord - Q_coord)
        bis_Q_dir = get_unit_vector(dir_QO + dir_QB)

        # Найдем инцентр OPBQ
        O1 = line_intersection(
            P_coord, bis_P_dir,
            Q_coord, bis_Q_dir)
        O1 = np.array([O1[0], O1[1], 0])

        T_new = project_point_onto_line(O1, P_coord, B_coord)
        r_new = np.linalg.norm(O1 - T_new)

        bis_P_line = Line(P_coord, P_coord + 2.5 * bis_P_dir, color=WHITE)
        bis_Q_line = Line(Q_coord, Q_coord + 2.5 * bis_Q_dir, color=WHITE)

        incenter_new = Dot(O1, color=RED, radius=0.05)
        O_new_text = Tex(r"$O_1$", color=YELLOW, font_size=34).next_to(incenter_new, UR, buff=0.1)

        incircle_new = Circle(radius=r_new, color=BLUE, stroke_width=3).move_to(O1)

        E = project_point_onto_line(O1, A_coord, B_coord)
        E = Dot(E, color=GREEN, radius=0.04)

        F = project_point_onto_line(O1, I_coord, P_coord)
        F = Dot(F, color=GREEN, radius=0.04)

        F_text = Tex("$F$", color=YELLOW, font_size=34).next_to(F, LEFT, buff=0.1)
        E_text = Tex("$E$", color=YELLOW, font_size=34).next_to(E, DOWN, buff=0.1)

        O1F = Line(O1, F, color=YELLOW)
        O1E = Line(O1, E, color=YELLOW)

        AEO1_angle = RightAngle(
            Line(E.get_center(), A.get_center()),
            Line(E.get_center(), O1),
            color=YELLOW,
            length=0.2
        )

        O1FP_angle = RightAngle(
            Line(F.get_center(), O1),
            Line(F.get_center(), P.get_center()),
            color=YELLOW,
            length=0.2
        )

        R_text_1 = Tex("$R$", font_size=34, color=WHITE)
        R_text_1.next_to(OP.get_center(), LEFT+DOWN, buff=0.1)

        R_text_2 = Tex("$R$", font_size=34, color=WHITE)
        R_text_2.next_to(OQ.get_center(), UP, buff=0.1)


        r_text_1 = Tex("$r$", font_size=34, color=WHITE)
        r_text_1.next_to(O1E.get_center(), LEFT, buff=0.1)

        r_text_2 = Tex("$r$", font_size=34, color=WHITE)
        r_text_2.next_to(O1F.get_center(), DOWN, buff=0.1)


        OB = Line(I_coord, B, color=WHITE)

        solve_1 = Tex(
            *SOLVE_1,
            font_size=16,
        )

        solve_2 = Tex(
            *SOLVE_2,
            font_size=16,
            tex_environment='flushleft',
            tex_to_color_map={
                "Решение": GOLD,
            }
        )

        solve_1.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        text_group_1 = VGroup(solve_1)
        text_group_1.next_to(problem_group, DOWN, buff=0.5, aligned_edge=LEFT)

        solve_2.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        text_group_2 = VGroup(solve_2)
        text_group_2.next_to(problem_group, DOWN, buff=0.5, aligned_edge=LEFT)

        answer_text = Tex(
            r"Ответ: $90^\circ$",
            font_size=24,
            tex_environment='flushleft',
            color=WHITE
        )

        # Рамка вокруг ответа
        answer_rect = SurroundingRectangle(
            answer_text,
            color=YELLOW,
            buff=0.2,
            stroke_width=2
        )

        # Группируем и помещаем в левый нижний угол
        answer_group = VGroup(answer_text, answer_rect)
        answer_group.to_corner(DL, buff=0.3)

        """Появление треугольника и подписей"""
        self.play(Write(solve_1[0]))
        self.play(Indicate(solve_1[0]), scale=1.5)

        self.play(
            Create(A),
            Create(B),
            Create(C),
            Create(AB),
            Create(BC),
            Create(CA)
        )
        self.wait(0.5)
        self.play(
            Write(A_text),
            Write(B_text),
            Write(C_text)
        )

        """Анимация построения окружности"""
        self.play(Write(solve_1[1]))
        self.play(Indicate(solve_1[1]), scale=1.5)

        self.play(Create(incenter))
        self.play(Indicate(incenter), scale_factor=1.5, run_time=1)
        self.play(Create(incircle), Write(O_text))
        self.wait(0.5)


        """Анимация построения касательных"""
        self.play(Write(solve_1[2]))
        self.play(Indicate(solve_1[2]), scale=1.5)

        self.play(Create(OP), Create(OQ))
        self.wait(0.5)
        self.play(Write(P_text), Write(Q_text))
        self.play(Create(OQC_angle), Create(APO_angle))
        self.play(Write(R_text_2), Write(R_text_1))
        self.wait(0.5)


        """Построение бисскетрис и окружности"""
        self.play(Write(solve_1[3]))
        self.play(Write(solve_1[4]))
        self.play(Indicate(solve_1[4]), scale=2, run_time=1.5)

        self.play(Create(bis_Q_line), Create(bis_P_line))
        self.wait(0.5)
        self.play(Create(incenter_new))
        self.play(Flash(incenter_new, color=YELLOW, line_length=0.3, run_time=1))
        self.play(Create(incircle_new))
        self.play(Write(O_new_text))
        self.wait(0.5)
        self.play(Uncreate(bis_P_line), Uncreate(bis_Q_line))
        self.wait(0.5)


        """Анимация угла ABC"""
        self.play(Write(solve_1[5]))

        self.play(Create(ABC_angle))
        self.play(Flash(ABC_angle, line_length=1, run_time=1))


        """Строки построение рисунка пропадают"""
        self.play(Write(solve_1[6]))
        self.play(FadeOut(*solve_1, shift=UP, run_time=2))

        """Повление r"""
        self.play(Write(solve_2[0]))
        self.play(Write(solve_2[1]))

        """Трансформация R -> 2r"""
        self.play(Write(solve_2[2]))
        self.wait(0.5)

        # Создаём объекты "2r" в позициях старых "R"
        two_r_1 = Tex("$2r$", font_size=34, color=YELLOW).move_to(R_text_1)
        two_r_2 = Tex("$2r$", font_size=34, color=YELLOW).move_to(R_text_2)

        # Превращаем R в 2r
        self.play(
            ReplacementTransform(R_text_1, two_r_1),
            ReplacementTransform(R_text_2, two_r_2),
            run_time=1.5
        )
        self.wait(0.5)


        """Построение перпендикулятор и углов"""
        self.play(Write(solve_2[3], run_time=5))
        self.play(Create(O1E), Create(O1F), Create(E), Create(F))
        self.play(Write(E_text), Write(F_text))
        self.play(Create(AEO1_angle), Create(O1FP_angle))
        self.play(Write(r_text_1), Write(r_text_2))
        self.play(Create(OB))


        """Появление ответа слева снизу"""
        self.play(Write(solve_2[4], run_time=3))
        self.wait(0.5)


        self.play(
            Grow(answer_text, **ELASTIC),
            run_time=1.5
        )
        self.play(
            Create(answer_rect),
            run_time=1
        )
        self.wait()
