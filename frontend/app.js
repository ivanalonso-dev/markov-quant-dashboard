async function loadDashboard() {

    // ====================================
    // MARKET DATA
    // ====================================

    const marketResponse = await fetch(
        "http://127.0.0.1:8000/market-data"
    );

    const marketData = await marketResponse.json();

    // ====================================
    // MARKET STATE
    // ====================================

    let shortState = marketData.market_state;



// ====================================
// CLEAN MARKET STATE
// ====================================

if (
    shortState.includes("BULL_MARKET")
) {

    shortState = "Bull Market";

} else if (
    shortState.includes("BEAR_MARKET")
) {

    shortState = "Bear Market";

} else if (
    shortState.includes("SIDEWAYS_CHOP")
) {

    shortState = "Sideways Market";

} else if (
    shortState.includes("PANIC_VOLATILITY")
) {

    shortState = "High Volatility";

} else {

    shortState = "Normal Market";
}

    document.getElementById(
        "market-state"
    ).innerText = shortState;

    // ====================================
    // SIGNAL
    // ====================================

    const signalElement = document.getElementById(
        "signal"
    );

    signalElement.innerText = marketData.signal;

    signalElement.classList.remove(
        "buy",
        "sell",
        "hold"
    );

    if (marketData.signal === "BUY") {

        signalElement.classList.add("buy");

    } else if (marketData.signal === "SELL") {

        signalElement.classList.add("sell");

    } else {

        signalElement.classList.add("hold");
    }

    // ====================================
    // CONFIDENCE
    // ====================================

    document.getElementById(
        "confidence"
    ).innerText =
        marketData.confidence;

    // ====================================
    // BALANCE
    // ====================================

    document.getElementById(
        "balance"
    ).innerText =
        `$${marketData.balance}`;

    // ====================================
    // WINRATE
    // ====================================

    document.getElementById(
        "winrate"
    ).innerText =
        `${marketData.winrate}%`;

    // ====================================
    // SHARPE RATIO
    // ====================================

    document.getElementById(
        "sharpe"
    ).innerText =
        marketData.sharpe_ratio;

    // ====================================
    // BTC HISTORY
    // ====================================

    const btcResponse = await fetch(
        "http://127.0.0.1:8000/btc-history"
    );

    const btcData = await btcResponse.json();

    // ====================================
    // FORMAT DATA
    // ====================================

    const labels = btcData.map(item => {

        const date = new Date(
            item.time * 1000
        );

        return date.toLocaleDateString();
    });

    const prices = btcData.map(
        item => item.value
    );

    // ====================================
    // CHART
    // ====================================

    const ctx = document.getElementById(
        "btcChart"
    );

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{

                label: "BTC Price",

                data: prices,

                borderColor: "#00ff99",

                backgroundColor:
                    "rgba(0,255,153,0.1)",

                borderWidth: 3,

                tension: 0.3,

                fill: true,

                pointRadius: 0
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    labels: {

                        color: "white",

                        font: {

                            size: 14
                        }
                    }
                }
            },

            scales: {

                x: {

                    ticks: {

                        color: "white"
                    },

                    grid: {

                        color:
                            "rgba(255,255,255,0.05)"
                    }
                },

                y: {

                    ticks: {

                        color: "white"
                    },

                    grid: {

                        color:
                            "rgba(255,255,255,0.05)"
                    }
                }
            }
        }
    });
}

// ========================================
// LOAD DASHBOARD
// ========================================

loadDashboard();

// ========================================
// AUTO REFRESH
// ========================================

setInterval(() => {

    location.reload();

}, 10000);