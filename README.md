# SafeCallerWebServices
This project mimics the behaviour of a famous application Truecaller. The project exposes several endpoints for the user to interact with it. 
It uses JWT authentication system and let's a user login, logout, Search for contacts, Mark a phone number spam. 

## Searching
All of the searches done by the users eventually hit a global database which shows the search results and their corrersponding details such as 
the spam likelihood (How likely this phone number is to be a spam). 
**ElasticSearch** is used for efficient searching. A user can search search either by number and name. Writing just a few initials of a name will 
give all of the related phone number matches the name.

