import os
import sys
import re
import requests
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def compile_tikz_to_png(tikz_code, output_path, fsize='45px', target_width=1920):
    """
    Compiles TikZ code to a PNG image using the QuickLaTeX API,
    and resizes it to Full HD (target_width=1920) using PIL Image.
    """
    # Define standard preamble with math, tikz, and pgfplots packages
    preamble = (
        r"\usepackage[utf8]{vietnam}"
        r"\usepackage{amsmath,amssymb}"
        r"\usepackage{tikz}"
        r"\usepackage{circuitikz}"
        r"\usepackage{chemfig}"
        r"\usepackage{pgfplots}"
        r"\pgfplotsset{compat=1.18}"
        r"\usetikzlibrary{patterns,decorations.pathreplacing,shapes,arrows,positioning,calc,arrows.meta,decorations.pathmorphing,decorations.markings,intersections,backgrounds,shadows,angles,quotes}"
    )
    
    # QuickLaTeX POST parameters
    payload = {
        'formula': tikz_code,
        'fsize': fsize,
        'fcolor': '000000',
        'mode': '0',
        'out': '1',
        'preamble': preamble
    }
    
    import urllib.parse
    encoded_data = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)
    
    try:
        response = requests.post(
            'https://quicklatex.com/latex3.f',
            data=encoded_data,
            headers={'Content-Type': 'application/x-www-form-urlenc
















































        test_code = r"""
        \begin{tikzpicture}[scale=1.2, >=stealth]
            % Trục tọa độ
            \draw[->, thick] (0,-1.2) -- (0,5.5) node[left] {$t~(^{\circ}\text{C})$};
            \draw[->, thick] (0,0) -- (9,0) node[below] {$Q~(\text{kJ})$};
            
            % Các đường gióng nhiệt độ
            \draw[dashed, gray] (0,5) node[left, black] {$100$} -- (8,5);
            \draw[dashed, gray] (0,-0.5) node[left, black] {$-10$} -- (0.5,-0.5);
            \node[left] at (0,0) {$0$};
            
            % Đường cong đun nóng
            \draw[very thick, red] (0.5,-0.5) -- (1.5,0) -- (3,0) -- (4.5,5) -- (8,5);
            
            % Các điểm mốc
            \filldraw[blue] (0.5,-0.5) circle (1.5pt) node[below right, black] {\small A};
            \filldraw[blue] (1.5,0) circle (1.5pt) node[above left, black] {\small B};
            \filldraw[blue] (3,0) circle (1.5pt) node[above right, black] {\small C};
            \filldraw[blue] (4.5,5) circle (1.5pt) node[above left, black] {\small D};
            \filldraw[blue] (8,5) circle (1.5pt) node[above right, black] {\small E};
        \end{tikzpicture}
        """
        dest = r"c:\Users\Admin\.antigravity-ide\soạn tài liệu\output\generated_docs\heating_curve_test.png"
        compile_tikz_to_png(test_code, dest)
    else:
        # Read from file or string
        input_src = sys.argv[1]
        out_path = sys.argv[2]
        
        # If input_src is a path to a file, read it, otherwise treat it as raw TikZ code
        if os.path.exists(input_src):
            with open(input_src, 'r', encoding='utf-8') as f:
                code = f.read()
        else:
            code = input_src
            
        compile_tikz_to_png(code, out_path)
