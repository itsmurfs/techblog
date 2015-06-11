#This is the python module for processing html which uses beautifulsoup
from HTMLParser import HTMLParseError

from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments import lexers




class HtmlTool(object):

    def __init__(self, html):
        self.html_parsed = BeautifulSoup(html, 'lxml')


    def _highlight(self, code_string, lexer):
        """
        Highlight the code passed as string using pygments with the lexer provided

        returns the code pygmented wraped inside a div
        """
        code_pygmented =  highlight(code_string, lexer, HtmlFormatter(full=False,
                                                                      linenos='table',
                                                                      anchorlinenos=True,
                                                                      linespans='line'))
        code_dom = BeautifulSoup(code_pygmented)

        #In this way we don't care about the element returned by pygments
        #We have to wrap the code inside a div to maintain a good level of abstraction
        code_highlighted = code_dom.body.contents[0].wrap(BeautifulSoup().new_tag("div", **{'class':''}))
        #add an highlighted class to mark this code as already highlighted
        code_highlighted.attrs['class'].append('highlighted')

        return  code_highlighted



    def get_html_parsed_as_string(self):
        return unicode(self.html_parsed.body.encode_contents(),'utf-8')


    def apply_pygments_to_code_tags(self):


        if self.html_parsed == None:
            raise HTMLParseError

        code_elements = self._extract_tags('div.techblog_code')


        #The list of the returned codes to the model. This list is a list of couple (element, data_attrs)
        #The data_attrs is a dict containing only the data_* attribute of the div pyg_div element
        codes_to_model = []

        for code in code_elements:

            #Check if the div is already pygmented
            if 'highlighted' not in code.attrs['class']:
                #We have to pygment
                lexer = lexers.get_lexer_by_name(code.attrs['data-language'])
                #set the readable name of the lexer inside the tag, this is useful when we'll create the model
                code.attrs['data-language'] = lexer.name
                code_highlight = self._highlight(code.pre.string, lexer)
                code_highlight.attrs = self._merge_attrs(code.attrs, code_highlight.attrs)
                code.replace_with(code_highlight)
            else:
                #The cod is already pygmented
                code_highlight = code

            data_attrs = self._build_data_attrs(code_highlight.attrs)
            codes_to_model.append((unicode(code_highlight),data_attrs))


        return codes_to_model



    def _extract_tags(self, css_selector):

        return self.html_parsed.select(css_selector)


    def _build_data_attrs(self, attrs):

        keys = [x for x in attrs.keys() if x.startswith('data')]
        data_attr = {}
        for k in keys:
            data_attr[k]= attrs[k]

        return  data_attr

    def _merge_attrs(self, code_attrs, highlight_attrs):

        new_attrs = dict()
        new_attrs.update(code_attrs)
        for (k,v) in highlight_attrs.iteritems():
            if k not in new_attrs:
                new_attrs[k] = v
            else:
                new_attrs[k].extend(v)

        return new_attrs



class TechblogHtmlFormatter(HtmlFormatter):
    pass

