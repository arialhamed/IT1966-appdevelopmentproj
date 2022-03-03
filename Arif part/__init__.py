from Forms import CreateFaqForm
import FAQ
# and the rest

# <------------------------------------------------------->
# <------------------ FAQ (Arif's Code) ------------------>
# <------------------------------------------------------->
# <--- Start of FAQ Display page with form --->
@app.route('/FAQ', methods=['GET', 'POST'])
def faq():
    faq_dict = {}
    create_faq_form = CreateFaqForm(request.form)
    try:
        db = shelve.open('storage.db',
                         'c')  # argument is 'c', so guaranteed that it will create, concerning a warning from another line
        faq_dict = db["FAQ"]
    except KeyError:
        print("Error in retrieving storage.db, recreating storage.db.")

    # Function below used multiple times, only for translation of data
    def displayers(faq_dict_func):
        q_list = []
        u_count = 0
        a_count = 0
        for key in faq_dict_func:
            question = faq_dict_func.get(key)
            q_list.append(question)
            if question.get_answer() == '':
                u_count += 1
            else:
                a_count += 1
        return q_list, u_count, a_count

    if request.method == 'POST' and create_faq_form.validate():
        if create_faq_form.question.data != '' and create_faq_form.answer.data == '':
            faq_details = FAQ.FAQ(create_faq_form.question.data, session['username'])
            faq_dict[faq_details.get_id()] = faq_details
            create_faq_form.question.data = ''

        db['FAQ'] = faq_dict

        faq_dict = db['FAQ']
        try:
            faq = faq_dict[faq_details.get_id()]
            print("\"" + str(faq.get_question()) + "\" question was stored in storage.db successfully with id ==",
                  faq.get_id())
        except KeyError:
            error = "Question failed to upload (KeyError). Log out and sign in again"
            print("KeyError in retrieving latest input, likely it was blank. This error is expected.")
            question_list, unanswered_count, answered_count = displayers(faq_dict)
            return render_template("faq.html", form=create_faq_form, count=len(question_list),
                                   question_list=question_list,
                                   unanswered_count=unanswered_count,
                                   answered_count=answered_count,
                                   error=error)
        except UnboundLocalError:
            error = "Question failed to upload (UnboundLocalError). Log out and sign in again"
            print("UnboundLocalError in retrieving latest input, likely it was blank. This error is expected.")
            question_list, unanswered_count, answered_count = displayers(faq_dict)
            return render_template("faq.html", form=create_faq_form, count=len(question_list),
                                   question_list=question_list,
                                   unanswered_count=unanswered_count,
                                   answered_count=answered_count,
                                   error=error)
        else:
            success = 'Your question has been uploaded! The admins will upload their answer soon within the week!'
            question_list, unanswered_count, answered_count = displayers(faq_dict)
            return render_template("faq.html", form=create_faq_form, count=len(question_list),
                                   question_list=question_list,
                                   unanswered_count=unanswered_count,
                                   answered_count=answered_count,
                                   success=success)
    question_list, unanswered_count, answered_count = displayers(faq_dict)
    db.close()

    return render_template("faq.html", form=create_faq_form, count=len(question_list),
                           question_list=question_list,
                           unanswered_count=unanswered_count,
                           answered_count=answered_count)


# <--- End of FAQ Display page with form --->


# <--- Start of FAQ answering page with form, for admin --->
@app.route('/FAQanswering/<int:id>/', methods=['GET', 'POST'])
def faqanswering(id):
    faq_answer = CreateFaqForm(request.form)
    if request.method == 'POST' and faq_answer.validate():
        faq_dict = {}
        db = shelve.open('storage.db', 'w')
        faq_dict = db['FAQ']

        faq = faq_dict.get(id)
        # print(type(faq))
        # print(faq)
        faq.set_question(faq_answer.question.data)
        faq.set_answer(faq_answer.answer.data)

        db['FAQ'] = faq_dict
        db.close()

        return redirect(url_for('faq'))
    else:
        faq_dict = {}
        db = shelve.open('storage.db', 'r')
        faq_dict = db['FAQ']
        db.close()

        faq = faq_dict.get(id)
        faq_answer.question.data = faq.get_question()
        faq_answer.answer.data = faq.get_answer()
        return render_template('faq_answering.html', form=faq_answer)


# <--- End of FAQ answering page with form, for admin --->


# <--- Start of FAQ deletion page, for admin --->
@app.route("/FAQdelete/<int:id>/", methods=['POST'])
def faqdelete(id):
    faq_dict = {}
    db = shelve.open("storage.db", 'w')
    faq_dict = db["FAQ"]

    faq = faq_dict.pop(id)

    db['FAQ'] = faq_dict
    db.close()

    return redirect(url_for("faq"))


# <--- End of FAQ deletion page, for admin --->

if __name__ == "__main__":
    app.run(debug=True)
