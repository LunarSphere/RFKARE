
function createMapGrid() {
    const mapGrid = document.getElementById('mapGrid');
    mapGrid.innerHTML = ''; // Clear existing grid

    // Create 10x13 grid
    for (let row = 0; row < 10; row++) {
        for (let col = 0; col < 13; col++) {
            const tile = document.createElement('div');
            tile.className = 'map-tile';
            
            // Set background image
            tile.style.backgroundImage = `url('data/gee_image_row${row}_col${col}.png')`;
            
            // Highlight the specified tile (3rd row, 4th column)
            if (row === 4 && col === 4) {
                tile.classList.add('highlighted');
            }
            
            mapGrid.appendChild(tile);
        }
    }
}

function handleAnalyze() {
    const button = document.getElementById('analyzeBtn');
    const spinner = document.querySelector('.spinner');
    const results = document.getElementById('results');
    const factorsList = document.getElementById('factorsList');

    // Disable button and show spinner
    button.disabled = true;
    spinner.style.display = 'block';
    button.querySelector('span').textContent = 'Analyzing...';

    // Simulate API call
    setTimeout(() => {
        // Update results
        document.getElementById('locationResult').textContent = 'East Tulsa District';
        document.getElementById('scoreResult').textContent = '87.5/100';
        
        // Update factors list
        const factors = [
            'High accessibility via I-44',
            'Large undeveloped land area',
            'Growing population density',
            'Favorable zoning laws'
        ];
        
        factorsList.innerHTML = factors.map(factor => `<li>${factor}</li>`).join('');

        // Create map grid
        createMapGrid();

        // Show results
        results.style.display = 'block';

        // Reset button
        button.disabled = false;
        spinner.style.display = 'none';
        button.querySelector('span').textContent = 'Analyze';
    }, 2000);
}