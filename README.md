![logo](assets/logo.png)

# About

Split subscriptions and collect money automatically and instantly over UPI seamlessly.

### Screenshots


### Video


## The problem it solves

Sharing subscriptions like Netflix friends is not seamless. Collect payments
online and reconciling them manually using Apps still requires us 
to manually confirm payments, and APIs/SDKs by PSPs are expensive. 

## The hack

We piggyback on paisa values in the UPI request amount as the transaction ID, 
and reconcile the payment seamlessly and automatically into the subscriptions.

## The app

To demonstrate the hack for this hackathon, we decided to concentrate our efforts 
to Splitting Recurring Payments such as those for 
Netflix/Amazon Prime/Hotstar/Spotify etc. Although, our 
hack can be extended to any kind of collect requests.

A user can create groups on our app and enter his friends contact details
and instantly get reconciliations from our app when he receives payments.

### Our hack allows you to consolidate your UPI requests for free! 
- Daily UPI requests are limited by PSP apps like Google Pay. 
  - You can request upto 5 times on Google Pay a day
  - New users can't be requested more than once a day
- Payment API's are expensive
  - Costs (2% per transaction) are added onto the consumers
- You need to check your Bank transaction details and reconcile manually without a PSP
- Apps like Paisa Vasool are impossible on top of UPI as of today

### Our hack allows payers to pay with any VPA.
- No need to ask your user to be on a specific UPI app
- No need for payee to pay from his own account (parents/friends can pay on behalf)

### Instant reconcilation
- We process the transacation as soon as we get the bank SMS
- Users don't need to check their bank details

## Challenges we ran into

The biggest challenge was to figure out a way to solve these issues:
- How to identify a transaction
- How to not need the payers VPA

We figured out that:
- The identifier can be embedded in the paisa value
- We can read SMS to get the amount and parse the transaction ID.

### Detailed technical flow
- User installs our app and gives read permission for SMS to our app.
  - Our app is open source and only sends SMS with UPI VPAs to our server
- They create a collect request in the UI with the amount and users, and create a group for recurring weekly/monthly transactions.
  - User adds his clients/friends to the group using mobile number and/or email
    - These are saved for the future
- The collect request is then processed by the server
  - UPI link (which can be embedded in SMS/Whatsapp/Telegram) is created using [https://upi.link/](https://upi.link/) API - It is sent to all the clients/friends with appropriate amount that has been hacked to include the transaction identifier in the amount paisa value. 
- The app waits for SMS from the bank of the User, which includes the amount (plus paisa value identifier) inside it.
  - On receiving the SMS, we change the state of the pending transaction to complete.
- The user can check the state and see all his transactions from our app.

## Future
- The Sahamati framework in the future will allow users to share their bank transaction ledger details with apps directly in a standardized format via Aggregators.
- UPI roadmap has split requests planned for the future.