// EdgeFinder Web Application JavaScript

class EdgeFinderApp {
    constructor() {
        this.data = null;
        this.init();
    }

    init() {
        this.loadData();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Auto-refresh every 5 minutes
        setInterval(() => {
            this.loadData();
        }, 5 * 60 * 1000);
    }

    async loadData() {
        try {
            this.showLoading();
            const response = await fetch('/api/latest');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.text();
            this.parseAndDisplayData(data);
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Failed to load data. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    parseAndDisplayData(markdownData) {
        // Parse the markdown data to extract information
        const lines = markdownData.split('\n');
        let currentSection = '';
        let discrepancies = [];
        let mostBet = [];
        let seattlePick = null;
        let summary = {};

        // Extract summary information
        const summaryLine = lines.find(line => line.includes('**Total Games:**'));
        if (summaryLine) {
            const summaryMatch = summaryLine.match(/\*\*Total Games:\*\* (\d+)/);
            if (summaryMatch) {
                summary = {
                    games: parseInt(summaryMatch[1]),
                    markets: parseInt(summaryMatch[1]), // Use games as markets for now
                    books: parseInt(summaryMatch[1])    // Use games as books for now
                };
            }
        }

        // Extract last updated time
        const timeLine = lines.find(line => line.includes('**Generated:**'));
        if (timeLine) {
            const timeMatch = timeLine.match(/\*\*Generated:\*\* (.+)/);
            if (timeMatch) {
                summary.lastUpdated = timeMatch[1];
            }
        }

        // Parse sections
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            
            if (line.startsWith('## 🏠 Seattle Games')) {
                currentSection = 'seattle';
                continue;
            } else if (line.startsWith('## 📊 Robinhood vs Sportsbooks Comparison')) {
                currentSection = 'comparison';
                continue;
            }

            // Parse table rows
            if (line.startsWith('|') && line.includes('|') && !line.includes('---')) {
                const cells = line.split('|').map(cell => cell.trim()).filter(cell => cell);
                if (cells.length >= 12 && cells[0] !== 'Rank') {
                    const gameData = {
                        rank: cells[0],
                        sport: cells[1],
                        game: cells[2],
                        time: cells[3],
                        robinhoodAway: cells[4],
                        sportsbookAway: cells[5],
                        awayPayout: cells[6],
                        robinhoodHome: cells[7],
                        sportsbookHome: cells[8],
                        homePayout: cells[9],
                        volume: cells[10],
                        discrepancy: cells[11]
                    };

                    if (currentSection === 'comparison') {
                        discrepancies.push(gameData);
                        mostBet.push(gameData); // Use same data for both tables
                    }
                }
            }

            // Parse Seattle pick
            if (currentSection === 'seattle' && line.startsWith('**') && line.includes('@')) {
                const gameMatch = line.match(/\*\*(.+?)\*\*/);
                if (gameMatch) {
                    seattlePick = {
                        game: gameMatch[1],
                        details: []
                    };
                }
            }

            if (currentSection === 'seattle' && line.startsWith('- **')) {
                const detailMatch = line.match(/- \*\*(.+?):\*\* (.+)/);
                if (detailMatch && seattlePick) {
                    seattlePick.details.push({
                        label: detailMatch[1],
                        value: detailMatch[2]
                    });
                }
            }
        }

        this.displayData({ summary, discrepancies, mostBet, seattlePick });
    }

    displayData(data) {
        this.updateSummary(data.summary);
        this.updateDiscrepanciesTable(data.discrepancies);
        this.updateMostBetTable(data.mostBet);
        this.updateSeattlePick(data.seattlePick);
    }

    updateSummary(summary) {
        document.getElementById('totalGames').textContent = summary.games || '-';
        document.getElementById('totalMarkets').textContent = summary.markets || '-';
        document.getElementById('totalBooks').textContent = summary.books || '-';
        document.getElementById('lastUpdated').textContent = summary.lastUpdated || '-';
    }

    updateDiscrepanciesTable(discrepancies) {
        const tbody = document.querySelector('#discrepanciesTable tbody');
        tbody.innerHTML = '';

        discrepancies.forEach((game) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="badge bg-primary">${game.rank}</span></td>
                <td><span class="badge sport-badge bg-secondary">${game.sport}</span></td>
                <td><strong>${game.game}</strong></td>
                <td><small>${game.time}</small></td>
                <td><span class="badge bg-info">${game.robinhoodAway}</span></td>
                <td><span class="badge bg-success">${game.sportsbookAway}</span></td>
                <td><span class="badge bg-warning">${game.awayPayout}</span></td>
                <td><span class="badge bg-info">${game.robinhoodHome}</span></td>
                <td><span class="badge bg-danger">${game.sportsbookHome}</span></td>
                <td><span class="badge bg-warning">${game.homePayout}</span></td>
                <td><span class="badge bg-secondary">${game.volume}</span></td>
                <td><span class="discrepancy-${this.getDiscrepancyClass(game.discrepancy)}">${game.discrepancy}</span></td>
            `;
            tbody.appendChild(row);
        });
    }

    updateMostBetTable(mostBet) {
        const tbody = document.querySelector('#mostBetTable tbody');
        tbody.innerHTML = '';

        // Sort by volume (highest first) for most bet table
        const sortedByVolume = [...mostBet].sort((a, b) => {
            const volumeA = parseInt(a.volume.replace(/,/g, ''));
            const volumeB = parseInt(b.volume.replace(/,/g, ''));
            return volumeB - volumeA;
        });

        sortedByVolume.forEach((game, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="badge bg-primary">${index + 1}</span></td>
                <td><span class="badge sport-badge bg-secondary">${game.sport}</span></td>
                <td><strong>${game.game}</strong></td>
                <td><small>${game.time}</small></td>
                <td><span class="badge bg-info">${game.robinhoodAway}</span></td>
                <td><span class="badge bg-success">${game.sportsbookAway}</span></td>
                <td><span class="badge bg-warning">${game.awayPayout}</span></td>
                <td><span class="badge bg-info">${game.robinhoodHome}</span></td>
                <td><span class="badge bg-danger">${game.sportsbookHome}</span></td>
                <td><span class="badge bg-warning">${game.homePayout}</span></td>
                <td><span class="badge bg-secondary">${game.volume}</span></td>
                <td><span class="discrepancy-${this.getDiscrepancyClass(game.discrepancy)}">${game.discrepancy}</span></td>
            `;
            tbody.appendChild(row);
        });
    }

    updateSeattlePick(seattlePick) {
        const container = document.getElementById('seattlePick');
        
        if (!seattlePick) {
            container.innerHTML = '<p class="text-muted">No Seattle team games found in current data.</p>';
            return;
        }

        let html = `
            <div class="seattle-pick">
                <h4><i class="fas fa-home me-2"></i>${seattlePick.game}</h4>
                <div class="row">
        `;

        seattlePick.details.forEach(detail => {
            html += `
                <div class="col-md-6 mb-2">
                    <div class="metric">
                        <span class="metric-label">${detail.label}</span>
                        <span class="metric-value">${detail.value}</span>
                    </div>
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    getDiscrepancyClass(discrepancy) {
        // Remove % sign and convert to decimal
        const value = parseFloat(discrepancy.replace('%', '')) / 100;
        if (value >= 0.1) return 'high';
        if (value >= 0.05) return 'medium';
        return 'low';
    }

    getVolumeClass(volume) {
        const value = parseInt(volume.replace(/,/g, ''));
        if (value >= 2000) return 'high';
        if (value >= 1000) return 'medium';
        return 'low';
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('d-none');
        document.getElementById('mainContent').style.opacity = '0.5';
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('d-none');
        document.getElementById('mainContent').style.opacity = '1';
    }

    showError(message) {
        // Create a toast notification
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-danger border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-exclamation-triangle me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        // Add to page
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        toastContainer.appendChild(toast);

        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
}

// Global functions for button clicks
function refreshData() {
    window.edgeFinderApp.loadData();
}

function downloadCSV() {
    window.open('/api/csv', '_blank');
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.edgeFinderApp = new EdgeFinderApp();
});
