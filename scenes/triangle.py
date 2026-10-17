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
        return None # Прямые параллельны
        
    t, s = np.linalg.solve(A_mat, b_vec)
    # Возвращаем точку с z=0
    return np.array([p1[0] + t * v1[0], p1[1] + t * v1[1], 0])

PROBLEM = '''Окружность с центром O, вписанная в треугольник ABC, касается сторон AB и BC в точках P и Q соответственно. В четырёхугольник BPOQ можно вписать окружность. Найдите угол ABC, если известно, что радиус этой окружности вдвое меньше радиуса вписанной окружности треугольника ABC. Ответ дайте в градусах.'''

class Triangle(Scene):
    def construct(self):

        problem_group = setup_problem(
            self, 
            PROBLEM,
            font_size=24
        )
        A = Dot(3*LEFT + 1.5*DOWN)
        B = Dot(1.5*DR + RIGHT)
        C = Dot(1.2*UP + 1.2*UR)
        

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
            Line(Q.get_center(),I_coord),  
            Line(Q.get_center(), C_coord),          
            color=YELLOW,
            length=0.2
            
        )


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
            Create(OP), FadeIn(P),
            Create(OQ), FadeIn(Q),
            Write(P_text), Write(Q_text),
            Create(APO_angle), Create(OQC_angle),
            run_time=2
        )
        self.wait()

        #Координаты вершин четырехугольника
        O_coord = I_coord 
        P_coord = T_AB     
        B_coord = B_coord 
        Q_coord = T_BC

        #Найдем направление бисс. угла Р
        dir_PO = get_unit_vector(O_coord - P_coord)
        dir_PB = get_unit_vector(B_coord - P_coord)
        bis_P_dir = get_unit_vector(dir_PO + dir_PB)

        #Найдем направление бисс. угла Q
        dir_QO = get_unit_vector(O_coord - Q_coord)
        dir_QB = get_unit_vector(B_coord - Q_coord)
        bis_Q_dir = get_unit_vector(dir_QO + dir_QB)

        #Найдем инцентр OPBQ
        O1 = line_intersection(
            P_coord, bis_P_dir, 
            Q_coord, bis_Q_dir)
        O1 = np.array([O1[0], O1[1], 0])

        T_new = project_point_onto_line(O1, P_coord, B_coord)
        r_new = np.linalg.norm(O1 - T_new)

        bis_P_line = Line(P_coord, P_coord + 2.5 * bis_P_dir, color=WHITE)
        bis_Q_line = Line(Q_coord, Q_coord + 2.5 * bis_Q_dir, color=WHITE)

        incenter_new = Dot(O1, color=RED, radius=0.05)
        O_new_text = Tex(r"$O_1$", color=YELLOW, font_size=34).next_to(incenter_new, DOWN, buff=0.1)

        incircle_new = Circle(radius=r_new, color=BLUE, stroke_width=3).move_to(O1)

        self.play(
            Create(bis_P_line),
            Create(bis_Q_line), 
            run_time=1.5
        )
        self.wait()
        self.play(
            FadeIn(incenter_new), 
            Write(O_new_text), 
            run_time=1
        )
        self.wait(0.5)

        self.play(
            Uncreate(bis_P_line),
            Uncreate(bis_Q_line), 
        )

        self.play(
            Create(incircle_new)
        )



        E = project_point_onto_line(O1, A_coord, B_coord)
        E = Dot(E, color=GREEN, radius=0.04)

        F = project_point_onto_line(O1, I_coord, P_coord)
        F = Dot(F, color=GREEN, radius=0.04)

        F_text = Tex("$F$", color=YELLOW, font_size=34).next_to(F, UR, buff=0.1)
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

        self.play(
            Create(E), Create(F),
            Create(O1E),
            Create(O1F),
            Write(F_text), 
            Write(E_text)
        )

        self.play(
            Create(O1FP_angle),
            Create(AEO1_angle)
        )


        R_text_1 = Tex("$R$", font_size=34, color=WHITE)
        R_text_1.next_to(OP.get_center(), LEFT, buff=0.1)
        R_text_1.set_opacity(0)

        R_text_2 = Tex("$R$", font_size=34, color=WHITE)
        R_text_2.next_to(OQ.get_center(), UP, buff=0.1)
        R_text_2.set_opacity(0)

        OB = Line(I_coord, B, color=WHITE)
        self.play(Create(OB))

        

        triangle_group = VGroup(
                AB, BC, CA,                  
                A, B, C,                     
                A_text, B_text, C_text,
                incircle,              
                incenter, O_text,      
                P, Q,                  
                P_text, Q_text,        
                OP, OQ,  
                APO_angle, OQC_angle, 
                incenter_new, O_new_text, 
                incircle_new, 
                E, F, O1F, O1E, 
                R_text_1, R_text_2,
                E_text, F_text, 
                AEO1_angle, O1FP_angle, 
                OB         
            )
        self.play(triangle_group.animate.shift(3*RIGHT))
        self.remove(R_text_1, R_text_2)
        
        R_text_1.set_opacity(1)
        R_text_2.set_opacity(1)

        self.play(Write(R_text_1), Write(R_text_2))
        self.wait()
