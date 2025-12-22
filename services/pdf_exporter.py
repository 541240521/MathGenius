from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import math

class PDFExporter:
    def __init__(self):
        # Register Chinese font
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            self.font_name = 'STSong-Light'
        except:
            self.font_name = 'Helvetica'

    def export(self, filepath, questions, with_answers=False, title="数学口算能力测试卷", cols=4, grade_tag="L1 STANDARD", questions_per_page=60):
        c = canvas.Canvas(filepath, pagesize=A4)
        
        # Calculate total pages for questions
        total_q_pages = max(1, (len(questions) + questions_per_page - 1) // questions_per_page)
        
        # Draw Questions Pages
        for p in range(total_q_pages):
            start_idx = p * questions_per_page
            end_idx = min(start_idx + questions_per_page, len(questions))
            page_questions = questions[start_idx:end_idx]
            
            self._draw_page(c, page_questions, title, is_answer=False, cols=cols, grade_tag=grade_tag, 
                            page_num=p+1, total_pages=total_q_pages, start_idx=start_idx, questions_per_page=questions_per_page)
            c.showPage()
        
        if with_answers:
            # For answers, we can often fit more per page, but for consistency let's use the same or slightly more
            # Let's use the same questions_per_page for simplicity
            total_ans_pages = total_q_pages
            for p in range(total_ans_pages):
                start_idx = p * questions_per_page
                end_idx = min(start_idx + questions_per_page, len(questions))
                page_questions = questions[start_idx:end_idx]
                
                self._draw_page(c, page_questions, title + " (参考答案)", is_answer=True, cols=cols, grade_tag=grade_tag, 
                                page_num=p+1, total_pages=total_ans_pages, start_idx=start_idx, questions_per_page=questions_per_page)
                c.showPage()
            
        c.save()

    def _draw_page(self, c, questions, title, is_answer, cols, grade_tag, page_num, total_pages, start_idx, questions_per_page):
        width, height = A4
        margin = 40 # Points
        
        # Determine layout based on questions_per_page
        layout_map = {
            20: {"font": 16, "row_h": 35 * mm, "y_start": height - 140},
            40: {"font": 14, "row_h": 18 * mm, "y_start": height - 130},
            60: {"font": 12, "row_h": 13 * mm, "y_start": height - 130},
            80: {"font": 10, "row_h": 10 * mm, "y_start": height - 125},
            100: {"font": 9.5, "row_h": 8 * mm, "y_start": height - 120}
        }
        
        conf = layout_map.get(questions_per_page, layout_map[60]) 
        main_font_size = conf["font"]
        row_height = conf["row_h"]
        y_cursor = conf["y_start"]
            
        # 1. Title
        c.setFont(self.font_name, 22)
        c.drawCentredString(width / 2, height - 50, title)
        
        # 2. Bold Line under Title
        c.setLineWidth(2)
        c.line(margin, height - 70, width - margin, height - 70)
        
        # 3. Header Info Lines
        c.setFont(self.font_name, 10)
        info_y = height - 95
        c.drawString(margin, info_y, "姓名：_________")
        c.drawString(margin + 110, info_y, "班级：_________")
        c.drawString(margin + 220, info_y, "学号：_________")
        c.drawString(margin + 330, info_y, "日期：_________")
        c.drawString(margin + 440, info_y, "得分：_________")
        
        # 4. Questions
        col_width = (width - 2 * margin) / cols
        
        rows_per_page = math.ceil(len(questions) / cols)
        
        for i, q in enumerate(questions):
            col = i // rows_per_page
            row = i % rows_per_page
            
            x = margin + col * col_width
            y = y_cursor - row * row_height
            
            if y < 60: # Avoid footer
                break
                
            q_num = f"{i+1}."
            c.setFont(self.font_name, main_font_size - 3)
            c.setFillColorRGB(0.6, 0.6, 0.6)
            c.drawString(x, y, q_num)
            
            c.setFont(self.font_name, main_font_size)
            c.setFillColorRGB(0.1, 0.1, 0.1)
            
            text = q["question"]
            if is_answer:
                display_text = f"{text} {q['answer']}"
            else:
                display_text = f"{text} ____"
                
            c.drawString(x + 18, y, display_text)
            
        # 5. Footer
        footer_y = 50
        c.setLineWidth(1)
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.line(margin, footer_y, width - margin, footer_y)
        
        # Left tag: Black background
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.roundRect(margin, footer_y - 25, 140, 20, 4, stroke=0, fill=1)
        
        c.setFont(self.font_name, 8)
        c.setFillColorRGB(1, 1, 1)
        c.drawCentredString(margin + 70, footer_y - 18, "MATHGENIUS SYSTEM PRO")
        
        # Middle: Page number
        c.setFillColorRGB(0.1, 0.1, 0.1)
        page_text = f"PAGE {page_num} / {total_pages}"
        c.drawCentredString(width / 2, footer_y - 18, page_text)
        
        # Right tag: Border
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.roundRect(width - margin - 100, footer_y - 25, 100, 20, 4, stroke=1, fill=0)
        c.drawCentredString(width - margin - 50, footer_y - 18, grade_tag)
