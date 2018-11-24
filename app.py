from flask import Flask, request, redirect, url_for, render_template, jsonify
import jinja2
import csv
import random
from random import shuffle
from twilio.rest import Client
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

load_dotenv(find_dotenv())

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('ACCOUNT_TOKEN')
account_number = os.getenv('ACCOUNT_NUMBER')

client = Client(account_sid, auth_token)

tarot_tsv_file = open("tarot-deck.tsv", "r")
# Open tsv Tarot deck file
TAROT_DECK_DICT = {}

tarot_reading = []

with open("tarot-deck.tsv") as tsv:
	for line in csv.reader(tsv, dialect="excel-tab"):
		TAROT_DECK_DICT[line[0]] = line[1:]

@app.route("/")
def home():
	introduction_text = "As you walk along a murky path, you encounter a dark shape. As you draw closer to it, you realize it's a hooded stranger. A hand beckons from within the depths of the stranger's robes. With apprehension, you peer closer, and see that the stranger is shuffling a deck of cards."
	return render_template("index.html", text=introduction_text)

@app.route("/cut_deck")
def cut_deck():
	text = "The robed figure asks you to cut the deck, and you do so with great trepidition. With a voice like gravel, the figure tells you to select a deck."
	cut_deck_image = "static/53c0cce811d9a_thumb900.jpg"
	return render_template("cards.html", text=text, cut_deck_image=cut_deck_image)

@app.route("/left_deck")
def deck_selection():
	text = "You make your choice! Five cards are dealt from the deck and laid out before you. Your job is to choose the final three cards to reveal your fate."
	five_card_image = "static/53c0cce811d9a_thumb900.jpg"
	return render_template("five_cards.html", text=text, five_card_image=five_card_image)

@app.route("/final_reading", methods=['GET', 'POST'])
def final_five():
	final_cards = random.sample(xrange(78),3)
	for card in final_cards:
		tarot_reading.append(TAROT_DECK_DICT[str(card)])
	text = "Here are your cards ..."
	five_card_image = "static/53c0cce811d9a_thumb900.jpg"
	return render_template("final_cards.html", text=text, tarot_reading=tarot_reading)

@app.route("/text", methods=['GET', 'POST'])
def text_reading():
	number = request.form.getlist('phonenumber')
	final_reading = []
	for card in tarot_reading:
		final_reading.append(card[1])

	message_body = '; '.join(final_reading)

	client.messages.create(from_=account_number, body=message_body, to=number[0])
	
	return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)