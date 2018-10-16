## Mailgun logs

The component fetches logs from Mailgun and returns status of email sent.

### Inputs
* **username** - Mailgun username. If API key is used, fill in `api`.
* **Token** - password or API key for Mailgun.
* **Mailing list name** - the name of the table, used as an input, which contains e-mail addresses, names and other related attributes. Full file name needs to be specified, including the .csv extension.
* **Domain URL** - URL of the domain used. See Mailgun API help for more information.
* **Subject** - subject of emails, for which the logs are to be fetched. If not specified, logs for all emails with given email address will be fetched.

### Outputs
Application returns table `logs.csv`, which is an input table mailing list, with 2 extra columns appended:
* **event** - determines, whether an email
    * **accepted** - email was accepted by Mailgun and will be delivered by it
    * **delivered** - email was delivered
    * **failed** - email was not delivered
    * see Mailgun Events API documentation for more information on various other events.
* **date** - date when the event happened.
