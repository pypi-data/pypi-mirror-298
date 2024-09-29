""" Module to Reports in PDF Format """
import dataclasses
import os

import pkg_resources
import pandas as pd
import pandas.api.types as pdtypes
import fpdf

from o7pdf.pandas_basic import Rectangle, PandasBasic



@dataclasses.dataclass
class ChartParam: # pylint: disable=too-many-instance-attributes
    """Parameters the chart"""
    spacing : float = 0.5 # Spacing between the elements in percentage (0 to 1)
    x_label_step = 1 # Steps for the X label



@dataclasses.dataclass
class SerieParam: # pylint: disable=too-many-instance-attributes
    """Parameters for a column"""
    name : str = '' # TBD
    data : str = 'no-data' # data column

    color : dict = None  # Color of the background
    width : float = None
    type : str = False  # Only bar for now
    is_stacked : bool = False
    stack_id : int = None

    y_axis : str = 'left'


@dataclasses.dataclass
class Axis: # pylint: disable=too-many-instance-attributes
    """ Values for the Axis, used for internal calculations"""
    title : str = ''    # TBD
    width : float = 5
    height : float = None
    min : float = None
    max : float = None
    step : float = None
    format : str = '{:,.0f}'
    color : dict = None
    grid : bool = False # TBD, alway on for now
    position : str = 'left'
    visible : bool = True # TBD, alway visible for now


    @property
    def value_to_height(self) -> float:
        """Calculate value to height ratio"""
        return self.height / (self.max - self.min)

res_dir = pkg_resources.resource_filename(__name__, 'res')



#*************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
#*************************************************
class PandasChart(PandasBasic): # pylint: disable=too-many-instance-attributes
    """Class to generate a chart from Pandas Dataframe in a PDF Report"""


    def __init__(self,
        series : list[SerieParam],
        width : float,
        height : float,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.param : ChartParam = ChartParam()
        self.series : list[SerieParam] = series
        self.width : float = width
        self.height : float = height

        self._chart_rect : Rectangle = Rectangle()
        self._data_rect : Rectangle = Rectangle()


        self._x_count : int = None
        self._x_width : float = None  # Width of each X elements
        self._x_spacing : float = None  # distance between each X element
        self._x_axis_height : float = 5
        self._stack_count : int = None # number of stacks in each X element
        self._stack_leftover : dict[pd.Series] = None # leftover space in each stack

        self.axis = {
            'left' : Axis(),
            'right' : Axis()
        }

    # *************************************************
    #
    # *************************************************
    def prepare(self) :
        """Prepare variables before the CHART generation"""

        # Determine the number of X elements & variables


        # Set the chart rectangle (Maximum area)
        self._chart_rect.x = self.original_x
        self._chart_rect.y = self.original_y
        self._chart_rect.w = self.width
        self._chart_rect.h = self.height

        # Set the data rectangle (Area for the data)
        self._data_rect.x = self.original_x + self.axis['left'].width
        self._data_rect.y = self.original_y
        self._data_rect.w = self.width - self.axis['left'].width
        self._data_rect.h = self.height - self._x_axis_height

        self._x_count = len(self.df.index)
        self._x_width = self._data_rect.w / self._x_count
        self._x_spacing = self._x_width * self.param.spacing
        self._stack_count = max(len([serie for serie in self.series if not serie.is_stacked]), 1)


        #---------------------------
        # Prepare the Axis values
        #---------------------------
        for axis in self.axis.values():

            if axis.color is None:
                axis.color = self.LINE_COLOR

            axis.height = self._data_rect.h

            if axis.max is None:
                axis.max = max(self.df[serie.data].max() for serie in self.series if serie.y_axis == axis.position)
            if axis.min is None:
                axis.min = min(self.df[serie.data].min() for serie in self.series if serie.y_axis == axis.position)
            if axis.step is None:
                axis.step = (axis.max - axis.min) / 5 if axis.step is None else axis.step

        #---------------------------
        # Prepare Series values
        #---------------------------
        current_stack_id = 0
        self._stack_leftover = {}
        for serie in self.series:
            if serie.color is None:
                serie.color = self.LINE_COLOR

            # TBD if serie.width is None:
            #     serie.width = 0.2

            if serie.type is None:
                serie.type = 'bar'

            if serie.width is None:
                serie.width = (self._x_width - self._x_spacing)  / self._stack_count

            serie.stack_id = current_stack_id
            current_stack_id = current_stack_id + 1 if not serie.is_stacked else current_stack_id
            #print(serie)

        #---------------------------
        # Calculate the leftover space in each stack
        #---------------------------
        for index in range(self._stack_count):
            list_of_data = [serie.data for serie in self.series if serie.stack_id == index]
            self._stack_leftover[index] = self.df[list_of_data].sum(axis=1)

        #print(self._stack_leftover)


        return self



    # *************************************************
    #
    # *************************************************
    def generate(self) :
        """Generate the table inside the PDF Report"""

        self.prepare()

        self.draw_current_highlight()

        self.draw_x_label()
        self.draw_axis(self.axis['left'])
        self.draw_data()
        self.draw_title()

        # self.draw_borders([self._chart_rect], self.LINE_COLOR)




        return self


    # *************************************************
    #
    # *************************************************
    def draw_title(self):
        """Draw the chart title"""

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size = self.font_size)
            self.pdf.set_text_color(**self.LINE_COLOR)
            self.pdf.set_xy(self._data_rect.x, self._data_rect.y)
            self.pdf.cell(
                w = self._data_rect.w, h = self.font_size  / 2,
                text = f'{self.title}', fill=False,
                new_x ="LEFT", new_y="NEXT", align = 'C', border = 0, markdown = True)




    # *************************************************
    #
    # *************************************************
    def draw_data(self):
        """Draw the data in the chart"""

        for index, serie in enumerate(self.series):
            self.draw_serie(index, serie)


    # *************************************************
    #
    # *************************************************
    def draw_serie(self, serie_index : int, serie : SerieParam):
        """ Draw a serie in the chart"""

        axis = self.axis[serie.y_axis]
        self._stack_leftover[serie.stack_id] = self._stack_leftover[serie.stack_id] - self.df[serie.data]
        with self.pdf.local_context():
            self.pdf.set_draw_color(**serie.color)
            self.pdf.set_fill_color(**serie.color)

            for count, (value_index, row) in enumerate(self.df.iterrows()):
                value = row[serie.data]
                height = value * axis.value_to_height

                left_over = self._stack_leftover[serie.stack_id][value_index]
                offset = left_over * axis.value_to_height

                x_pos = self._data_rect.x + (count * self._x_width) + (serie.stack_id * serie.width) + (self._x_spacing / 2)
                y_pos = self._data_rect.y + self._data_rect.h - height - offset

                #print(f'{value_index=} - {value=} - {height=} - {x_pos=} - stack_id={serie.stack_id}')
                self.pdf.rect(x_pos, y_pos, serie.width, height, style='F')


    # *************************************************
    #
    # *************************************************
    def draw_x_label(self):
        """Draw label for the x axis"""

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size = self.font_size)
            self.pdf.set_text_color(**self.LINE_COLOR)

            for index, (title, row) in enumerate(self.df.iterrows()):

                x_pos = self._data_rect.x + (index * self._x_width)
                y_pos = self._data_rect.y + self._data_rect.h

                if index % self.param.x_label_step == 0:

                    self.pdf.set_xy(x_pos, y_pos)
                    self.pdf.cell(
                        w = self._x_width, h = self._x_axis_height,
                        text = f'{title}', fill=False,
                        new_x ="LEFT", new_y="NEXT", align = 'C', border = 0, markdown=True)

                    x_pos_center = x_pos + (self._x_width / 2)

                    self.pdf.line(x_pos_center, y_pos, x_pos_center, y_pos + 0.75)



            self.pdf.line(self._data_rect.x, self._data_rect.y2, self._data_rect.x2, self._data_rect.y2)


    # *************************************************
    #
    # *************************************************
    def draw_axis(self, axis : Axis):
        """Draw label for the a Y axis"""

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size = self.font_size)
            self.pdf.set_text_color(**axis.color)
            self.pdf.set_draw_color(**self.LINE_COLOR_BG)

            for value in range(int(axis.min), int(axis.max), int(axis.step)):

                height = (value - axis.min) * axis.value_to_height
                y_pos = self._data_rect.y + self._data_rect.h - height

                self.pdf.set_xy(self._chart_rect.x, y_pos - (self.font_size  / 2))
                self.pdf.cell(
                    w = self.axis['left'].width, h = self.font_size,
                    text = f'{axis.format.format(value)}', fill=False,
                    new_x ="LEFT", new_y="NEXT", align = 'C', border = 0, markdown=True)


                self.pdf.line(self._data_rect.x, y_pos, self._data_rect.x2, y_pos)


            self.pdf.set_draw_color(**axis.color)
            self.pdf.line(self._data_rect.x, self._data_rect.y, self._data_rect.x, self._data_rect.y2)


    # *************************************************
    #
    # *************************************************
    def draw_current_highlight(self):
        """Draw box to show the current value"""

        if self.current is None:
            return

        with self.pdf.local_context():
            self.pdf.set_draw_color(**self.PROGRESS)
            self.pdf.set_fill_color(**self.PROGRESS)

            count = len(self.df.index) - 1
            x_pos = self._data_rect.x + (count * self._x_width)
            width = self._x_width
            y_pos = self._chart_rect.y
            height = self._chart_rect.h

            self.pdf.rect(x_pos, y_pos, width, height, style='F')
