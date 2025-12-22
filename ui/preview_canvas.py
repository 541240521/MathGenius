from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QRectF
import math

class PreviewCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.questions = []
        self.cols = 4
        self.show_answers = False
        self.title = "数学口算能力测试卷"
        self.grade_tag = "L1 STANDARD"
        self.current_page = 0
        self.total_pages = 1
        self.questions_per_page = 60
        self.setMinimumSize(400, 600)

    def update_data(self, questions, cols, show_answers, title="数学口算能力测试卷", grade_tag="L1 STANDARD", questions_per_page=60, with_answer_pages=True):
        self.questions = questions
        self.cols = cols
        self.show_answers = show_answers
        self.title = title
        self.grade_tag = grade_tag
        self.questions_per_page = questions_per_page
        self.with_answer_pages = with_answer_pages
        
        # Calculate total pages
        if not self.questions:
            self.total_q_pages = 1
            self.total_pages = 1
        else:
            self.total_q_pages = math.ceil(len(self.questions) / self.questions_per_page)
            if self.with_answer_pages:
                self.total_pages = self.total_q_pages * 2
            else:
                self.total_pages = self.total_q_pages
            
        if self.current_page >= self.total_pages:
            self.current_page = self.total_pages - 1
        if self.current_page < 0:
            self.current_page = 0
            
        self.update()

    def set_page(self, page_index):
        if 0 <= page_index < self.total_pages:
            self.current_page = page_index
            self.update()
            return True
        return False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        painter.fillRect(self.rect(), QColor("#f0f0f0"))

        widget_w = self.width()
        widget_h = self.height()
        margin = 20
        available_w = widget_w - 2 * margin
        available_h = widget_h - 2 * margin
        a4_ratio = 210 / 297
        
        if available_w / available_h > a4_ratio:
            page_h = available_h
            page_w = page_h * a4_ratio
        else:
            page_w = available_w
            page_h = page_w / a4_ratio
            
        page_x = (widget_w - page_w) / 2
        page_y = (widget_h - page_h) / 2
        
        page_rect = QRectF(page_x, page_y, page_w, page_h)
        painter.setBrush(QColor("white"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(page_rect)
        
        # Shadow
        painter.setBrush(QColor(0, 0, 0, 30))
        painter.drawRect(QRectF(page_x + 4, page_y + 4, page_w, page_h))
        painter.setBrush(QColor("white"))
        painter.setPen(QPen(QColor("#dcdcdc"), 1))
        painter.drawRect(page_rect)
        
        self._draw_content(painter, page_rect)

    def _draw_content(self, painter, rect):
        virtual_w = 595
        virtual_h = 842
        scale = rect.width() / virtual_w
        
        painter.save()
        painter.translate(rect.x(), rect.y())
        painter.scale(scale, scale)
        
        # Determine dynamic font size and row height based on questions_per_page
        layout_map = {
            20: {"font": 16, "row_h": 110, "y_start": 200},
            40: {"font": 14, "row_h": 55,  "y_start": 180},
            60: {"font": 12, "row_h": 38,  "y_start": 180},
            80: {"font": 10, "row_h": 28,  "y_start": 170},
            100: {"font": 9.5, "row_h": 23, "y_start": 165}
        }
        
        # Get config based on questions_per_page (which is per-page, constant across pages)
        target_count = self.questions_per_page
        conf = layout_map.get(target_count, layout_map[60])
        
        main_font_size = conf["font"]
        row_height = conf["row_h"]
        start_y = conf["y_start"]
            
        # 1. Title
        painter.setPen(QPen(QColor("#1a1a1a"), 2))
        font = QFont("Arial", 22, QFont.Weight.Bold)
        painter.setFont(font)
        title_to_draw = self.title if not self.show_answers else f"{self.title} (答案页)"
        painter.drawText(QRectF(0, 40, virtual_w, 50), Qt.AlignmentFlag.AlignCenter, title_to_draw)
        
        # 2. Bold Line under Title
        painter.setPen(QPen(QColor("#1a1a1a"), 3))
        painter.drawLine(40, 100, virtual_w - 40, 100)
        
        # 3. Header Info Lines
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        info_y = 135
        painter.drawText(40, info_y, "姓名：_________")
        painter.drawText(150, info_y, "班级：_________")
        painter.drawText(260, info_y, "学号：_________")
        painter.drawText(370, info_y, "日期：_________")
        painter.drawText(480, info_y, "得分：_________")
        
        # 4. Questions
        col_width = (virtual_w - 80) / self.cols
        
        # Determine if current page is an answer page
        is_preview_answer = self.show_answers or (self.with_answer_pages and self.current_page >= self.total_q_pages)
        
        # Adjust indices based on whether it's an answer page
        display_page_idx = self.current_page
        if self.with_answer_pages and self.current_page >= self.total_q_pages:
            display_page_idx = self.current_page - self.total_q_pages
            
        start_idx = display_page_idx * self.questions_per_page
        end_idx = min(start_idx + self.questions_per_page, len(self.questions))
        page_questions = self.questions[start_idx:end_idx]
        
        # Vertical numbering logic
        num_questions = len(page_questions)
        rows_per_page = math.ceil(num_questions / self.cols)
        
        for i, q in enumerate(page_questions):
            # i is the sequence in the list, we need to map it to vertical grid
            # Vertical mapping: column first, then row
            # For vertical layout: 
            # col = i // rows_per_page
            # row = i % rows_per_page
            
            col = i // rows_per_page
            row = i % rows_per_page
            
            # Recalculate global index for the question to keep numbering consistent
            # In vertical layout, the question at (row, col) has index:
            global_idx = start_idx + i 
            
            x = 40 + col * col_width
            y = start_y + row * row_height
            
            if y > virtual_h - 100:
                break
            
            # Question Number
            font.setPointSize(main_font_size - 3)
            font.setBold(False)
            painter.setFont(font)
            painter.setPen(QColor("#999999"))
            painter.drawText(x, y + 10, f"{i+1}.")
            
            # Question Text
            font.setPointSize(main_font_size)
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor("#1a1a1a"))
            
            q_text = q["question"]
            if not is_preview_answer:
                display_text = q_text + " ____"
            else:
                display_text = q_text + " " + q["answer"]
                
            painter.drawText(QRectF(x + 18, y, col_width - 20, row_height), 
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
                             display_text)
        
        # 5. Footer
        footer_y = virtual_h - 50
        painter.setPen(QPen(QColor("#1a1a1a"), 2))
        painter.drawLine(40, footer_y, virtual_w - 40, footer_y)
        
        # Left tag: Black background
        painter.setBrush(QColor("#1a1a1a"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(40, footer_y + 10, 140, 25, 4, 4)
        
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("white"))
        painter.drawText(QRectF(40, footer_y + 10, 140, 25), Qt.AlignmentFlag.AlignCenter, "MATHGENIUS SYSTEM PRO")
        
        # Middle: Page number
        painter.setPen(QColor("#1a1a1a"))
        page_label = f"PAGE {self.current_page + 1} / {self.total_pages}"
        if self.with_answer_pages and self.current_page >= self.total_q_pages:
            page_label += " (ANS)"
        painter.drawText(QRectF(0, footer_y + 10, virtual_w, 25), Qt.AlignmentFlag.AlignCenter, page_label)
        
        # Right tag: Border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor("#1a1a1a"), 1))
        painter.drawRoundedRect(virtual_w - 140, footer_y + 10, 100, 25, 4, 4)
        painter.drawText(QRectF(virtual_w - 140, footer_y + 10, 100, 25), Qt.AlignmentFlag.AlignCenter, self.grade_tag)
        
        painter.restore()
