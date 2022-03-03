import smtplib

# My email address
# credentials found in https://docs.google.com/document/d/1Ryvv_gmkNGLJL6WzX-El3QS4DicYojW5UsrlYk5KSCo/edit
# else, use your own credentials
gmail_user = ''
gmail_password = ''


def Email(email, first_name, last_name):
    sent_from = gmail_user
    to = email
    subject = 'Queensway Shopping Center: Forgot Password'
    new_password = "P@$$w0rd123"
    body = 'Dear {} {},\n\nYour new password is {}. \n Please Change your Password as soon as you login.'.format(first_name, last_name, new_password)

    email_text = "Subject: {}\n\n{}".format(subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
        return new_password
    except Exception as e:
        # e to print the error of the email
        print(e)
        print('Email unsuccessful')
