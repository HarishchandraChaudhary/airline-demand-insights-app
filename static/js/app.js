// airline_demand_app/static/js/app.js
document.addEventListener('DOMContentLoaded', () => {
    const popularRoutesTable = document.getElementById('popular-routes-table');
    const highDemandPeriodsTable = document.getElementById('high-demand-periods-table');
    const priceTrendsChartCanvas = document.getElementById('priceTrendsChart');
    const aiInsightsOutput = document.getElementById('ai-insights-output');
    const generateInsightsBtn = document.getElementById('generate-insights-btn');
    const insightsLoading = document.getElementById('insights-loading');

    let chartInstance = null; // To store the Chart.js instance

    // Function to fetch and display data
    async function fetchData() {
        try {
            const response = await fetch('/api/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Fetched Data:", data);

            // Populate Popular Routes Table
            popularRoutesTable.innerHTML = ''; // Clear previous data
            data.popular_routes.forEach(route => {
                const row = `
                    <tr class="hover:bg-gray-100">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${route.route}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${route.demand}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$${route.avg_price.toFixed(2)}</td>
                    </tr>
                `;
                popularRoutesTable.insertAdjacentHTML('beforeend', row);
            });

            // Populate High Demand Periods Table
            highDemandPeriodsTable.innerHTML = ''; // Clear previous data
            data.high_demand_periods.forEach(period => {
                const row = `
                    <tr class="hover:bg-gray-100">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${period.period}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${period.location}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${period.demand_factor.toFixed(2)}x</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${period.notes}</td>
                    </tr>
                `;
                highDemandPeriodsTable.insertAdjacentHTML('beforeend', row);
            });

            // Prepare data for Price Trends Chart
            const uniqueDates = [...new Set(data.price_trends.map(item => item.date))].sort();
            const datasets = [];
            const routes = [...new Set(data.price_trends.map(item => item.route))];

            routes.forEach(route => {
                const routePrices = uniqueDates.map(date => {
                    const trend = data.price_trends.find(item => item.date === date && item.route === route);
                    return trend ? trend.price : null; // Use null for missing data points
                });

                datasets.push({
                    label: route,
                    data: routePrices,
                    borderColor: getRandomColor(),
                    tension: 0.1,
                    fill: false,
                    pointRadius: 3,
                    pointHoverRadius: 5
                });
            });

            // Destroy existing chart if it exists
            if (chartInstance) {
                chartInstance.destroy();
            }

            // Render Price Trends Chart
            chartInstance = new Chart(priceTrendsChartCanvas, {
                type: 'line',
                data: {
                    labels: uniqueDates,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Flight Price Trends for Popular Routes'
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            },
                            type: 'time', // Use time scale for dates
                            time: {
                                unit: 'day',
                                tooltipFormat: 'MMM D, YYYY',
                                displayFormats: {
                                    day: 'MMM D'
                                }
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Price ($)'
                            },
                            beginAtZero: false
                        }
                    }
                }
            });

            // Store the fetched data globally for insights generation
            window.appData = data;

        } catch (error) {
            console.error('Error fetching data:', error);
            alert('Failed to load data. Please check the server and try again.');
        }
    }

    // Function to generate random color for chart lines
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Event listener for Generate Insights button
    generateInsightsBtn.addEventListener('click', async () => {
        if (!window.appData) {
            aiInsightsOutput.innerHTML = '<p class="text-red-500">No data available to generate insights. Please refresh the page.</p>';
            return;
        }

        insightsLoading.classList.remove('hidden'); // Show spinner
        generateInsightsBtn.disabled = true; // Disable button
        aiInsightsOutput.innerHTML = ''; // Clear previous insights

        try {
            const response = await fetch('/api/insights', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(window.appData), // Send the fetched data to backend
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            aiInsightsOutput.innerHTML = result.insights.replace(/\n/g, '<br>'); // Display insights, convert newlines to <br>
            console.log("AI Insights:", result.insights);

        } catch (error) {
            console.error('Error generating insights:', error);
            aiInsightsOutput.innerHTML = `<p class="text-red-500">Failed to generate insights: ${error.message}. Please ensure your Gemini API key is set correctly on the server.</p>`;
        } finally {
            insightsLoading.classList.add('hidden'); // Hide spinner
            generateInsightsBtn.disabled = false; // Re-enable button
        }
    });

    // Initial data fetch on page load
    fetchData();
});
