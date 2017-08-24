class HtmlPageBuilder:

    PAGE_HEADER = ""\
"""
<!DOCTYPE html>
<html lang="en">
<head lang=en>
    <meta charset="windows-1250">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Report</title>
    <link 
        rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" 
        integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" 
        crossorigin="anonymous">
</head>
<body>
    <div class="container">
    """

    PAGE_FOOTER = ""\
"""
    </div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script 
    src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" 
    integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" 
    crossorigin="anonymous"></script>
</body>
</html>
"""

    @staticmethod
    def make_indent(indent_level=0):
        return "\t" * indent_level

    @staticmethod
    def open_tag(tag="", css_class="", indent_level=0):
        output = HtmlPageBuilder.make_indent(indent_level)
        output += '<{} class="{}">\n'.format(tag, css_class)
        return output

    @staticmethod
    def close_tag(tag="div", indent_level=0):
        output = HtmlPageBuilder.make_indent(indent_level)
        output += "</{}>\n".format(tag)
        return output

    @staticmethod
    def add_text(text="", indent_level=0):
        output = HtmlPageBuilder.make_indent(indent_level)
        output += str(text) + "\n"
        return output

    @staticmethod
    def add_page_element(tag="div", css_class="", indent_level=0, text=""):
        output = HtmlPageBuilder.open_tag(tag, css_class, indent_level)
        output += HtmlPageBuilder.add_text(text, indent_level + 1)
        output += HtmlPageBuilder.close_tag(tag, indent_level)
        return output

    @staticmethod
    def build_table_header(table_data, tag, indent_level):
        output = HtmlPageBuilder.open_tag('tr', '', indent_level)

        for row in table_data:
            output += HtmlPageBuilder.open_tag(tag, '', indent_level+1)
            output += HtmlPageBuilder.add_text(row, indent_level + 2)
            output += HtmlPageBuilder.close_tag(tag, indent_level + 1)

        output += HtmlPageBuilder.close_tag('tr', indent_level)
        return output

    @staticmethod
    def build_table_rows(table_data, tag, indent_level):
        output = ""

        for row in table_data:
            output += HtmlPageBuilder.open_tag('tr', '', indent_level)

            for cell in row:
                output += HtmlPageBuilder.open_tag(tag, '', indent_level + 1)
                output += HtmlPageBuilder.add_text(cell, indent_level + 2)
                output += HtmlPageBuilder.close_tag(tag, indent_level + 1)

            output += HtmlPageBuilder.close_tag('tr', indent_level)

        return output

    @staticmethod
    def build_table(table_headers=[], table_data=[], indent_level=0):
        output = HtmlPageBuilder.open_tag('table', 'table', indent_level)
        output += HtmlPageBuilder.build_table_header(table_headers, 'th', indent_level + 1)
        output += HtmlPageBuilder.build_table_rows(table_data, 'td', indent_level + 1)
        output += HtmlPageBuilder.close_tag('table', indent_level)

        return output
