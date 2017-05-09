# jlynn_arts_website

## Overview:

This is the begining of a website for my wife who is an artist, from this site people can view and buy her art online. The payment is
processed securely thrugh Stripe and shipping is calculated via Easypost.

## Installation:

A requirements.txt is included in the file structure and needs to be installed to get all dependencies and a postgres database is used 
for storing the data. There are keys that are currently set as OS Variables that I can send upon request. Also as a side note the API keys
for Stripe and Easypost are trial versions so that no real purchases are made.

## Database:

As mentioned this program uses Postgres and the database is set up to store "Art" which allows you to add diffrent things like title,dimensions,
description, and images. Also the database stores your customers shipping address so to be retrieved if needed, no billing information is stored
locally.

## User Expierence:

The site is pretty straight foward, the paintings currently are not removed from the database upon "purchase". This is so that the website can
be tested and run without needing to add more "art". When purchasing their are a number of card numbers that Stripe has set aside for testing
purposes, the easiest is for Visa: 4242 4242 4242 4242 with any exp date and cvs number you want. If you want to add art you can do so via the admin
page and create a superuser in your terminal. The last thing is the about tab is none functioning as is the contact form at the bottom of the 
main page, I didn't have time to get these running.

# Examples

## Main Page

<img width="1127" alt="screen shot 2017-05-09 at 5 25 05 pm" src="https://cloud.githubusercontent.com/assets/10622937/25875400/d366a738-34dc-11e7-8f23-d73315c63e50.png">

## Shop Page

<img width="1016" alt="screen shot 2017-05-09 at 5 31 42 pm" src="https://cloud.githubusercontent.com/assets/10622937/25875513/8cc55102-34dd-11e7-9aac-e9095624a462.png">

## Shipping Information Page

<img width="1011" alt="screen shot 2017-05-09 at 5 35 39 pm" src="https://cloud.githubusercontent.com/assets/10622937/25875621/19f18e10-34de-11e7-8fcf-d94e6422d8ce.png">

## Order Summary Page







