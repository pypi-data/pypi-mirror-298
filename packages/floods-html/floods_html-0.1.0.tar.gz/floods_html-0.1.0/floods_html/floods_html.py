from floods_html import json_format as jf


def json_to_html(input, **kwargs):
    if type(input) is str:
        pydantic_data_object = jf.FHJSON.model_validate_json(input)
    elif type(input) is dict:
        pydantic_data_object = jf.FHJSON(**input)
    elif isinstance(input, jf.FHJSON):
        pydantic_data_object = input
    else:
        raise ValueError("Invalid input type. Must be either a JSON string, JSON object, or a FHJSON class instance.")
    html_output = []
    for entry in pydantic_data_object.data:
        html_entry = entry_to_html(entry, **kwargs)
        html_output.append(html_entry)
    return html_output


def entry_to_html(entry, **kwargs):
    if entry.type == "table":
        return table_to_html(entry.data, **kwargs)
    elif entry.type == "svg_figure":
        return figure_to_html(entry.data, **kwargs)
    else:
        raise ValueError("Unknown entry type: {}".format(entry.type))


def table_to_html(json, default_colour="FFFFFF", **kwargs):
    html_table_header = ""
    html_table_rows = ""

    table_row_html_template = '<td style="background-color: {colour}">{value}</td>'

    for table_header_entry in json.header:
        html_table_header += table_row_html_template.format(
            colour=table_header_entry.background_color
            if table_header_entry.background_color is not None
            else default_colour,
            value=table_header_entry.value or "",
        )

    for table_row in json.rows:
        html_table_row = ""
        for table_entry in table_row:
            html_table_row += table_row_html_template.format(
                colour=table_entry.background_color if table_entry.background_color is not None else default_colour,
                value=table_entry.value or "",
            )
        html_table_row = "<tr>" + html_table_row + "</tr>"
        html_table_rows += html_table_row

    table_html_template = """
    <h3>{title}</h3>
    <table class="table table-bordered">
        <thead><tr>{header}</tr></thead>
        <tbody>{body}</tbody>
    </table>
    """

    table_html = table_html_template.format(title=json.title, header=html_table_header, body=html_table_rows)

    return table_html


def figure_to_html(json, svg_location="", default_height=100, default_width=100, **kwargs):
    svg_file = svg_location + json.filename

    if svg_file[:4] == "http":
        figure_html_template = """
            <span>
                <h4>{title}</h4>
                <img src={imgname} width={width} height={height} />
            </span>
        """

        figure_html = figure_html_template.format(
            title=json.title,
            imgname=svg_file,
            width=json.width if json.width is not None else default_width,
            height=json.height if json.height is not None else default_height,
        )
    else:
        figure_html_template = """
        <div style="width: {width}px; height: {height}px">
            <span>
                <h4>{title}</h4>
                {svg}
            </span>
        </div>
        """

        svg_contents = open(svg_file, "r").read()
        svg_contents = svg_contents.replace("<svg", '<svg width="100%" height="100%"')

        figure_html = figure_html_template.format(
            title=json.title,
            svg=svg_contents,
            width=json.width if json.width is not None else default_width,
            height=json.height if json.height is not None else default_height,
        )

    return figure_html
