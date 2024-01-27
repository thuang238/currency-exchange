The Breakdown!

Folder: node_modules
Contents: Bootstrap!
Purpose: Bootstrap packages

Folder: static
Contents: background.jpg, script.js, styles.css
Purpose: static elements of website.

Folder: templates
Contents: all html files
Purpose: keep all html files in one place

api.py:
- We have the api as the endpoint where we fetch data for latest conversion rates and then we asve it as a JSON file
- We parse JSON file into a python dictionary so we can match the inputted currency acronym with its conversion rate

app.py:
- We configure Flask application including loading templates and configuring the session.
- We have database configured using exchange.db file.
- We included routing based on the validity of the user's input with the login and register page.
- We leverage GET and POST requests for currency conversion so that we track real time exchange rates, do currency conversion, logs transaction in database, and returns new currency value as JSON.
- We fetch data from API.
- We also have errors in case responses are not expected and have relevant error messages.

exchange.db:
- We have columns including id, user_id, CurrentCurrency, NewCurrency, cash, conversion_rate, and time_stamp which are pretty self-intuitive.
- The user_id table allows us to ensure that transactions are maintained for each specific user and not mix it with other users on the system.
- id is used for identifying each transaction.

helpers.py:
- Shows the decorators used in Flask
- Apology function - Shows messsage to user to provide insights to errors encountered with the default being 400 being maaning request
- login_required decorator - Ensure that users are redirected after they are logged in to the proper routes and are redirected to login page if they are not logged in
- usd function - Formats numerical value as USD with 2 decimal points


LICENSE: Good for projects on Githubs for others to use and distribute. We chose MIT Liscense because its minimal restrictions encourage collaboration, compatibility with other licenses.


Our project, initially focused on currency exchange with multiple tools. We wanted to provide a way for tourists to converting currency, transaction history, and keeping track of money in one's account.


We used CSS/HTML for front-end since we gain some experience in class and wanted to deep dive the langauge. We explored React a bit and spend a couple hours learning its basics through YouTube videos from Code with Mosh and actual docuementation, but ultimately decided on CSS/HTML given that we had some proficiency in that but can leverage React for future projects. We used Flask for back end but also considered JavaScript and Node.js given our experience before and this allowed us to implement a more complex project than if we learned a new language. With Flask, we used Restful APIs and also learned github for version control with add, commmit, and push seaminglessly. Also, this feature allow us to learn about feature branches, merging branches after we were done, and check out (cherry pick) various commits as necessary. This platform made it easier to collaborate and is used in the industry for software engineering. We used an Currency Exchange API too for real-time conversion. Users also have the ability to log in and register so they can save their info for next time with username and password. As for debugging, we learned about common methods such as with the inspect element and through the console and its print messages. We explored various resources and office hours and decided on our technologies given its efficiency and learning curve.

Also, for our exchange page, we added a cool feature. As we have over 160+ currencies, we have a input box where users can search for the currency and the list is dynamically updated based on the user inputs. This is the same for current currency and desired currency. For the amount box, we added additional requirements for the number to be either 0 or a positive number with at most 2 decimal point since this is how currency is. For the exchange button to work, we added a requirement where all 3 input fields have to be completed. Otherwise, you recieve an error mesage.

Our goals of varying difficult for the good, better, and best outcomes were all fulfilled since this was 20 for good, 40 for better, and 60 for best. We included 162 countries for this API. Finding the API was a big challenging since we didn't want to pay for an API and were limited to free APIs. Through our research, we found that the Google API was very popular and also came with great documentation, but that was depreciated in Jan 2023, so we had to leverage other sources.

Workflow
- Users register and then login or they can just skip to login if they have an account
- Shows user dashboard with name and balance in account
- Displays currency exchange
- Show transaction history
- Users can add currency based off the currency noted in exchange navigation bar 

Project Hour Break Down
- Finding API - 3 hours
- Learning about API and connecting API (including JSON schema) - 3 hours
- Debugging - 20 hours (including many office hours and testing)
- Learning GitHub - 4 hours each
- Learning React - 2 hours each
- Design Features and Layout Design - 3 hours
- Developing code - 8 hours
- Adding in error messages (aka edge cases to improve useribility) - 2 hours

While we reached out goals for this project as noted in the proposal, we had indirectly wanted to make the project more big scale in the sense that we had a map that showed nearby ATMs and provided an additional list with ATMs with the lowest fee within a 10 mile radius. This will be an action item for us to develop over winter break. On paper, the project seemed pretty easy, but as this is one of the first times we're worked on a full-stack project, the debugging phase took a lot more time than expected because as we fixed one error, we would get new errors which was like a Dominos effect cycle. But through this, we learned so much and grew since we are now more confident in our abilities to tackle challenges.

