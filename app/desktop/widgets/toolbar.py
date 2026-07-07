from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar


class MainToolBar(QToolBar):
    """Main desktop toolbar."""

    def __init__(
        self,
        new_action: QAction,
        open_csv_action: QAction,
        open_excel_action: QAction,
        save_action: QAction,
        run_action: QAction,
        export_action: QAction,
        parent=None,
    ) -> None:
        super().__init__("Principal", parent)

        self.setMovable(False)

        self.addAction(new_action)
        self.addSeparator()
        self.addAction(open_csv_action)
        self.addAction(open_excel_action)
        self.addSeparator()
        self.addAction(save_action)
        self.addSeparator()
        self.addAction(run_action)
        self.addAction(export_action)