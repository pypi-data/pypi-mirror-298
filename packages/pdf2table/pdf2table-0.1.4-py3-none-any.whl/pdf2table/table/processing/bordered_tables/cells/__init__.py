# coding: utf-8
from typing import List

from pdf2table.table.processing.bordered_tables.cells.deduplication import deduplicate_cells
from pdf2table.table.processing.bordered_tables.cells.identification import get_cells_dataframe
from pdf2table.table.structure.models import Line
from pdf2table.table.structure.table_object import Cell

def get_cells(horizontal_lines: List[Line], vertical_lines: List[Line]) -> List[Cell]:
    """
    Identify cells from horizontal and vertical rows
    :param horizontal_lines: list of horizontal rows
    :param vertical_lines: list of vertical rows
    :return: list of all cells in image
    """
    # Create dataframe with cells from horizontal and vertical rows
    df_cells = get_cells_dataframe(horizontal_lines=horizontal_lines,
                                   vertical_lines=vertical_lines)

    # Handle case of empty cells
    if df_cells.collect().height == 0:
        return []

    # Deduplicate cells
    df_cells_dedup = deduplicate_cells(df_cells=df_cells)

    # Convert to Cell objects
    cells = [Cell(x1=row["x1"], x2=row["x2"], y1=row["y1"], y2=row["y2"])
             for row in df_cells_dedup.collect().to_dicts()]

    return cells
