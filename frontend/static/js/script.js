$(document).ready(function() {
    // Function to handle changes in input fields
    $('#num_coins, #lineup_size').change(function() {
        $('#max_repeating').attr('max', $('#lineup_size').val());

        let numCoins = $('#num_coins').val();
        let coinInputsHtml = '';
        for(let i = 1; i <= numCoins; i++) {
            coinInputsHtml += `
                <div class="row mb-2">
                    <div class="col">
                        <label>Coin ${i} Head Probability</label>
                        <input type="number" class="form-control coin-head-probability" id="probability_${i}" min="0" max="100" step="0.01" value="0" required>
                    </div>
                    <div class="col">
                        <label>Coin ${i} Tail Probability</label>
                        <input type="number" class="form-control coin-tail-probability" id="tail_probability_${i}" min="0" max="100" step="0.01" value="0" required disabled>
                    </div>
                    <div class="col">
                        <label>Coin ${i} Head Points</label>
                        <input type="number" class="form-control" id="head_points_${i}" min="0" max="200" value="0" required>
                    </div>
                    <div class="col">
                        <label>Coin ${i} Tail Points</label>
                        <input type="number" class="form-control" id="tail_points_${i}" min="0" max="200" value="0" required>
                    </div>
                    <div class="col">
                        <label>Coin ${i} Min Appearance</label>
                        <input type="number" class="form-control min-appearance" id="min_appearance_${i}" min="0" value="0" required>
                    </div>
                    <div class="col">
                        <label>Coin ${i} Max Appearance</label>
                        <input type="number" class="form-control max-appearance" id="max_appearance_${i}" min="0" value="0" required>
                    </div>
                </div>
            `;
        }
        $('#coinInputs').html(coinInputsHtml);

        $('.min-appearance, .max-appearance').attr('max', $('#lineup_size').val());

        $('.coin-head-probability').change(function() {
            const headProb = $(this).val();
            const tailProb = (100 - headProb).toFixed(2);
            $(this).closest('.row').find('.coin-tail-probability').val(tailProb);
        });
    });

    // Function to handle submit button click
    $('#submit').click(function(event) {
        event.preventDefault(); // Prevent default form submission

        console.log('Submit button clicked'); // Debugging statement

        const numCoins = $('#num_coins').val();
        const lineupSize = $('#lineup_size').val();
        const requiredLineups = $('#required_lineups').val();
        const maxRepeating = $('#max_repeating').val();
        const optimizerType = $('#optimizer_type').val();
        
        let probabilities = [];
        let headPoints = [];
        let tailPoints = [];
        let minAppearances = {};
        let maxAppearances = {};

        for(let i = 1; i <= numCoins; i++) {
            probabilities.push(parseFloat($(`#probability_${i}`).val()) / 100); // Convert percentage to a decimal for the backend
            headPoints.push(parseFloat($(`#head_points_${i}`).val()));
            tailPoints.push(parseFloat($(`#tail_points_${i}`).val()));
            minAppearances[i] = parseInt($(`#min_appearance_${i}`).val());
            maxAppearances[i] = parseInt($(`#max_appearance_${i}`).val());
        }

        const data = {
            num_coins: parseInt(numCoins),
            lineup_size: parseInt(lineupSize),
            probabilities: probabilities,
            head_points: headPoints,
            tail_points: tailPoints,
            max_repeating: parseInt(maxRepeating),
            required_lineups: parseInt(requiredLineups),
            min_appearances: minAppearances,
            max_appearances: maxAppearances
        };

        // Sending AJAX request
        $.ajax({
            type: 'POST',
            url: `/optimize/${optimizerType}`,
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response); // Log response for debugging
                // Update the UI with the result
                $('#resultsContent').html(JSON.stringify(response));
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText); // Log detailed error message
                $('#errorMessage').html('An error occurred. Please try again.').show(); // Display error message
                // Add code to handle the error here, like displaying an error message
            }
        });
    });
});
