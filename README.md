### OVER/UNDER DFS Optimizer

#### Overview
OVER/UNDER DFS Optimizer is a web application designed to optimize coin lineups for Daily Fantasy Sports (DFS) competitions, including popular platforms like Thrive Fantasy DFS and Pick6 on Draftkings. These types of games represent the next iteration of DFS and sports gambling games, offering innovative approaches to fantasy sports.

The optimizer provides three different strategies based on user-defined criteria: Value Optimizer, Points Optimizer, and Probability Optimizer. Each optimizer utilizes linear programming techniques to generate optimized coin lineups while adhering to specified constraints.

#### Features
1. **Value Optimizer:**
   - Maximizes the expected value (EV) of the coin lineups.
   - Allows users to assign probabilities and points to each coin (heads/tails).
   - Considers constraints on minimum and maximum appearances of each coin type.

2. **Points Optimizer:**
   - Maximizes the total points of the coin lineups.
   - Enables users to assign points for each coin (heads/tails).
   - Supports constraints on minimum and maximum appearances of each coin type.

3. **Probability Optimizer:**
   - Maximizes the total probability of the coin lineups.
   - Requires users to input probabilities for each coin (heads/tails).
   - Incorporates constraints on minimum and maximum appearances of each coin type.

#### Usage
1. Input the number of coins, lineup size, required lineups, and maximum repeating patterns.
2. Choose the optimizer type: Value Optimizer, Points Optimizer, or Probability Optimizer.
3. Specify the details for each coin:
   - Head Probability (for Probability Optimizer)
   - Tail Probability (for Probability Optimizer)
   - Head Points (for Value Optimizer and Points Optimizer)
   - Tail Points (for Value Optimizer and Points Optimizer)
   - Minimum Appearance
   - Maximum Appearance
4. Click the "Submit" button to generate optimized lineups based on the selected optimizer type.
5. View the results, including the generated lineups and a summary of coin appearances.

#### Technologies Used
- Python (Flask) for backend development
- PuLP library for linear programming optimization
- JavaScript (jQuery) for frontend interaction
- HTML/CSS for frontend layout and design
- Bootstrap for responsive web design

#### Running the Application
1. Clone the repository from GitHub.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Flask application using `python app.py`.
4. Access the application in your web browser at `http://localhost:5000/`.
