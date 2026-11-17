"""Execute every cell in a fresh kernel, then export a standalone HTML report."""
import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]

def main():
    path = next((ROOT / 'notebooks').glob('*.ipynb'))
    nb = nbformat.read(path, as_version=4)
    km = KernelManager(kernel_name='python3')
    km.kernel_spec.argv[0] = sys.executable
    os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
    os.environ['WIFI_N_JOBS'] = '2'
    client = NotebookClient(nb, km=km, timeout=1800,
                            resources={'metadata': {'path': str(ROOT)}},
                            allow_errors=False)
    def progress(cell_index, **kwargs):
        print(f'Executing cell {cell_index + 1}/{len(nb.cells)}', flush=True)
    client.on_cell_start = progress
    try:
        client.execute()
    except Exception:
        nbformat.write(nb, ROOT / '.verification' / 'failed_execution.ipynb')
        raise
    nbformat.write(nb, path)
    report_dir = ROOT / 'reports'
    report_dir.mkdir(exist_ok=True)
    body, _ = HTMLExporter(embed_images=True).from_notebook_node(nb)
    style = '''<style>
    @media print {
      @page { size: A4 landscape; margin: 12mm; }
      body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      .jp-Cell { break-inside: auto; }
      pre { white-space: pre-wrap !important; overflow-wrap: anywhere; }
      .jp-OutputArea-output { overflow: visible !important; }
      table { font-size: 9px; max-width: 100%; }
      td, th { white-space: normal !important; overflow-wrap: anywhere; }
      img { max-width: 100% !important; object-fit: contain; }
    }
    </style>'''
    body = body.replace('</head>', style + '</head>')
    (report_dir / 'wifi_room_classification.html').write_text(body, encoding='utf-8')
    count = sum(c.cell_type == 'code' for c in nb.cells)
    assert all(c.execution_count is not None for c in nb.cells if c.cell_type == 'code')
    assert not any(o.output_type == 'error' for c in nb.cells if c.cell_type == 'code' for o in c.outputs)
    print(f'PASS: {count} code cells executed; notebook and HTML saved.', flush=True)

if __name__ == '__main__':
    main()
