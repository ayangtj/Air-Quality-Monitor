import yagmail

sender_email = 'aquser41@gmail.com'
receiver_email = 'aquser41@gmail.com'

subject = 'Air Quality Alert'

sender_password = input(f'Plase enter the password for {sender_email}:\n')

yag = yagmail.SMTP(user=sender_email, password=sender_password)

contents = [
    'At 10:20:00 today, your air quality was unhealthy'
    'air reading: 150.98'
]

yag.send(to=receiver_email, subject=subject, contents=contents)