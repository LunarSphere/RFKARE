
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

        // Show results
        results.style.display = 'block';

        // Reset button
        button.disabled = false;
        spinner.style.display = 'none';
        button.querySelector('span').textContent = 'Analyze';
    }, 2000);
}