from manim import *
from xml.dom import minidom
import svg.path

#Function variables
time = np.arange(-40, 40, 0.01)
svg_file = open("fourier.svg")
doc = minidom.parse(svg_file)
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()
path = path_strings[0]
pp = svg.path.parse_path(path)
func = [-pp.point(pos) for pos in np.linspace(0, 1, len(time))]
center_real = (max(np.real(func))+min(np.real(func)))/2
center_imag = (max(np.imag(func))+min(np.imag(func)))/2
func = [-pp.point(pos)-center_real-1j*center_imag for pos in np.linspace(0, 1, len(time))]
T = 8
w0 = 2*np.pi/T
COLOR = "#00FF00"

#Approximation variables
iterations = 10

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
            x_range = [min(np.real(func))*1.5, max(np.real(func))*1.5, (max(np.real(func))-min(np.real(func)))/8],
            y_range = [min(np.imag(func)), max(np.imag(func)), (max(np.imag(func))-min(np.imag(func)))/8],
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
                line_color = COLOR,
                add_vertex_dots = False,
            )
            plot = VGroup(axes, graph)
            iterationLabel = Tex(f'Iteration = {idx}').shift(3*UP+3.5*RIGHT)

            if idx < 10:
                run_time = 0.1
            elif idx < 20:
                run_time = 0.025
            elif idx < 50:
                run_time = 0.01
            else:
                run_time = 0.001
            if idx != 0:
                self.play(ReplacementTransform(previousPlot, plot), run_time=run_time)
                self.play(ReplacementTransform(previousiterationLabel, iterationLabel), run_time=run_time)
            else:
                self.add(plot, iterationLabel)
                self.wait(0.3)
                
            previousPlot = plot
            previousiterationLabel = iterationLabel