from manim import *


class SlidingTangent(Scene):
    def construct(self):
        # 1. Настраиваем систему координат
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True, "font_size": 24}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # 2. Определяем функцию f(x) и её производную f'(x)
        def f(x):
            return x ** 2

        def df(x):
            return 2 * x

        graph = axes.plot(f, color=BLUE, x_range=[-3, 3])
        graph_label = MathTex("f(x) = x^2", color=BLUE).next_to(graph, UR, buff=0.2)

        # 3. ValueTracker будет плавно менять значение x
        x_tracker = ValueTracker(-2)

        # 4. Функция для построения касательной в текущей точке x
        def get_tangent():
            x = x_tracker.get_value()
            y = f(x)
            slope = df(x)  # Наклон касательной

            # Берем две точки на касательной (чуть левее и правее) и строим прямую
            dx = 0.7
            p1 = axes.c2p(x - dx, y - slope * dx)
            p2 = axes.c2p(x + dx, y + slope * dx)
            return Line(p1, p2, color=YELLOW, stroke_width=3)

        # 5. Точка касания
        dot = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), f(x_tracker.get_value())),
            color=RED,
            radius=0.08
        ))

        # 6. Сама касательная линия
        tangent = always_redraw(get_tangent)

        # 7. Текст с текущим значением производной
        def get_deriv_text():
            x = x_tracker.get_value()
            slope = df(x)
            return MathTex(
                f"f'({x:.1f}) = {slope:.1f}",
                font_size=36,
                color=YELLOW
            ).to_corner(UR, buff=0.5)

        deriv_text = always_redraw(get_deriv_text)

        # 8. Треугольник касательной
        def get_slope_triangle():
            x = x_tracker.get_value()
            y = f(x)
            slope = df(x)

            dx = 0.5
            dy = slope * dx

            p1 = axes.c2p(x, y)
            p2 = axes.c2p(x + dx, y)
            p3 = axes.c2p(x + dx, y + dy)

            return Polygon(p1, p2, p3, color=GREEN, fill_opacity=0.2)

        triangle = always_redraw(get_slope_triangle)

        # 9. Анимация появления объектов
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), Write(graph_label))
        self.wait(0.5)

        self.play(
            FadeIn(dot),
            Create(tangent),
            Create(triangle),
            Write(deriv_text)
        )
        self.wait(0.5)

        # 10. Главная анимация: двигаем x от -2 до 2 и обратно
        self.play(
            x_tracker.animate.set_value(2),
            run_time=15,
            rate_func=there_and_back
        )

        self.wait(1)
