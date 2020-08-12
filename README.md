# Tyrceo-Hiring-Test
This is my approach to solve the problem mentioned [here](https://github.com/Tyrceo/Hiring-Test-Instructions).

# To run the test
I have put an requirements.txt, and with that I've created a Pipfile and Pipfile.lock files so you can run the virtual environment. The requirements.txt file is just in case something hapens and you need to create the Pipfile files yourselves.

After you have run the python script, you will have the points.geojson file created. In order to make the project work, you need to copy and paste the file into the "visualization" folder, and create a local server with the command "python -m http.server". After that, you can go to the localhost on your machine and you will see the map with the result of the test.

# When you see the test
I've separated the data circles with colors, as you mentioned it was a bonus. The meaning of the colors are explained in the code as well, but I'll explain it here too.
- Blue: locations where more than 50% of the population that took the survey said Squirtle.
- Turquoise green: locations where more than 50% of the population that took the survey said Bulbasaur.
- Orange: locations where more than 50% of the population that took the survey said Charmander.
- Black: locations where more than 50% of the population that took the survey said a pokemon, but they wrote typos. In this case, the pokemon will be known by proximity. That means, that if we see a black cicrcle inside the "bulbasaur" cluster, we know it's also a Bulbasaur point. This could have been removed by changing the value of the typos when cleaning the dataset, but as you said, we want to keep that values.


