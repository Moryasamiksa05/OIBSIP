import speech_recognition as sr
import datetime
import wikipedia
import os
import smtplib
import distutils
from email.message import EmailMessage

# Initialize the speech recognition engine
r = sr.Recognizer()

# Function to send an email
def send_email(subject, message, from_addr, to_addr, password):
    msg = EmailMessage()
    msg.set_content(message)
    msg['subject'] = subject
    msg['from'] = from_addr
    msg['to'] = to_addr

    server = smtplib.SMTP_SSL('mauryasamiksha188@gmail.com', 465)
    server.login(from_addr, password)
    server.send_message(msg)
    server.quit()

# Function to get the current date and time
def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Function to search Wikipedia
def search_wikipedia(query):
    results = wikipedia.search(query)
    if results:
        return wikipedia.summary(results[0], sentences=2)
    else:
        return "No results found"

# Main function
def main():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='en-in')
        print("You said: " + command)

        if "hello" in command.lower():
            print("Hello! How can I assist you today?")
        elif "time" in command.lower():
            print("Current time: " + get_current_datetime())
        elif "search" in command.lower():
            query = command.replace("search", "")
            print("Results: " + search_wikipedia(query))
        elif "email" in command.lower():
            subject = input("Enter the subject: ")
            message = input("Enter the message: ")
            from_addr = input("Enter the from address: ")
            to_addr = input("Enter the to address: ")
            password = input("Enter the password: ")
            send_email(subject, message, from_addr, to_addr, password)
            print("Email sent successfully!")
        else:
            print("I didn't understand that. Please try again.")

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
    except sr.RequestError as e:
        print("Error; {0}".format(e))

if __name__ == "__main__":
    main()