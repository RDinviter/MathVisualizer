class Triga_a(Scene):
    def construct(self):
        eq_text_a = Tex(r'a) Решите уравнение $2\cos\left({x-\frac{\pi}{3}}\right)+$'
                        r'$2\sin\left({\frac{3\pi}{2} + x}\right)=0$', font_size=25, color=GOLD_A).to_corner(UL, buff=0.4)
        eq_text_b = Tex(r"б) Найдите корни уравнения, принадлежащие отрезку $\left[-2\pi ; -\frac{\pi}{2}\right]$",
                        font_size=25, 
                        color=GOLD_A).to_corner(UL)
        eq_text_b.next_to(eq_text_a, DOWN, aligned_edge=LEFT)
        eq_group = VGroup(eq_text_a, eq_text_b)

        self.play(Write(eq_text_a), Write(eq_text_b), run_time=2)
        self.play(eq_group.animate.scale(0.8))
        self.play(eq_group.animate.to_corner(UL, buff=0.2))

        eq_box = SurroundingRectangle(
            eq_group,
            color=GOLD_A,
            buff=0.15,
            stroke_width=2
        )
        self.play(Create(eq_box), run_time=1)
        self.wait(0.5)
        
        # Группируем условие с рамкой для дальнейшего позиционирования
        eq_with_box = VGroup(eq_group, eq_box)

        step_1_text = Tex(
            "a) Применим формулу приведения и формулу косинуса разности:",
            font_size=20,
            color=WHITE
        ).next_to(eq_group, DOWN, aligned_edge=LEFT, buff=0.4)
        
        #Шаг первый
        self.play(FadeIn(step_1_text, shift=UP))
        self.wait()

        step_1_formula = (
            r"\sin\left(\frac{3\pi}{2} + x\right) = -\cos x",
            r"\cos\left(x - \frac{\pi}{3}\right) = \cos x \cdot \cos\frac{\pi}{3} + \sin x \cdot \sin{\frac{\pi}{3}}"
        )
        step_1_formula = MathTex(*step_1_formula, font_size=18)
        step_1_formula.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        step_1_formula.next_to(step_1_text, DOWN, aligned_edge=LEFT)
        step_1_formula.shift(RIGHT)

        self.play(Write(step_1_formula[0]))
        self.play(Write(step_1_formula[1]))

        #Шаг 2
        step_2_t = Tex(
            "Получим:",
            font_size=18
        ).next_to(step_1_formula, DOWN, aligned_edge=LEFT)
        
        step_2_f = (
            r"2\left(\cos{x} \cdot \cos{\frac{\pi}{3}} + \sin{x} \cdot \sin{\frac{\pi}{3}}\right) -2\cos{x} = 0", 
            r"\cos{x} + \sqrt{3}\sin{x}-2\cos{x}=0",
            r"\sqrt{3}\sin{x} - \cos{x} = 0"
        )
        step_2_f = MathTex(*step_2_f, font_size=18)
        step_2_f.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        step_2_f.next_to(step_2_t, DOWN, aligned_edge=LEFT)
        step_2_t.shift(LEFT)
        self.play(Write(step_2_t))
        self.play(Write(step_2_f[0]))
        self.play(Write(step_2_f[1]))
        self.play(TransformFromCopy(step_2_f[1], step_2_f[2]))

        #Шаг 3
        step_3_t = Tex(
            r"Заметим, что если $\cos{x}=0$, то $\sin{x}=0$, ",
            r"что противоречит ОТТ. Значит, можем обе части уравнения ",
            r"поделить на $\cos{x} \neq 0$. \\",
            r"Получаем:",
            font_size=18,
            tex_environment="flushleft"
        )

        step_3_t.next_to(step_2_f, DOWN, aligned_edge=LEFT)
        step_3_t.shift(0.5*LEFT)
        self.play(Write(step_3_t[:3]))
        self.play(GrowFromCenter(step_3_t[-1].shift(0.5*LEFT)))

        step_3_f = (
            r"\sqrt{3}\tg{x} - 1 = 0",
            r"\tg{x} = \frac{1}{\sqrt{3}}",
        )
        step_3_f = MathTex(*step_3_f, font_size=18)
        step_3_f.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        step_3_f.next_to(step_3_t, DOWN, aligned_edge=LEFT)
        step_3_f.shift(RIGHT)
        self.play(Write(step_3_f))

        ans = Tex(r"a) $x=\frac{\pi}{6} + \pi k, k \in \mathbb{Z}.$", 
            font_size=18,
            color=GOLD)
        
        ans.next_to(step_3_f, DOWN, aligned_edge=LEFT)
        self.play(Write(ans))
        
        ans_box = SurroundingRectangle(
            ans,
            color=GOLD_A,
            buff=0.15,
            stroke_width=2
        )
        self.play(Create(ans_box))

        solution_group = VGroup(
            step_1_text, step_1_formula,
            step_2_t, step_2_f,
            step_3_t, step_3_f
        )
        self.play(
            solution_group.animate.shift(UP * 3).fade(1),
            run_time=1.5
        )
        ans_group = VGroup(ans, ans_box)
        self.remove(solution_group)

        self.play(ans_group.animate.next_to(eq_box, DOWN, aligned_edge=LEFT))
        self.wait(2)



