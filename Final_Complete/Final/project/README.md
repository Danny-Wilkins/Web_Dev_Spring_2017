<h1>Bytes</h1>

<h2>Inspiration</h2>
"I never actually know if I'm getting a good deal anymore..."

While enjoying some free pizza, we began to discuss the struggles of being broke students in New York City.

"The food is good, but it's also really expensive."

"How much is too much for good food?"

"Bad food is cheap food and that's all that matters."

There are countless websites to check out food in your area, but they're all missing a critical element: <h4>a comparison with other local restaurants to determine if the food is a good value.</h4>

<h2>What it does</h2>
Bytes compares the ratings and cost of a restaurant to other restaurants around you to help you get the best food for your money. Bytes, taking into account cost/rating ratio of local restaurants, calculates a score and assigns a letter grade determining the quality of the deal. The higher the score, the better the deal!

<h2>How it works</h2>
Back-end dependencies: Requests, BeautifulSoup, NumPy, SciPy, GeoPy

Bytes is written in Python, using the Yelp API. GeoPy was used to get location; its ability to easily acquire latitude and longitude coordinates worked well with Yelp's API calls. From there, the API generates a list of restaurants within the specified distance, feeds their cost and rating into SciPy, calculates a linear regression based on this data. From there, the restaurants are rated based on their actual position either above or below the regression line; above meaning a better than average deal, and below meaning worse than average. NumPy is used to simplify some of the mathematical work behind this. The data is returned with the name of the restaurant, the score, and the letter grade. 

The front end was written using HTML and CSS to provide a web interface. JavaScript and Flask were used to integrate front end (mostly user input) with the back end. Bootstrap was used for a simple, sleek interface and compatibility with mobile devices.

<h2>Challenges we ran into</h2>
The greatest challenge by far has been using Flask to tie the front and back ends together, with the largest obstacle being getting user input into the back end, and then taking the results from the back end and outputting it to the front end. In the end, I used Python to return a dynamically generated HTML page containing all of the results. I know you have things like innerHtml to change the page content, but because the true issue lied in returning info from Python to JS, I opted to create the page in Python instead.

AWS is the absolute bane of my existence. It literally just will not work. A few times I got it to display Bytes, but upon refreshing the page or making any changes to the most meaningless code, or even adding a COMMENT or NOTHING it broke everything and I couldn't get the page up again. I've given up and, as such, Bytes is a localhost:5000 only application.

<h2>Accomplishments I'm proud of</h2>
The accomplishment I'm most proud of is my solution to the back end/front end interaction issue. I had no idea how to do the most basic thing transferring data between Python and JS (honestly I'd rather never mix languages again). I tried rewriting it in JavaScript, but I found the geolocation stuff a bit too hard to use (Google Maps API and all, I'd rather not right now). After finally figuring out how to get Javascript to call on a Python function, I was able to do the calculations on the back end and, by copy and appending to index.html, return results to the front end with the information plugged in.

At present, Bytes is extensible (to hotels, attractions, and other things under the Yelp API), and it is good at error handling. Being able to learn new APIs quickly is a skill I gladly continue to improve upon. I am also proud of the idea used for rating the restaurants: it makes sense, is efficient, and demonstrates an efficiency in thinking outside of coding.

<h2>What I learned</h2>
I learned a bit more JavaScript, even if it didn't make it into the final project. A bit of JQuery. I learned a bit about how Flask works to tie the front and back ends together, and just problem solving in general to come up with a unique (albeit ghetto) solution for a problem I was having.

<h2>What's next for Bytes</h2>
Bytes, in its current state, works very efficiently for finding local deals on food. However, this behavior could easily be extended to other areas such as hotels, attractions, and other things. Adding other features such as displaying menus, maps, having user accounts to allow users to save favorites and view eating history, share recommendations with friends, etc. Bytes could also (in a non-evil way) collect data about its users, using this information to improve user experience and perhaps even local food options. Most importantly, cleaning up the integration between the front and back ends using Flask would be great.