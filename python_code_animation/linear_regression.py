import pandas as pd
from math import sqrt
from manim import *

def create_model() -> tuple:
    data = list(pd.read_csv("data/single_independent_variable_linear_small.csv").itertuples())
    m = ValueTracker(1.93939)
    b = ValueTracker(4.73333)

    ax = Axes(
        x_range=[0, 10],
        y_range=[0, 25, 5],
        axis_config={"include_tip": False},
    )
    # plot points 
    points = [Dot(point=ax.c2p(p.x, p.y), radius=.15, color=BLUE) for p in data]

    # plot function
    line = Line(start=ax.c2p(0, b.get_value()), end=ax.c2p(10, m.get_value()*10+b.get_value())).set_color(YELLOW)

    # make line follow m and b value 
    line.add_updater(
        lambda l: l.become(Line(start=ax.c2p(0, b.get_value()), end=ax.c2p(10, m.get_value()*10+b.get_value()))).set_color(YELLOW)
    )
        
    return data,m,b,ax,points,line

class FirstScene(Scene):

    def construct(self):

        data,m,b,ax,points,line = create_model()

        # add elements to VGroup
        graph = VGroup(ax, *points)

        # three versions of linear function 
        eq1 = MathTex("f(x) = ", r"m ", r"x + ","b").move_to((RIGHT+DOWN))
        eq1[1].set_color(RED)
        eq1[3].set_color(RED)

        eq2 = MathTex(r"f(x) = ", r"\beta_1", r"x + ", r"\beta_0").move_to((RIGHT+DOWN))
        eq2[1].set_color(RED)
        eq2[3].set_color(RED)

        eq3 = MathTex("f(x) = ", f'{m.get_value()}', r"x + ",f'{b.get_value()}').move_to((RIGHT+DOWN))
        eq3[1].set_color(RED)
        eq3[3].set_color(RED)

      
        # populate charting area
        self.play(
            DrawBorderThenFill(graph),
            run_time=2.0
        )

        # draw line 
        self.play(
            Create(line),
            run_time=2.0
            )
        
        # transform the math equation to three variants
        # equation 1 create
        self.play(
            Create(eq1)
        )

        self.wait()


        # animate the coefficients m and b
        def blink(item, value, increment):
          self.play(ScaleInPlace(item, 4/3), value.animate.increment_value(increment))

          for i in range(0,1):
            self.play(ScaleInPlace(item, 3/4), value.animate.increment_value(-2*increment))
            self.play(ScaleInPlace(item, 4/3), value.animate.increment_value(2*increment))

          self.play(ScaleInPlace(item, 3/4), value.animate.increment_value(-increment))
          self.wait()

        blink(eq1[1], m, .50)
        blink(eq1[3], b, 2.0)

        self.wait()

        # transform to beta coefficients
        self.play(ReplacementTransform(eq1,eq2))

        self.wait()

        # transform with coefficent values
        self.play(
            ReplacementTransform(
                eq2, 
                eq3
            )
        )

        self.wait()

        # remove equation 
        self.play(
              FadeOut(eq3, shift=DOWN),
        )

def create_residual_model(scene,data,m,b,ax,points,line) -> tuple: 
  residuals: list[Line] = []
  for d in data: 
    residual = Line(start=ax.c2p(d.x, d.y), end=ax.c2p(d.x, m.get_value() * d.x + b.get_value())).set_color(RED)
    scene.play(Create(residual), run_time=.3)
    residual.add_updater(lambda r,d=d: r.become(Line(start=ax.c2p(d.x, d.y), end=ax.c2p(d.x, m.get_value()*d.x+b.get_value())).set_color(RED)))
    residuals += residual

  # flex residuals changing the coefficients m and b
  def flex_residuals(): 
    m_delta=1.1
    scene.play(m.animate.increment_value(m_delta))
    for i in (-1,1,-1,1):
        scene.play(m.animate.increment_value(i*m_delta))
        scene.play(m.animate.increment_value(i*m_delta))
    scene.play(m.animate.increment_value(-m_delta))

    scene.wait()

  return residuals, flex_residuals


class ThirdScene(Scene):

    def construct(self):
        # add base graph 
        data,m,b,ax,points,line = create_model()
        self.add(ax,line,*points)

        residuals, flex_residuals = create_residual_model(self,data,m,b,ax,points,line)

        squares: list[Square] = []
        for i,d in enumerate(data):

          square = Square(color=RED,
                          fill_opacity=.6, 
                          side_length=residuals[i].get_length()
                          ).next_to(residuals[i], LEFT, 0)

          square.add_updater(lambda s=square,r=residuals[i]: s.become(
              Square(color=RED,
                     fill_opacity=.6, 
                     side_length=r.get_length()
                     ).next_to(r, LEFT, 0)
          ))

          squares+=square
          self.play(Create(square), run_time=.1)

        flex_residuals()
        length = 0.0

        for s in squares:
          length = sqrt(length**2 + s.side_length**2)
          total_square= Square(color=RED,fill_opacity=1,side_length=length).move_to(3 * LEFT + 2.5*UP)
          self.play(
              ReplacementTransform(s,total_square),
              run_time=.3
          )
        
        
        self.play(DrawBorderThenFill(Text("SSE").scale(.8).move_to(total_square)))
        self.wait()