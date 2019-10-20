![logo](assets/logo.png)

## The hack

### One line description of our hack on top of UPI

- Piggy back on Paisa values in the UPI request amount as a transaction identifier, and reconcile the payment seamlessly and automatically.

### Detailed technical flow

- User installs our app and gives read permission for SMS to our app.
  - Our app is open source and only sends SMS with UPI VPAs to our server
- They create a collect request in the UI with the amount and users, and create a group for recurring weekly/monthly transactions.
  - User adds his clients/friends to the group using mobile number and/or email
    - These are saved for the future
- The collect request is then processed by the server
  - UPI link (which can be embedded in SMS/Whatsapp/Telegram) is created using https://upi.link/ API - It is sent to all the clients/friends with appropriate amount that has been hacked to include the transaction identifier in the amount paisa value. 
- The app waits for SMS from the bank of the User, which includes the amount (plus paisa value identifier) inside it.
  - On receiving the SMS, we change the state of the pending transaction to complete.
- The user can check the state and see all his transactions from our app.

### Our hack allows you you to onsolidate your UPI requests for free! 

- Daily UPI requests are limited by PSP apps like Google Pay. 
  - You can request upto 5 times on Google Pay a day
  - New users can't be requested more than once a day
- Payment API's are expensive
  - Costs (2% per transaction) are added onto the consumer
- You need to check your Bank transaction details and reconcile manually without a PSP
- Apps like Paisa Vasool are impossible on top of UPI as of today

### Our hack allows payers to pay with any VPA.
- No need to ask your user to be on a specific UPI app
- No need for payee to pay from his own account (parents/friends can pay on behalf)

### Instant reconcilation
- We are able to process the the transacation as soon as it hits the bank via the SMS
- Users don't need to check their bank details

## The app

To demonstrate the hack for this hackathon, we decided to concentrate our efforts to Splitting Recurring Payments such as those for Netflix/Amazon Prime/Hotstar/Spotify etc. Although, our hack can be extended to any kind of collect requests.

### Screenshots

### Flow

## Future

- The Sahamati framework in the future will allow users to share their bank transaction ledger details with apps directly in a standardized format via Aggregators.
- UPI roadmap has split requests planned for the future.