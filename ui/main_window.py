from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton,
    QTabWidget, QLabel, QHBoxLayout, QDockWidget, QTableView, QHeaderView,
    QMessageBox, QAbstractItemView, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QAbstractTableModel    

from core.calculator import CalculatorEngine
from core.history import HistoryManager
from ui.graph_widget import GraphWidget

# --- Helper class for History Table ---
class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
        return None
    
    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setMinimumSize(400, 650) # Taller window for the new layout

        self.calc_engine = CalculatorEngine()
        self.history_manager = HistoryManager()
        self.current_mode = 'DEG' # Matches screenshot default

        self._create_menu_bar()
        self._setup_main_ui()
        self._create_history_dock()

        # Load the Dark Theme Stylesheet
        try:
            with open("assets/style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: style.qss not found.")

    def _create_menu_bar(self):
        # We can implement a custom hamburger menu later, keeping standard for now
        menu = self.menuBar()
        view_menu = menu.addMenu("&View")
        self.toggle_history_action = view_menu.addAction("&History Panel")
        self.toggle_history_action.setCheckable(True)
        self.toggle_history_action.triggered.connect(self._toggle_history_dock)

    def _setup_main_ui(self):
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0) # Edge to edge look
        main_layout.setSpacing(0)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.tabs = QTabWidget()
        self.tab_calc = QWidget()
        self.tab_graph = QWidget()

        self.tabs.addTab(self.tab_calc, "Scientific")
        self.tabs.addTab(self.tab_graph, "Graphing")

        self._setup_calculator_tab()
        self._setup_graphing_tab()

        main_layout.addWidget(self.tabs)

    def _setup_calculator_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. Display Screen (Large, right aligned)
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(80) # Bigger display
        layout.addWidget(self.display)

        # 2. Mode & Memory Row (DEG, F-E, Memory)
        mem_layout = QHBoxLayout()
        self.mode_label = QPushButton("DEG")
        self.mode_label.setFlat(True)
        self.mode_label.clicked.connect(self._toggle_mode) # Click to toggle DEG/RAD
        self.mode_label.setStyleSheet("text-align: left; font-weight: bold; color: white;")
        
        fe_btn = QPushButton("F-E")
        fe_btn.setFlat(True)
        
        # Spacer to push memory buttons right
        mem_layout.addWidget(self.mode_label)
        mem_layout.addWidget(fe_btn)
        mem_layout.addStretch()

        # Simple Memory Placeholders
        for m_text in ["MC", "MR", "M+", "M-", "MS"]:
            m_btn = QPushButton(m_text)
            m_btn.setFlat(True)
            m_btn.setStyleSheet("color: white;")
            mem_layout.addWidget(m_btn)
        
        layout.addLayout(mem_layout)

        # 3. The Grid (5 Columns, 7 Rows)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)

        # Grid Map matching the screenshot
        # (Text, Row, Col, Type)
        buttons_map = [
            # Row 1
            ('2nd', 0, 0, 'func'), ('pi', 0, 1, 'func'), ('e', 0, 2, 'func'), ('C', 0, 3, 'func'), ('⌫', 0, 4, 'func'),
            # Row 2
            ('x^2', 1, 0, 'op'), ('1/x', 1, 1, 'op'), ('|x|', 1, 2, 'func'), ('exp', 1, 3, 'func'), ('mod', 1, 4, 'op'),
            # Row 3
            ('sqrt', 2, 0, 'func'), ('(', 2, 1, 'func'), (')', 2, 2, 'func'), ('n!', 2, 3, 'func'), ('/', 2, 4, 'op'),
            # Row 4
            ('x^y', 3, 0, 'op'), ('7', 3, 1, 'num'), ('8', 3, 2, 'num'), ('9', 3, 3, 'num'), ('*', 3, 4, 'op'),
            # Row 5
            ('10^x', 4, 0, 'op'), ('4', 4, 1, 'num'), ('5', 4, 2, 'num'), ('6', 4, 3, 'num'), ('-', 4, 4, 'op'),
            # Row 6
            ('log', 5, 0, 'func'), ('1', 5, 1, 'num'), ('2', 5, 2, 'num'), ('3', 5, 3, 'num'), ('+', 5, 4, 'op'),
            # Row 7
            ('ln', 6, 0, 'func'), ('+/-', 6, 1, 'func'), ('0', 6, 2, 'num'), ('.', 6, 3, 'num'), ('=', 6, 4, 'eq')
        ]

        for text, r, c, btn_type in buttons_map:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            # Styling based on Type
            if btn_type == 'num':
                btn.setObjectName("num-btn")
                btn.clicked.connect(lambda checked, t=text: self._on_button_clicked(t))
            elif btn_type == 'eq':
                btn.setObjectName("equal-btn")
                btn.clicked.connect(self._on_equal_clicked)
            elif btn_type == 'func':
                if text == 'C':
                    btn.clicked.connect(lambda: self.display.setText("0"))
                elif text == '⌫':
                    btn.clicked.connect(self._on_backspace)
                elif text == '+/-':
                    btn.clicked.connect(self._on_negate)
                elif text == '|x|':
                    btn.clicked.connect(lambda: self._on_button_clicked("abs("))
                elif text == 'n!':
                    btn.clicked.connect(lambda: self._on_button_clicked("factorial("))
                else:
                    # Generic function handler
                    btn.clicked.connect(lambda checked, t=text: self._on_button_clicked(t + '(' if t not in ['(', ')', 'pi', 'e'] else t))
            elif btn_type == 'op':
                # Map special operators
                val = text
                if text == 'x^y': val = '^'
                if text == '10^x': val = '10^'
                if text == 'mod': val = '%'
                if text == 'x^2': val = '^2'
                if text == '1/x': val = '1/'
                btn.clicked.connect(lambda checked, t=val: self._on_button_clicked(t))

            grid_layout.addWidget(btn, r, c)

        layout.addLayout(grid_layout)
        self.tab_calc.setLayout(layout)

    def _setup_graphing_tab(self):
        layout = QVBoxLayout()
        input_layout = QGridLayout()
        
        # Styled inputs for graphing
        self.func_input = QLineEdit("sin(x)")
        self.func_input.setStyleSheet("font-size: 16px; border: 1px solid #555;")
        self.x_min_input = QLineEdit("-10")
        self.x_min_input.setStyleSheet("border: 1px solid #555;")
        self.x_max_input = QLineEdit("10")
        self.x_max_input.setStyleSheet("border: 1px solid #555;")
        
        plot_btn = QPushButton("Plot")
        plot_btn.setObjectName("equal-btn") # Reuse blue button style
        plot_btn.clicked.connect(self._on_plot_clicked)

        input_layout.addWidget(QLabel("f(x)="), 0, 0)
        input_layout.addWidget(self.func_input, 0, 1, 1, 3)
        input_layout.addWidget(QLabel("Min X:"), 1, 0)
        input_layout.addWidget(self.x_min_input, 1, 1)
        input_layout.addWidget(QLabel("Max X:"), 1, 2)
        input_layout.addWidget(self.x_max_input, 1, 3)
        input_layout.addWidget(plot_btn, 2, 3)

        layout.addLayout(input_layout)
        self.graph_widget = GraphWidget()
        layout.addWidget(self.graph_widget)
        self.tab_graph.setLayout(layout)

    def _create_history_dock(self):
        self.history_dock = QDockWidget("History", self)
        self.history_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.history_table = QTableView()
        self.history_model = PandasModel(self.history_manager.get_history())
        self.history_table.setModel(self.history_model)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_dock.setWidget(self.history_table)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.history_dock)
        self.history_dock.hide()

    # --- Logic ---
    def _on_button_clicked(self, text):
        if self.display.text() == "0":
            self.display.clear()
        self.display.setText(self.display.text() + text)

    def _on_backspace(self):
        text = self.display.text()
        self.display.setText(text[:-1] if len(text) > 0 else "0")

    def _on_negate(self):
        # Simple negation logic
        text = self.display.text()
        if text.startswith("-"):
            self.display.setText(text[1:])
        else:
            self.display.setText("-" + text)

    def _on_equal_clicked(self):
        expression = self.display.text()
        # Pass current mode to engine
        self.calc_engine.set_mode(self.current_mode)
        result = self.calc_engine.evaluate(expression)
        self.display.setText(result)
        self.history_manager.add_entry(expression, result)
        self.history_model.update_data(self.history_manager.get_history())

    def _toggle_mode(self):
        if self.current_mode == 'DEG':
            self.current_mode = 'RAD'
            self.mode_label.setText("RAD")
        else:
            self.current_mode = 'DEG'
            self.mode_label.setText("DEG")

    def _toggle_history_dock(self, checked):
        if checked:
            self.history_dock.show()
        else:
            self.history_dock.hide()

    def _on_plot_clicked(self):
        try:
            func = self.func_input.text()
            mn = float(self.x_min_input.text())
            mx = float(self.x_max_input.text())
            self.graph_widget.plot_function(func, mn, mx, mode=self.current_mode)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))