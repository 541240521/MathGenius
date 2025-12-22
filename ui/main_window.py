import os
import sys

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSpinBox, QPushButton, QCheckBox, QFileDialog, QMessageBox, QFrame,
    QSlider, QGroupBox, QLineEdit, QScrollArea, QApplication
)
from PyQt6.QtCore import Qt
from core.presets import GradePresets, CalculationMethods
from core.math_engine import QuestionGenerator
from ui.preview_canvas import PreviewCanvas
from services.pdf_exporter import PDFExporter
from services.word_exporter import WordExporter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MathGenius Desktop PRO")
        self.resize(1200, 900)
        
        self.generator = QuestionGenerator()
        self.current_questions = []
        self.current_config = GradePresets.L1
        
        self._init_ui()
        self.on_grade_changed()

    def _init_ui(self):
        """Initialize the main user interface."""
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        self._setup_styles()
        
        # Left Panel
        self.settings_scroll = QScrollArea()
        self.settings_scroll.setFixedWidth(420)
        self.settings_scroll.setWidgetResizable(True)
        self.settings_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.settings_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.settings_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.settings_content = QWidget()
        self.settings_content.setObjectName("settingsContent")
        self._setup_left_panel()
        self.settings_scroll.setWidget(self.settings_content)
        
        # Right Panel
        self.preview_panel = QFrame()
        self.preview_panel.setStyleSheet("background-color: #f0f2f5; border-radius: 20px;")
        self._setup_right_panel()
        
        main_layout.addWidget(self.settings_scroll)
        main_layout.addWidget(self.preview_panel, 1)

    def _setup_styles(self):
        """Configure global widget styles."""
        self.setStyleSheet("""
            #settingsContent { background-color: #ffffff; }
            QLabel { color: #666666; font-size: 12px; font-weight: bold; }
            QGroupBox { border: none; margin-top: 10px; }
            QGroupBox::title { color: #333333; font-size: 14px; font-weight: bold; }
            
            /* Inputs */
            QComboBox, QSpinBox, QLineEdit {
                background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
                padding: 8px 12px; min-height: 28px; color: #1e293b; font-size: 15px; font-weight: bold;
            }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox::down-arrow {
                image: none; border-left: 5px solid transparent; border-right: 5px solid transparent;
                border-top: 6px solid #94a3b8; margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #4b4b4b; color: white; selection-background-color: #3b82f6;
                selection-color: white; border-radius: 12px; outline: none; padding: 5px;
            }
            QComboBox QAbstractItemView::item { min-height: 40px; padding-left: 15px; border-radius: 8px; }

            /* SpinBox Arrows */
            QSpinBox::up-button, QSpinBox::down-button { border: none; background: transparent; width: 20px; margin-right: 8px; }
            QSpinBox::up-button { subcontrol-position: top right; height: 16px; margin-top: 4px; }
            QSpinBox::down-button { subcontrol-position: bottom right; height: 16px; margin-bottom: 4px; }
            QSpinBox::up-arrow { border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 6px solid #94a3b8; }
            QSpinBox::down-arrow { border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #94a3b8; }

            /* CheckBox & Buttons */
            QCheckBox { color: #475569; font-size: 14px; font-weight: bold; spacing: 8px; }
            QCheckBox::indicator {
                width: 12px; height: 12px; border: 1px solid #cbd5e1; border-radius: 3px; background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #0f172a; border-color: #0f172a;
                image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
            }
            QCheckBox::indicator:hover { border-color: #0f172a; }

            QPushButton { border-radius: 12px; padding: 12px; font-weight: bold; }
            #primaryBtn { 
                background-color: #0f172a; 
                color: #94a3b8; 
                border: none;
                border-radius: 20px; 
                padding: 8px 24px; 
                font-size: 14px;
                min-height: 40px;
            }
            #primaryBtn:hover {
                background-color: #1e293b;
            }
            #secondaryBtn { background-color: white; border: 2px solid #e2e8f0; color: #334155; }
            
            /* Logo & Title */
            #logo { font-size: 28px; color: #cbd5e1; font-weight: 900; font-family: 'Arial Black'; margin-right: 5px; }
            #title { font-size: 20px; color: #2c3e50; font-weight: bold; }

            /* Slider */
            QSlider::groove:horizontal { border: 1px solid #e0e4e8; height: 6px; background: #f5f7fa; border-radius: 3px; }
            QSlider::handle:horizontal { background: #3498db; width: 18px; height: 18px; margin: -7px 0; border-radius: 9px; }
        """)

    def _setup_left_panel(self):
        # Use a container widget with layout to hold everything
        container = QWidget(self.settings_content)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(12)
        
        # Ensure the content widget's layout is set
        main_v_layout = QVBoxLayout(self.settings_content)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.addWidget(container)

        # Header
        header = QHBoxLayout()
        logo, title = QLabel("M"), QLabel("MathGenius")
        logo.setObjectName("logo"); title.setObjectName("title")
        header.addWidget(logo); header.addWidget(title); header.addStretch()
        layout.addLayout(header)

        # Controls
        self.grade_combo = self._create_combo(GradePresets.get_all(), self.on_grade_changed)
        self.calc_combo = self._create_combo(CalculationMethods.get_all(), self.generate_questions)
        layout.addWidget(QLabel("🎓 选择年级预设")); layout.addWidget(self.grade_combo)
        layout.addWidget(QLabel("🔡 选择计算方式")); layout.addWidget(self.calc_combo)

        # Parameters
        params_group = QGroupBox("⚙️ 试卷核心参数")
        params_layout = QVBoxLayout(params_group)
        
        self.title_input = QLineEdit("数学口算能力测试卷")
        self.title_input.textChanged.connect(self.update_preview)
        params_layout.addWidget(QLabel("试卷自定义大标题")); params_layout.addWidget(self.title_input)

        range_layout = QHBoxLayout()
        self.min_spin, self.max_spin = QSpinBox(), QSpinBox()
        for s, v in [(self.min_spin, 1), (self.max_spin, 20)]:
            s.setRange(0, 1000); s.setValue(v); range_layout.addWidget(s)
        params_layout.addWidget(QLabel("数值范围 (最小 - 最大)")); params_layout.addLayout(range_layout)

        self.blank_pos_combo = QComboBox()
        self.blank_pos_combo.addItem("结果未知 (A + B = ?)", "result")
        self.blank_pos_combo.addItem("随机项未知 (A + ? = C)", "random")
        self.blank_pos_combo.currentIndexChanged.connect(self.generate_questions)
        params_layout.addWidget(QLabel("填空位置")); params_layout.addWidget(self.blank_pos_combo)

        # Count & Page
        self.count_val_label = QLabel("60")
        self.count_slider = self._create_slider(20, 100, 60, self.on_count_slider_changed)
        h = QHBoxLayout(); h.addWidget(QLabel("# 每页题量")); h.addWidget(self.count_val_label)
        params_layout.addLayout(h); params_layout.addWidget(self.count_slider)

        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 100); self.page_spin.setValue(10)
        self.page_spin.valueChanged.connect(self.on_page_spin_changed)
        self.page_slider = self._create_slider(1, 100, 10, self.on_page_slider_changed)
        h = QHBoxLayout(); h.addWidget(QLabel("📄 生成总页数")); h.addWidget(self.page_spin)
        params_layout.addLayout(h); params_layout.addWidget(self.page_slider)
        layout.addWidget(params_group)

        # Options
        options_box = QFrame()
        options_box.setStyleSheet("background-color: #f1f5f9; border-radius: 12px; padding: 10px;")
        options_layout = QHBoxLayout(options_box)
        options_layout.setContentsMargins(15, 5, 15, 5)
        self.show_answer_cb = self._create_check("实时预览答案", self.update_preview)
        self.gen_ans_page_cb = self._create_check("生成答案页", self.update_preview, True)
        options_layout.addWidget(self.show_answer_cb)
        options_layout.addStretch()
        options_layout.addWidget(self.gen_ans_page_cb)
        layout.addWidget(options_box)

        layout.addSpacing(20)

        export_layout = QHBoxLayout()
        self.pdf_btn = self._create_btn("📄 PDF 导出", self.export_pdf)
        self.word_btn = self._create_btn("💾 Word 导出", self.export_word)
        export_layout.addWidget(self.pdf_btn); export_layout.addWidget(self.word_btn)
        layout.addLayout(export_layout); layout.addStretch()

    def _create_combo(self, items, func):
        cb = QComboBox()
        for i in items: cb.addItem(i["name"], i["id"])
        cb.currentIndexChanged.connect(func)
        return cb

    def _create_slider(self, min_v, max_v, curr, func):
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(min_v, max_v); s.setValue(curr); s.valueChanged.connect(func)
        return s

    def _create_check(self, text, func, checked=False):
        c = QCheckBox(text)
        c.setChecked(checked); c.stateChanged.connect(func)
        return c

    def _create_btn(self, text, func):
        b = QPushButton(text); b.clicked.connect(func)
        b.setObjectName("secondaryBtn")
        return b

    def _setup_right_panel(self):
        layout = QVBoxLayout(self.preview_panel)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.preview_canvas = PreviewCanvas()
        layout.addWidget(self.preview_canvas)
        
        # Bottom Controls (Refresh + Pagination)
        nav = QHBoxLayout()
        
        # Refresh Button
        self.refresh_btn = QPushButton("↻  重新生成题目")
        self.refresh_btn.setObjectName("primaryBtn")
        self.refresh_btn.clicked.connect(self.generate_questions)
        self.refresh_btn.setMinimumHeight(40)
        self.refresh_btn.setFixedWidth(160)
        nav.addWidget(self.refresh_btn)
        
        nav.addStretch()
        
        # Pagination
        self.prev_btn = QPushButton("◀ 上一页")
        self.next_btn = QPushButton("下一页 ▶")
        self.page_label = QLabel("第 1 / 1 页")
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.page_label)
        nav.addWidget(self.next_btn)
        nav.addStretch()
        
        layout.addLayout(nav)

    def on_grade_changed(self):
        grade_id = self.grade_combo.currentData()
        self.current_config = GradePresets.get_by_id(grade_id).copy()
        self.min_spin.setValue(self.current_config["min_val"])
        self.max_spin.setValue(self.current_config["max_val"])
        self.count_slider.setValue(self.current_config.get("default_count", 60))
        
        idx = self.calc_combo.findData(self.current_config.get("default_calc", "basic_add_sub"))
        if idx >= 0: self.calc_combo.setCurrentIndex(idx)
        self.generate_questions()

    def on_count_slider_changed(self, value):
        snapped = round(value / 20) * 20
        if snapped != value:
            self.count_slider.setValue(snapped)
            return
        self.count_val_label.setText(str(snapped))
        self.generate_questions()

    def on_page_slider_changed(self, value):
        self.page_spin.blockSignals(True)
        self.page_spin.setValue(value)
        self.page_spin.blockSignals(False)
        self.generate_questions()

    def on_page_spin_changed(self, value):
        self.page_slider.blockSignals(True)
        self.page_slider.setValue(value)
        self.page_slider.blockSignals(False)
        self.generate_questions()

    def generate_questions(self):
        calc_id = self.calc_combo.currentData()
        self.current_config.update(CalculationMethods.get_by_id(calc_id))
        self.current_config.update({
            "min_val": self.min_spin.value(),
            "max_val": self.max_spin.value(),
            "blank_pos": self.blank_pos_combo.currentData()
        })
        
        total = self.count_slider.value() * self.page_spin.value()
        self.current_questions = self.generator.generate(total, self.current_config)
        self.update_preview()

    def update_preview(self):
        self.preview_canvas.update_data(
            self.current_questions, 4, self.show_answer_cb.isChecked(),
            self.title_input.text(), f"{self.current_config['id']} STANDARD",
            questions_per_page=self.count_slider.value(),
            with_answer_pages=self.gen_ans_page_cb.isChecked()
        )
        self.update_pagination_ui()

    def prev_page(self):
        if self.preview_canvas.set_page(self.preview_canvas.current_page - 1): self.update_pagination_ui()

    def next_page(self):
        if self.preview_canvas.set_page(self.preview_canvas.current_page + 1): self.update_pagination_ui()

    def update_pagination_ui(self):
        curr, total = self.preview_canvas.current_page + 1, self.preview_canvas.total_pages
        self.page_label.setText(f"第 {curr} / {total} 页")
        self.prev_btn.setEnabled(curr > 1)
        self.next_btn.setEnabled(curr < total)

    def export_pdf(self):
        if not self.current_questions: return
        path, _ = QFileDialog.getSaveFileName(self, "保存 PDF", "math_sheet.pdf", "PDF Files (*.pdf)")
        if path:
            try:
                PDFExporter().export(
                    path, self.current_questions, with_answers=self.gen_ans_page_cb.isChecked(),
                    title=self.title_input.text(), cols=4,
                    grade_tag=f"{self.current_config['id']} STANDARD",
                    questions_per_page=self.count_slider.value()
                )
                QMessageBox.information(self, "成功", "PDF 导出成功！")
            except Exception as e: QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def export_word(self):
        if not self.current_questions: return
        path, _ = QFileDialog.getSaveFileName(self, "保存 Word", "math_sheet.docx", "Word Files (*.docx)")
        if path:
            try:
                WordExporter().export(
                    path, self.current_questions, with_answers=self.gen_ans_page_cb.isChecked(),
                    title=self.title_input.text(), cols=4,
                    grade_tag=f"{self.current_config['id']} STANDARD",
                    questions_per_page=self.count_slider.value()
                )
                QMessageBox.information(self, "成功", "Word 导出成功！")
            except Exception as e: QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
