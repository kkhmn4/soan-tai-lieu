"""Dữ liệu mẫu để chạy thử toàn bộ pipeline mà KHÔNG cần GEMINI_API_KEY hay
mạng — đường test offline thật sự đầu tiên của dự án (bản cũ có `dry_run.py`
nhưng đã hỏng cú pháp/thiếu hàm từ lâu, không chạy được).

Không nhằm mục đích sư phạm chính xác — chỉ cần đủ hợp lệ (đúng số lượng
câu hỏi 18/4/6, đủ trường bắt buộc) để đi hết được generate -> markdown ->
docx -> QA mà không tốn phí gọi Gemini.
"""
from __future__ import annotations

from gems.config.loader import LessonSpec
from gems.models.architect import (
    GEMSArchitect,
    KnowledgeUnit,
    LessonMatrix,
    MisconceptionItem,
    PedagogicalAnalysis,
    TaskItem,
)
from gems.models.homework import HomeworkContent, Part1Question, Part2Question, Part3Question
from gems.models.lesson_plan import (
    ActivityPlan,
    ActivitySteps,
    AdjustmentSection,
    DigitalCompetencyTarget,
    LessonPlanContent,
    MaterialsSection,
    ObjectivesSection,
)
from gems.models.worksheet import (
    ApplicationReading,
    CoreTheorySection,
    KnowledgeFormationUnit,
    LessonWorksheet,
    PracticeItem,
    TaskContent,
)


def build_architect(lesson: LessonSpec) -> GEMSArchitect:
    units = []
    for i in range(1, lesson.num_knowledge_units + 1):
        units.append(
            KnowledgeUnit(
                unit_id=f"ĐVKT {i}",
                unit_name=f"Đơn vị kiến thức {i} của {lesson.name}",
                concepts=[f"Khái niệm {i}.1", f"Khái niệm {i}.2"],
                tasks=[
                    TaskItem(task_id=f"NV{i}.1", task_type="Matching Matrix", task_name=f"Nhiệm vụ ghép nối {i}",
                              description="Mô tả nhiệm vụ mẫu.", context_real="Bối cảnh thực tế mẫu."),
                    TaskItem(task_id=f"NV{i}.2", task_type="Bug Buster", task_name=f"Nhiệm vụ tìm lỗi {i}",
                              description="Mô tả nhiệm vụ mẫu thứ hai.", context_real="Bối cảnh thực tế mẫu khác."),
                ],
            )
        )
    return GEMSArchitect(
        analysis=PedagogicalAnalysis(
            key_concepts=["Khái niệm cốt lõi 1", "Khái niệm cốt lõi 2"],
            misconceptions=[
                MisconceptionItem(misconception="Quan niệm sai mẫu", correct_concept="Bản chất đúng mẫu",
                                    explanation="Giải thích sư phạm mẫu."),
            ],
            teaching_methods=["Dạy học khám phá", "Dạy học hợp tác nhóm"],
        ),
        matrix=LessonMatrix(lesson_name=lesson.name, units=units),
    )


def build_worksheet(architect: GEMSArchitect) -> LessonWorksheet:
    knowledge_formation = [
        KnowledgeFormationUnit(
            unit_id=unit.unit_id,
            unit_name=unit.unit_name,
            tasks=[
                TaskContent(task_id=t.task_id, task_type=t.task_type, task_name=t.task_name,
                             content=f"Nội dung khám phá mẫu cho {t.task_name}.",
                             instructions="Nhóm 4 học sinh, 8 phút. Quan sát hình ảnh và đọc SGK mục liên quan.")
                for t in unit.tasks
            ],
            core_theory=CoreTheorySection(
                summary_cloze="Định nghĩa (1) là đại lượng đặc trưng cho (2) của vật.",
                key_words=["đại lượng mẫu", "tính chất mẫu"],
            ),
        )
        for unit in architect.matrix.units
    ]
    practice_items = [
        PracticeItem(unit_id=unit.unit_id, unit_name=unit.unit_name,
                      scenario="Tình huống vận dụng thực tế mẫu.",
                      instructions="Hoạt động cá nhân, 5 phút, dựa vào công thức đã học và SGK.")
        for unit in architect.matrix.units
    ]
    application_readings = [
        ApplicationReading(unit_id=unit.unit_id, unit_name=unit.unit_name,
                             reading_content="Đoạn đọc hiểu mở rộng STEM mẫu.")
        for unit in architect.matrix.units
    ]
    return LessonWorksheet(
        lesson_name=architect.matrix.lesson_name,
        knowledge_formation=knowledge_formation,
        practice_items=practice_items,
        application_readings=application_readings,
    )


def build_homework(architect: GEMSArchitect) -> HomeworkContent:
    part1 = [
        Part1Question(question_text=f"Câu hỏi trắc nghiệm mẫu số {i}?", option_a="Phương án A",
                        option_b="Phương án B", option_c="Phương án C", option_d="Phương án D",
                        correct_option="A", explanation="Giải thích mẫu.")
        for i in range(1, 19)
    ]
    part2 = [
        Part2Question(question_text=f"Nhận định Đúng/Sai mẫu số {i}.", statement_a="Mệnh đề a mẫu",
                        statement_b="Mệnh đề b mẫu", statement_c="Mệnh đề c mẫu", statement_d="Mệnh đề d mẫu",
                        correct_a=True, correct_b=False, correct_c=True, correct_d=False,
                        explanation="Giải thích mẫu cho 4 mệnh đề.")
        for i in range(1, 5)
    ]
    part3 = [
        Part3Question(question_text=f"Câu hỏi trả lời ngắn mẫu số {i}?", correct_answer="100", unit="J",
                        explanation="Lời giải chi tiết mẫu.")
        for i in range(1, 7)
    ]
    return HomeworkContent(lesson_name=architect.matrix.lesson_name,
                             part1_questions=part1, part2_questions=part2, part3_questions=part3)


def build_lesson_plan(architect: GEMSArchitect) -> LessonPlanContent:
    activities = [
        ActivityPlan(
            activity_id=f"HD{i}", activity_name=f"Hoạt động {i}: {unit.unit_name}",
            objectives="Mục tiêu hoạt động mẫu.", content="Nội dung hoạt động mẫu.",
            product="Sản phẩm học tập mẫu.",
            active_learning_techniques=["Chia sẻ nhóm đôi"],
            digital_competency_codes=["1.2"],
            steps=ActivitySteps(
                step1_transfer="Giáo viên giao nhiệm vụ mẫu.",
                step2_execution="Học sinh thực hiện nhiệm vụ mẫu.",
                step3_report="Học sinh báo cáo kết quả mẫu.",
                step4_conclusion="Giáo viên kết luận, chuẩn hóa kiến thức mẫu.",
            ),
        )
        for i, unit in enumerate(architect.matrix.units, 1)
    ]
    return LessonPlanContent(
        lesson_name=architect.matrix.lesson_name, duration="2 tiết",
        objectives=ObjectivesSection(physics_competency=["Năng lực vật lý mẫu"],
                                       general_competency=["Năng lực tự học mẫu"],
                                       digital_competency=[DigitalCompetencyTarget(
                                           code="1.2",
                                           competency="Đánh giá dữ liệu, thông tin và nội dung số",
                                           learning_outcome="Đánh giá độ tin cậy của dữ liệu số và hướng dẫn bạn kiểm tra nguồn.",
                                           evidence="Phiếu so sánh dữ liệu có liên kết và nhận xét nguồn.",
                                       )],
                                       qualities=["Chăm chỉ", "Trách nhiệm"]),
        materials=MaterialsSection(teacher_materials=["Máy chiếu", "Phiếu học tập"],
                                     student_materials=["SGK", "Vở ghi"]),
        activities=activities,
        adjustments=AdjustmentSection(advantages="", limitations="", solutions=""),
    )
