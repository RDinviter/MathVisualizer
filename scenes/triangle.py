from manim import *
import numpy as np

# Вспомогательная функция: проекция точки P на прямую, заданную точками A и B
def project_point_onto_line(P, A, B):
    v = B - A                  
    w = P - A                  
    t = np.dot(w, v) / np.dot(v, v)  
    return A + t * v          

class Triangle(Scene):
    def construct(self):
        A = Dot(3*LEFT + 1.5*DOWN)
        B = Dot(1.5*DR + RIGHT)
        C = Dot(1.2*UP + 1.2*UR)
        

        A_text = Tex("A", color=YELLOW, font_size=34).next_to(A, DL, buff=0.1)
        B_text = Tex("B", color=YELLOW, font_size=34).next_to(B, DR, buff=0.1)
        C_text = Tex("C", color=YELLOW, font_size=34).next_to(C, UR, buff=0.1)

        A_coord = A.get_center()
        B_coord = B.get_center()
        C_coord = C.get_center()

        a = np.linalg.norm(B_coord - C_coord)
        b = np.linalg.norm(C_coord - A_coord)
        c = np.linalg.norm(A_coord - B_coord)

        I_coord = (a * A_coord + b * B_coord + c * C_coord) / (a + b + c)
        incenter = Dot(I_coord, color=RED, radius=0.05)

        O_text = Tex("O", color=YELLOW, font_size=34).next_to(incenter, UL, buff=0.1)

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

        P_text = Tex("P", color=YELLOW, font_size=34).next_to(P, DOWN, buff=0.1)
        Q_text = Tex("Q", color=YELLOW, font_size=34).next_to(Q, UR, buff=0.1)

        # Радиусы от центра к точкам касания
        radius_AB = Line(I_coord, T_AB, color=YELLOW)
        radius_BC = Line(I_coord, T_BC, color=YELLOW)

        # === Анимация ===
        self.play(
            Create(AB), Create(BC), Create(CA),
            FadeIn(A), FadeIn(B), FadeIn(C),
            Write(A_text), Write(B_text), Write(C_text),
            run_time=2
        )
        self.wait(0.5)

        self.play(Create(incircle), FadeIn(incenter), Write(O_text), run_time=2)
        self.wait(0.5)

        # Последовательное появление радиусов
        self.play(
            Create(radius_AB), FadeIn(P),
            Create(radius_BC), FadeIn(Q),
            Write(P_text), Write(Q_text),
            run_time=2
        )
        self.wait()

        #Координаты вершин четырехугольника
        O_coord = I_coord.get_center()  
        P_coord = T_AB.get_center()       
        B_coord_new = B_coord.get_center()    
        Q_coord = T_BC.get_center()       

        # Стороны OPBQ
        OP = np.linalg.norm(P_coord - O_coord)  # = r
        PB = np.linalg.norm(B_coord_new - P_coord)
        BQ = np.linalg.norm(Q_coord - B_coord_new)
        QO = np.linalg.norm(O_coord - Q_coord)  # = r

        
