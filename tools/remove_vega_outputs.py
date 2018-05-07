"""
Tool to remove vegalite outputs from a notebook.

For notebooks with a lot of embedded data, this helps keep the notebook size
manageable.
"""

import nbformat

def _strip(output, ignore_mimetypes=('application/vnd.vegalite.v2+json',)):
    if 'data' in output:
        output = output.copy()
        output['data'] = {k: v for k, v in output['data'].items()
                          if k not in ignore_mimetypes}
    return output


def strip_vega_outputs(notebook):
    for cell in notebook['cells']:
        if 'outputs' not in cell:
            continue
        cell['outputs'] = [_strip(output) for output in cell['outputs']]
    return notebook


def main(input_filename, output_filename):
    notebook = nbformat.read(input_filename, as_version=nbformat.NO_CONVERT)
    stripped = strip_vega_outputs(notebook)
    with open(output_filename, 'w') as f:
        nbformat.write(stripped, f)
    return output_filename


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    else:
        output_filename = filename + '-stripped'
    main(filename, output_filename)
    
