import sys
from prompt_toolkit.document import Document


def printText(text, output=None, end='\n'):
    if output is None:
        frame = sys._getframe().f_back
        if ('self' in frame.f_locals and
                'output_field' in frame.f_locals['self'].__dict__):
            # self object exists and output_field in self object.
            output = frame.f_locals['self'].__dict__['output_field']
        else:
            output = print
#            frame = frame.f_back
#            if ('self' in frame.f_locals and
#                'output_field' in frame.f_locals['self'].__dict__):
#                output = frame.f_locals['self'].__dict__['output_field']
#            else:
#                output = print
    if output is print or output is None:
        print(text, end=end)
    else:
        if type(output) != list:
            output = [output]
        for each in output:
            new_text = each.text + str(text) + end
            each.buffer.document = Document(
                text=new_text, cursor_position=len(new_text)
            )
