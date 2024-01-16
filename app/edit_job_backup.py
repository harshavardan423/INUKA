 # # Update existing questions and default answers
            # updated_existing_questions = request.form.getlist('existing_questions[]')
            # updated_existing_default_answers = request.form.getlist('existing_default_answers[]')

            # for question in questions[:]:  # Iterate over a copy of the list
            #     if question.text in updated_existing_questions:
            #         index = updated_existing_questions.index(question.text)
            #         question.default_answer = updated_existing_default_answers[index]
            #     else:
            #         db.session.delete(question)

            # # Add new questions and default answers
            # new_questions = request.form.getlist('questions[]')
            # new_default_answers = request.form.getlist('new_default_answers_1[]')
            # for question_text, default_answer_text in zip(new_questions, new_default_answers):
            #     # Generate a unique question_id for each new question
            #     question_id = f"{int(time.time())}{random.randint(1000, 9999)}"
                
            #     new_question = Question(
            #         id=question_id,
            #         text=question_text,
            #         default_answer=default_answer_text,
            #         job_id=job.id
            #     )
            #     db.session.add(new_question)