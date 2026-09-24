class Triga_b(Scene):
    def construct(self):
        self.camera.background_color = "#121440"

        eq_text_a = Tex(r'a) Решите уравнение $2\cos\left({x-\frac{\pi}{3}}\right)+$'
                        r'$2\sin\left({\frac{3\pi}{2} + x}\right)=0$', font_size=25, color=GOLD_A).to_corner(UL, buff=0.4)
        eq_text_b = Tex(r"б) Найдите корни уравнения, принадлежащие отрезку $\left[-2\pi ; -\frac{\pi}{2}\right]$",
                        font_size=25, 
                        color=GOLD_A).to_corner(UL)
        eq_text_b.next_to(eq_text_a, DOWN, aligned_edge=LEFT)
        eq_group = VGroup(eq_text_a, eq_text_b)
        eq_group.scale(0.8).to_corner(UL, buff=0.2)
        self.add(eq_text_a, eq_text_b)

        eq_box = SurroundingRectangle(
            eq_group,
            color=GOLD_A,
            buff=0.15,
            stroke_width=2
        )
        self.add(eq_box)
        eq_with_box = VGroup(eq_group, eq_box)

        ans = Tex(r"a) $x=\frac{\pi}{6} + \pi k, k \in \mathbb{Z}.$", 
            font_size=24,
            color=GOLD)
        self.add(ans)
        ans_box = SurroundingRectangle(
            ans,
            color=GOLD_A,
            buff=0.15,
            stroke_width=2
        )
        self.add(ans_box)

        ans_group = VGroup(ans, ans_box).next_to(eq_box, DOWN, aligned_edge=LEFT)

        step_1_t = Tex(
            r"б) Отберем корни на отрезке $\left[-2\pi ; -\frac{\pi}{2}\right]$:", 
            font_size=18)
        step_1_t.next_to(ans_group, DOWN, aligned_edge=LEFT)
        self.play(GrowFromCenter(step_1_t))

        circ = Circle(1.5)
        x_axis = Arrow(2* LEFT, 2 * RIGHT, tip_length=0.12)
        y_axis = x_axis.copy().rotate(PI / 2)
        trig_circ = VGroup(circ, x_axis, y_axis).set_stroke(WHITE, 2)
        self.play(Create(trig_circ, run_time=3), lag_ratio=0.1)

        zero = Tex("0").scale(0.65).shift(0.25 * DL)
        pi = MathTex(r"-\pi").shift(1.5 * LEFT + 0.25 * UL).scale(0.65)
        poltora_pi = MathTex(r"-\frac{3\pi}{2}").shift(1.7*UP+0.55*RIGHT).scale(0.45)
        half_pi = MathTex(r"-\frac{\pi}{2}").shift(1.7*DOWN+0.35*RIGHT).scale(0.45)
        two_pi = MathTex(r"-2\pi").shift(1.5 * RIGHT + 0.35 * UR).scale(0.65)
        self.play(GrowFromCenter(zero))
        self.play(GrowFromCenter(two_pi))
        self.play(GrowFromCenter(poltora_pi))
        self.play(GrowFromCenter(pi))
        self.play(GrowFromCenter(half_pi)) 

        arc = Arc(1.5, start_angle=0, angle=1.5*PI, color=YELLOW)
        dot_1 = Dot(1.5 * RIGHT, 0.1, color=YELLOW).set_stroke(BLACK, 1.5)
        dot_1.rotate(PI / 6, about_point=ORIGIN)
        self.play(Create(arc), run_time=2)
        
        root_1 = MathTex(r"-\dfrac{11\pi}{6}").scale(0.65)
        root_1.next_to(dot_1, UR, buff=0.1)
        self.play(FadeIn(root_1, scale=0), FadeIn(dot_1, scale=0))

        

        dot_2 = Dot(1.5 * RIGHT, 0.1, color=YELLOW).set_stroke(BLACK, 1.5)
        dot_2.rotate(7 * PI / 6, about_point=ORIGIN)

        dased_line = DashedLine(
            dot_1, dot_2,
            dashed_ratio=0.5,
            dash_length=0.1)

        root_2 = MathTex(r"-\dfrac{5\pi}{6}").scale(0.65)
        root_2.next_to(dot_2, DL, buff=0.1)
        self.play(Create(dased_line))
        self.play(FadeIn(root_2, scale=0), FadeIn(dot_2, scale=0))

        step_2_t = Tex(
            r"Получим числа:", 
            font_size=18
        ).next_to(step_1_t, DOWN, aligned_edge=LEFT)
        self.play(Write(step_2_t))

        step_2_f = (
            r"$x$ $= -2\pi + \dfrac{\pi}{6} =$ $-\dfrac{11\pi}{6}$",
            r"$x$ $= -\pi + \dfrac{\pi}{6} =$ $-\dfrac{5\pi}{6}$"
        )
        step_2_f = Tex(*step_2_f,
         font_size=18,
         tex_to_color_map={
                "$x$": YELLOW,
                "$-\dfrac{11\pi}{6}$": YELLOW,
                "$-\dfrac{5\pi}{6}$": YELLOW                
                })

        step_2_f.arrange(DOWN, aligned_edge=LEFT,buff=0.3)
        step_2_f.next_to(step_2_t, DOWN, aligned_edge=LEFT)

        self.play(Write(step_2_f[0]))
        self.play(Write(step_2_f[1]))

        ans_1 = Tex("б) $x=-\dfrac{11\pi}{6}$", font_size=18, color=YELLOW)
        ans_1.move_to(step_2_f[0])

        ans_2 = Tex("$x=-\dfrac{5\pi}{6}$", font_size=18, color=YELLOW)
        ans_2.move_to(step_2_f[1])

        ans_group_1 = VGroup(ans_1, ans_2)
        ans_box_1 = SurroundingRectangle(
            ans_group_1,
            color=GOLD_A,
            buff=0.15,
            stroke_width=2
        )
        

        self.play(TransformFromCopy(step_2_f[0], ans_1), TransformFromCopy(step_2_f[1], ans_2), FadeOut(step_2_f))
        self.play(Create(ans_box_1))
        self.wait()
