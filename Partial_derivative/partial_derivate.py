%%manim -qh Partial_Derivative

class Partial_Derivative(ThreeDScene):
    def construct(self): 
    # get the 2-D function
        self.set_camera_orientation(phi=60*DEGREES, theta=30*DEGREES, distance=2)
        self.plot_func()
        self.wait(2)
        self.slice_through(direction="x", pos=[0,2,0])
        self.wait(2)
        self.highlight_slice()
        self.wait()
        self.move_camera(theta=-90*DEGREES, run_time=2)
        self.wait(1)
        self.move_camera(phi=90*DEGREES)
        self.wait(2)
    # set up the 2D Screen for the 2D function
        new_x_axis = Arrow3D(start=[-5,0,0], end=[5,0,0])
        self.play(
            self.func_3d.animate.set_opacity(0.1), 
            FadeOut(self.ax.x_axis),
            FadeIn(new_x_axis)
            )

        self.wait(2)
        self.take_derivative()
        self.wait(5)
        
    def plot_func(self):
        ax = ThreeDAxes()
        self.ax = ax
        ax_labels = ax.get_axis_labels(Text("x"), Text("y"), Text("z"))
        self.ax_labels_3d = ax_labels

        def param_surface(u, v):
           return np.sin(u) + np.cos(v)
        func_3d = Surface(
            lambda u, v: ax.c2p(u, v, param_surface(u, v)),
            resolution=8,
            v_range=[-5, 5],
            u_range=[-5, 5],
            checkerboard_colors=False,
            fill_color = PURE_BLUE,
            fill_opacity = 0.5,
            )
        self.func_3d = func_3d
        self.func_3d_label = MathTex(r"z(x,y) = sin(x) + cos(y)").move_to([4,3,0])
        self.play(Create(ax), Write(ax_labels))
        self.play(DrawBorderThenFill(func_3d), run_time=2)
        self.camera.add_fixed_in_frame_mobjects(self.func_3d_label)
        self.play(FadeIn(self.func_3d_label))


    def slice_through(self, direction="x", pos=[0,0,0]):
        self.slice_pos=pos
        ax = self.ax
     # by default the plane into which the slice is rotated is the x-z-plane
        rot_ax = np.array([1,0,0])
        # rotate into y-z-plane
        if direction == "y": 
            rot_ax = np.array([0,1,0])
        # rotate into x-y-plance -> by default the slice will be in this plane so no need to do anything
        elif direction == "z":
            rot_ax = np.array([0,0,0])
            
        piece = ScreenRectangle().rotate(PI/2, axis=rot_ax)
        self.slice = piece
        piece.move_to(pos)
        self.play(Write(piece))
    
    def highlight_slice(self):
        ax = self.ax
        x = self.slice_pos[0]
        y = self.slice_pos[1]
        func = ParametricFunction(
            lambda t: ( 
                t,
                2,
                np.sin(t) + np.cos(y)
            ), color=RED, t_range=[-3.55,3.55,0.01]

        )
        self.slice_func = func
        new_func_3d_label = MathTex(r"z(x,2) = sin(x) + cos(2)").move_to([4,3,0])
        self.camera.add_fixed_in_frame_mobjects(new_func_3d_label)
        self.play(AnimationGroup(
            Write(func), 
            ReplacementTransform(self.func_3d_label, new_func_3d_label)            
            ), run_time=2
        )
        self.func_3d_label =  new_func_3d_label 
        newest_func_3d_label = MathTex(r"{z}_{y=2}(x) = sin(x) - 0.4161").move_to([4,3,0])
        self.camera.add_fixed_in_frame_mobjects(newest_func_3d_label)
        self.play(ReplacementTransform(self.func_3d_label, newest_func_3d_label))
        self.wait(1)
        self.func_3d_label =  newest_func_3d_label 

    
    def take_derivative(self):
        func = self.slice_func
        alpha = ValueTracker(0.2)
        point = always_redraw(
            lambda: Dot3D(
                func.point_from_proportion(alpha.get_value()),
                color=WHITE
            )           
        )
        tangent = always_redraw(
            lambda: TangentLine(
                func,
                alpha = alpha.get_value(),
                color=GREEN,
                length=4
            )
        )
        self.add(point, tangent)
        self.play(AnimationGroup(Create(point), Create(tangent)))
        self.wait()
        self.play(alpha.animate.set_value(0.8), run_time=4)
        
        


        