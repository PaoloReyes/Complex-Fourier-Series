from manim import *
import svg.path

#Function variables
time = np.arange(-40, 40, 0.01)
path = '''M 10,30
        A 20,20 0,0,1 50,30
        A 20,20 0,0,1 90,30
        Q 90,60 50,90
        Q 10,60 10,30 z'''
pp = svg.path.parse_path(path)
func = [-pp.point(pos)+50+50j for pos in np.linspace(0, 1, len(time))]
T = 8
w0 = 2*np.pi/T

#Approximation variables
iterations = 400

class Fourier(Scene):
    def calculateFn(self, f, n, t):
        T = t[-1] - t[0]
        multVector = []
        for idx, element in enumerate(f):
            multVector.append(element*np.exp(-1j*n*(2*np.pi/T)*t[idx]))
        area = 0
        for idx, element in enumerate(multVector):
            if idx != len(multVector)-1:    
                area += (t[idx+1]-t[idx])*multVector[idx+1]
        return area/T
    
    def calculateF(self, iterationValue):
        f = np.zeros(len(time))
        for iteration in range(-iterationValue, iterationValue+1):
            Fn = self.calculateFn(func, iteration, time)
            f = f + Fn*np.exp(1j*iteration*w0*time)
        f_real = np.real(f)
        f_imag = np.imag(f)
        return f_real, f_imag

    def construct(self):
        axes = Axes(
            x_range = [-70, 70, 14],
            y_range = [-70, 70, 14],
            x_length = 10,
            axis_config = {"include_numbers": False},
            tips=False,
        )

        iterationValues = [i for i in range(1,iterations)]
        for idx, iterationValue in enumerate(iterationValues):
            f_real, f_imag = self.calculateF(iterationValue)

            graph = axes.plot_line_graph(
                x_values = f_real,
                y_values = f_imag,
                line_color = RED,
                add_vertex_dots = False,
            )
            plot = VGroup(axes, graph)
            iterationLabel = Tex(f'Iteration = {idx}').shift(3*UP+3.5*RIGHT)

            if idx == 0:
                self.add(plot, iterationLabel)
                self.wait(0.3)
            elif idx < 10:
                self.play(ReplacementTransform(previousPlot, plot), run_time=0.1)
                self.play(ReplacementTransform(previousiterationLabel, iterationLabel), run_time=0.1)
            elif idx < 20:
                self.play(ReplacementTransform(previousPlot, plot), run_time=0.025)
                self.play(ReplacementTransform(previousiterationLabel, iterationLabel), run_time=0.025)
            elif idx < 50:
                self.play(ReplacementTransform(previousPlot, plot), run_time=0.01)
                self.play(ReplacementTransform(previousiterationLabel, iterationLabel), run_time=0.01)
            else:
                self.play(ReplacementTransform(previousPlot, plot), run_time=0.001)
                self.play(ReplacementTransform(previousiterationLabel, iterationLabel), run_time=0.001)

            previousPlot = plot
            previousiterationLabel = iterationLabel